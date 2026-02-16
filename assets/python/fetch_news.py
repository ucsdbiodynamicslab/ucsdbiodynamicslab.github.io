#!/usr/bin/env python3
import feedparser
import yaml
from pathlib import Path
from dateutil import parser as dateparser
from datetime import datetime

# Assume the script lives at assets/python/fetch_news.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # repo root
NEWS_FILE = BASE_DIR / "_data/news.yml"
PI_FILE = BASE_DIR / "_data/pis.yml"

# Google News RSS feed (broad search)
RSS_URL = "https://news.google.com/rss/search?q=UCSD+Synthetic+Biology&hl=en-US&gl=US&ceid=US:en"

def load_filters():
    """Load required terms and PI list from pis.yml"""
    with open(PI_FILE) as f:
        data = yaml.safe_load(f)
    required_terms = data.get("primary_filters", [])
    pi_terms = data.get("pis", [])
    return required_terms, pi_terms

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

def article_matches(text, required_terms, pi_terms):
    """Return True if text matches (all required_terms AND any PI)"""
    text_lower = text.lower()
    if not all(term.lower() in text_lower for term in required_terms):
        return False
    if not any(pi.lower() in text_lower for pi in pi_terms):
        return False
    return True

def normalize_date(date_str):
    """Convert date string to ISO date"""
    try:
        dt = dateparser.parse(date_str)
        return dt.isoformat()
    except Exception:
        return datetime.now().isoformat()

def fetch_articles():
    """Fetch articles from RSS feed and apply filtering"""
    feed = feedparser.parse(RSS_URL)
    required_terms, pi_terms = load_filters()
    existing = load_existing()
    existing_urls = {item["url"] for item in existing}
    new_items = []

    for entry in feed.entries:
        url = entry.link
        if url in existing_urls:
            continue

        text = f"{entry.title} {entry.summary if 'summary' in entry else ''}"
        if not article_matches(text, required_terms, pi_terms):
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
            "tags": ["UCSD Synthetic Biology"]  # optional, can add more dynamic tags later
        }
        new_items.append(item)

    if new_items:
        print(f"Adding {len(new_items)} new articles")
        existing.extend(new_items)
        save_news(existing)
    else:
        print("No new articles found")

if __name__ == "__main__":
    fetch_articles()
