from rapidfuzz import fuzz

SIMILARITY_THRESHOLD = 85  # headlines more similar than this = duplicate

def deduplicate(articles):
    unique = []
    for article in articles:
        headline = article.get("headline", "")
        is_duplicate = False
        for kept in unique:
            similarity = fuzz.token_sort_ratio(headline, kept.get("headline", ""))
            if similarity >= SIMILARITY_THRESHOLD:
                is_duplicate = True
                break
        if not is_duplicate:
            unique.append(article)
    removed = len(articles) - len(unique)
    print(f"[DEDUP] Removed {removed} duplicates, kept {len(unique)} unique articles")
    return unique