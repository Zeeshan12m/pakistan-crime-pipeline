import spacy
import pandas as pd
import os
from nlp.crime_types import classify_crime
from nlp.severity import calculate_severity

# Load spaCy model - we use a simple approach with city matching
# since Pakistan-specific NER models don't exist

nlp = spacy.load("en_core_web_sm")

# Load Pakistani cities
def load_cities():
    cities_path = "data/geo/pakistan_cities.csv"
    df = pd.read_csv(cities_path)
    # Create lookup dict: lowercase city name -> row
    return {row["city"].lower(): row for _, row in df.iterrows()}

CITIES = load_cities()

def extract_city(text):
    text_lower = text.lower()
    found = []
    for city_name in CITIES:
        if city_name in text_lower:
            found.append(city_name)
    if not found:
        return None, None, None
    # Return the first match (longest match wins if ties)
    found.sort(key=len, reverse=True)
    city = found[0]
    row = CITIES[city]
    return row["city"], row["lat"], row["lon"]

def extract_article(article):
    text = article.get("headline", "") + " " + article.get("body", "")
    crime_type = classify_crime(text)
    city, lat, lon = extract_city(text)
    severity = calculate_severity(text, crime_type)

    return {
        "source": article.get("source"),
        "url": article.get("url"),
        "headline": article.get("headline"),
        "crime_type": crime_type,
        "city": city,
        "lat": lat,
        "lon": lon,
        "severity": severity,
        "scraped_at": article.get("scraped_at"),
        "body_snippet": article.get("body", "")[:300]
    }
PAKISTAN_FILTER_TERMS = [
    "pakistan", "karachi", "lahore", "islamabad", "rawalpindi",
    "peshawar", "quetta", "faisalabad", "multan", "hyderabad",
    "balochistan", "sindh", "punjab", "kpk", "khyber", "gilgit",
    "ispr", "fir", "police", "pti", "pmln", "ppp", "fia", "nab"
]

def is_pakistan_relevant(text):
    text_lower = text.lower()
    return any(term in text_lower for term in PAKISTAN_FILTER_TERMS)