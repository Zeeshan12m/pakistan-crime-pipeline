CRIME_CATEGORIES = {
    "murder": [
        "murder", "killed", "kill", "qatl", "homicide", "shot dead",
        "stabbed to death", "dead body", "corpse", "found dead"
    ],
    "terrorism": [
        "terrorist", "terrorism", "blast", "bomb", "suicide bomber",
        "ied", "explosion", "attack", "militant", "extremist",
        "ispr", "india-backed", "banned outfit"
    ],
    "robbery": [
        "robbery", "robbed", "dacoity", "dacoit", "looted", "snatching",
        "mugging", "stolen", "theft", "burglar", "burglary"
    ],
    "kidnapping": [
        "kidnap", "kidnapping", "abduction", "abducted", "missing person",
        "held hostage", "ransom"
    ],
    "assault": [
        "assault", "attack", "beaten", "injured", "acid attack",
        "torture", "violence", "wounded"
    ],
    "sexual_crime": [
        "rape", "sexual assault", "harassment", "molest", "zyadti"
    ],
    "drug_crime": [
        "drug", "narcotics", "smuggling", "heroin", "contraband",
        "trafficking", "seized drugs"
    ],
    "cybercrime": [
        "cybercrime", "hacking", "online fraud", "scam", "deepfake",
        "ai-generated obscene", "tiktok"
    ],
    "corruption": [
        "corruption", "nab", "fraud", "embezzlement", "bribery",
        "money laundering", "fake accounts"
    ],
    "extortion": [
        "extortion", "bhatta", "ransom demand", "threatening"
    ]
}

def classify_crime(text):
    text_lower = text.lower()
    scores = {}
    for category, keywords in CRIME_CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score
    if not scores:
        return "other"
    return max(scores, key=scores.get)