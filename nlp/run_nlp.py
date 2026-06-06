import json
import glob
import pandas as pd
import os
from datetime import datetime
from nlp.extractor import extract_article, is_pakistan_relevant
from nlp.deduplicator import deduplicate

def load_raw_articles():
    articles = []
    files = glob.glob("data/raw/*.json")
    for filepath in files:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            articles.extend(data)
    print(f"[NLP] Loaded {len(articles)} raw articles from {len(files)} files")
    return articles

def run_nlp_pipeline():
    print("=" * 50)
    print("Starting NLP pipeline")
    print("=" * 50)

    # Load raw articles
    articles = load_raw_articles()

    # Deduplicate first
    articles = deduplicate(articles)

    # Extract features
    # Extract features
    print(f"[NLP] Extracting features from {len(articles)} articles...")
    extracted = []
    skipped = 0
    for article in articles:
        headline = article.get("headline", "")
        body = article.get("body", "")
        # Require Pakistan relevance in headline OR strong signal in first 200 chars of body
        if not is_pakistan_relevant(headline) and not is_pakistan_relevant(body[:200]):
            skipped += 1
            continue
        result = extract_article(article)
        extracted.append(result)
        print(f"[NLP] ✓ [{result['crime_type']}] [{result['city'] or 'unknown'}] "
              f"[severity: {result['severity']}] {result['headline'][:50]}")
    print(f"[NLP] Skipped {skipped} non-Pakistan articles")

    # Save to CSV
    os.makedirs("data/processed", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    output_path = f"data/processed/extracted_{date_str}.csv"
    df = pd.DataFrame(extracted)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n[NLP] Saved {len(extracted)} records to {output_path}")

    # Print summary
    print("\n--- Summary ---")
    print(df["crime_type"].value_counts().to_string())
    print(f"\nCities found: {df['city'].nunique()} unique")
    print(f"Articles with no city: {df['city'].isna().sum()}")

    return df

if __name__ == "__main__":
    run_nlp_pipeline()