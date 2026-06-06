SEVERITY_WEIGHTS = {
    # Crime type base scores
    "terrorism": 9,
    "murder": 8,
    "sexual_crime": 7,
    "kidnapping": 7,
    "assault": 5,
    "robbery": 5,
    "extortion": 5,
    "drug_crime": 4,
    "corruption": 4,
    "cybercrime": 3,
    "other": 2,
}

AMPLIFIERS = {
    "multiple": 1.5,      # multiple victims
    "children": 1.5,      # victim is a child
    "women": 1.3,         # victim is a woman
    "police": 1.2,        # police involved or targeted
    "mass": 2.0,          # mass casualty
    "gang": 1.3,          # gang-related
    "armed": 1.2,         # armed perpetrators
    "dead": 1.4,          # fatalities confirmed
    "killed": 1.4,
    "blast": 1.6,
    "bomb": 1.6,
}

def calculate_severity(text, crime_type):
    base = SEVERITY_WEIGHTS.get(crime_type, 2)
    multiplier = 1.0
    text_lower = text.lower()

    for keyword, weight in AMPLIFIERS.items():
        if keyword in text_lower:
            multiplier = max(multiplier, weight)

    raw_score = base * multiplier
    # Clamp between 1 and 10
    return round(min(10, max(1, raw_score)), 1)