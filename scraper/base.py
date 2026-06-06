import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

CRIME_KEYWORDS = [
    "murder", "killed", "robbery", "theft", "arrested", "police",
    "crime", "attack", "assault", "kidnap", "rape", "shoot", "firing",
    "gang", "violence", "dacoity", "dacoit", "extortion", "blast",
    "bomb", "terrorism", "terrorist", "drug", "smuggling", "qatl",
    "encounter", "dead body", "corpse", "missing", "abduction"
]

def is_crime_related(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRIME_KEYWORDS)

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None

def save_articles(articles, source):
    os.makedirs("data/raw", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    filepath = f"data/raw/{source}_{date_str}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[{source.upper()}] Saved {len(articles)} articles to {filepath}")
    return filepath