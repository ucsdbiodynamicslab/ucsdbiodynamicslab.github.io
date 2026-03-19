#!/usr/bin/env python3
import feedparser
import yaml
from pathlib import Path
from dateutil import parser as dateparser
from datetime import datetime
import re

# Determine the repository root based on script location
SCRIPT_DIR = Path(__file__).resolve().parent      # assets/python
REPO_ROOT = SCRIPT_DIR.parent.parent              # repo root
DATA_DIR = REPO_ROOT / "_data"

NEWS_FILE = DATA_DIR / "news.yml"
PI_FILE = DATA_DIR / "pis.yml"

# Stopwords to ignore for keyword generation
STOPWORDS = {
    "The", "And", "For", "With", "From", "This", "That", "Are", "Was", 
    "Has", "Have", "Will", "Its", "Their", "About", "Through", "Your", "They",
    "Researchers", "Research", "Study", "Studies", "Approach", "Demonstrate",
    "Anti", "Building", "New", "Novel", "Method", "Methods", "Tool", "Tools",
    "Platform", "Platforms", "System", "Systems", "Synthetic", "Biology", "UCSD"
}

def load_pis():
    with open(PI_FILE) as f:
        data = yaml.safe_load(f)
    return [pi["name"] for pi in data.get("pis", [])]


def load_existing():
    """Load existing news articles from news.yml"""
    if NEWS_FILE.exists():
        with open(NEWS_FILE) as f:
            return yaml.safe_load(f) or []
    return []


def save_news(news):
    """Sort news by date descending and save to YAML"""
    news_sorted = sorted(news, key=lambda x: x["date"], reverse=True)
    with open(NEWS_FILE, "w") as f:
        yaml.dump(news_sorted, f, sort_keys=False)


def normalize_date(date_str):
    """Convert date string to ISO date"""
    try:
        dt = dateparser.parse(date_str)
        return dt.isoformat()
    except Exception:
        return datetime.now().isoformat()


def generate_keywords(text, max_keywords=5):
    """
    Generate selective keywords from title + summary:
    - Only capitalized words or sequences of capitalized words (1-3 words)
    - Hyphenated words count as single words
    - Exclude stopwords
    - Deduplicate and limit number
    """
    # Treat hyphenated words as a single word by matching [A-Z][a-z-]+
    phrases = re.findall(r'\b(?:[A-Z][a-z-]+\s?){1,3}\b', text)
    keywords = []
    seen = set()
    for p in phrases:
        phrase = p.strip()
        if not phrase or phrase in STOPWORDS or len(phrase) < 4:
            continue
        key = phrase.lower()
        if key not in seen:
            keywords.append(phrase)
            seen.add(key)
        if len(keywords) >= max_keywords:
            break
    return keywords


def fetch_articles():
    """Fetch articles from a separate RSS feed per PI with selective tags"""
    pis = load_pis()
    existing = load_existing()
    existing_urls = {item["url"]: item for item in existing}
    new_items = []

    for pi in pis:
        query = f"{pi} Synthetic Biology UCSD"
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)
        print(f"Fetched {len(feed.entries)} entries for PI '{pi}'")

        for entry in feed.entries:
            url = entry.link
            pub_date = normalize_date(entry.get("published", ""))
            source = entry.source.title if "source" in entry else "Google News"
            summary = entry.summary if "summary" in entry else ""
            combined_text = f"{entry.title} {summary}"

            # Generate selective extra keywords for tags
            extra_keywords = generate_keywords(combined_text)

            # Base tags
            base_tags = ["UCSD Synthetic Biology"] + extra_keywords

            if url in existing_urls:
                # Merge PI name if article already exists
                existing_item = existing_urls[url]
                updated_tags = set(existing_item.get("tags", []) + [pi] + base_tags)
                existing_item["tags"] = sorted(updated_tags)
            else:
                item = {
                    "title": entry.title,
                    "url": url,
                    "source": source,
                    "date": pub_date,
                    "summary": summary,
                    "tags": [pi] + base_tags
                }
                new_items.append(item)
                existing_urls[url] = item

    if new_items:
        print(f"Adding {len(new_items)} new articles")
        existing.extend(new_items)
        save_news(existing)
    else:
        print("No new articles found")


if __name__ == "__main__":
    fetch_articles()
