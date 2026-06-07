from scraper.base import fetch_page, is_crime_related, save_articles, HEADERS
from datetime import datetime
import requests
from bs4 import BeautifulSoup

EXPRESS_SECTIONS = [
    "https://tribune.com.pk/pakistan",
    "https://tribune.com.pk/latest",
]

def scrape_express():
    articles = []
    seen_urls = set()

    for section_url in EXPRESS_SECTIONS:
        print(f"[EXPRESS] Scraping: {section_url}")
        soup = fetch_page(section_url)
        if not soup:
            continue

        links = soup.find_all("a", href=True)
        article_urls = []

        for link in links:
            href = link["href"]
            if not href.startswith("http"):
                href = "https://tribune.com.pk" + href
            if "/story/" in href and href not in seen_urls:
                article_urls.append(href)
                seen_urls.add(href)

        print(f"[EXPRESS] Found {len(article_urls)} article links in {section_url}")

        for url in article_urls[:20]:
            try:
                resp = requests.get(url, headers=HEADERS, timeout=15)
                soup2 = BeautifulSoup(resp.text, "html.parser")

                headline_tag = (
                    soup2.find("h1", class_="story-title") or
                    soup2.find("h1", class_="top-meta") or
                    soup2.find("h1")
                )
                # Use material-text for body — most specific Express Tribune class
                body_tag = (
                    soup2.find("div", class_="material-text") or
                    soup2.find("div", class_="story-content") or
                    soup2.find("article")
                )

                if not headline_tag or not body_tag:
                    continue

                headline = headline_tag.get_text(strip=True)
                body = body_tag.get_text(separator=" ", strip=True)

                if not is_crime_related(headline + " " + body):
                    continue

                articles.append({
                    "source": "express",
                    "url": url,
                    "headline": headline,
                    "body": body[:2000],
                    "scraped_at": datetime.now().isoformat()
                })

            except Exception as e:
                print(f"[EXPRESS] Error scraping {url}: {e}")
                continue

    save_articles(articles, "express")
    return articles


if __name__ == "__main__":
    scrape_express()