#!/usr/bin/env python3
import feedparser
import yaml
from pathlib import Path
from dateutil import parser as dateparser
from datetime import datetime

# Determine the repository root based on script location
SCRIPT_DIR = Path(__file__).resolve().parent      # assets/python
REPO_ROOT = SCRIPT_DIR.parent.parent              # repo root
DATA_DIR = REPO_ROOT / "_data"

NEWS_FILE = DATA_DIR / "news.yml"
PI_FILE = DATA_DIR / "pis.yml"

def load_pis():
    """Load PI list from pis.yml"""
    if not PI_FILE.exists():
        raise FileNotFoundError(f"Could not find PI file at {PI_FILE}")
    with open(PI_FILE) as f:
        data = yaml.safe_load(f)
    pis = data.get("pis", [])
    return pis

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

def fetch_articles():
    """Fetch articles from a separate RSS feed per PI"""
    pis = load_pis()
    existing = load_existing()
    existing_urls = {item["url"] for item in existing}
    new_items = []

    for pi in pis:
        query = f"{pi} Synthetic Biology UCSD"
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(rss_url)
        print(f"Fetched {len(feed.entries)} entries for PI '{pi}'")

        for entry in feed.entries:
            url = entry.link
            if url in existing_urls:
                continue

            pub_date = normalize_date(entry.get("published", ""))
            source = entry.source.title if "source" in entry else "Google News"
            summary = entry.summary if "summary" in entry else ""

            item = {
                "title": entry.title,
                "url": url,
                "source": source,
                "date": pub_date,
                "summary": summary,
                "tags": [pi, "UCSD Synthetic Biology"]
            }
            new_items.append(item)
            existing_urls.add(url)

    if new_items:
        print(f"Adding {len(new_items)} new articles")
        existing.extend(new_items)
        save_news(existing)
    else:
        print("No new articles found")

if __name__ == "__main__":
    fetch_articles()
