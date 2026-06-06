from scraper.base import fetch_page, is_crime_related, save_articles, HEADERS
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

DAWN_SECTIONS = [
    "https://www.dawn.com/pakistan",
    "https://www.dawn.com/news/latest-news",
]

SKIP_KEYWORDS = ["dawn images", "aurora", "magazine", "herald", "weekly"]

def scrape_dawn():
    articles = []
    seen_urls = set()

    for section_url in DAWN_SECTIONS:
        print(f"[DAWN] Scraping: {section_url}")
        soup = fetch_page(section_url)
        if not soup:
            continue

        links = soup.find_all("a", href=True)
        article_urls = []

        for link in links:
            href = link["href"]
            if (
                href.startswith("https://www.dawn.com/news/")
                and href not in seen_urls
            ):
                article_urls.append(href)
                seen_urls.add(href)

        print(f"[DAWN] Found {len(article_urls)} unique article links")

        for url in article_urls[:30]:
            try:
                time.sleep(0.5)
                resp = requests.get(url, headers=HEADERS, timeout=15)
                soup2 = BeautifulSoup(resp.text, "html.parser")

                # More specific selectors for Dawn
                headline_tag = (
                    soup2.find("h1", class_="story__title") or
                    soup2.find("h2", class_="story__title") or
                    soup2.find("h1")
                )
                body_tag = (
                    soup2.find("div", class_="story__content") or
                    soup2.find("div", class_="template-definition__story") or
                    soup2.find("article")
                )

                if not headline_tag or not body_tag:
                    continue

                headline = headline_tag.get_text(strip=True)

                # Skip non-article pages
                if any(skip in headline.lower() for skip in SKIP_KEYWORDS):
                    continue

                # Skip very short headlines (nav items, etc.)
                if len(headline) < 20:
                    continue

                body = body_tag.get_text(separator=" ", strip=True)

                if not is_crime_related(headline + " " + body):
                    continue

                articles.append({
                    "source": "dawn",
                    "url": url,
                    "headline": headline,
                    "body": body[:2000],
                    "scraped_at": datetime.now().isoformat()
                })
                print(f"[DAWN] ✓ {headline[:60]}")

            except Exception as e:
                print(f"[DAWN] Error scraping {url}: {e}")
                continue

    save_articles(articles, "dawn")
    return articles


if __name__ == "__main__":
    scrape_dawn()