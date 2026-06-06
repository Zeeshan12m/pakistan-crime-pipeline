from scraper.base import is_crime_related, save_articles, HEADERS
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = r"C:\Users\zeeshan\.wdm\drivers\chromedriver\win64\148.0.7778.178\chromedriver-win32\chromedriver.exe"

GEO_SECTIONS = [
    "https://www.geo.tv/category/pakistan",
    "https://www.geo.tv/latest-news",
]

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_geo():
    articles = []
    seen_urls = set()
    driver = get_driver()

    try:
        for section_url in GEO_SECTIONS:
            print(f"[GEO] Scraping: {section_url}")
            driver.get(section_url)
            time.sleep(8)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.find_all("a", href=True)
            article_urls = []

            for link in links:
                href = link["href"]
                if not href.startswith("http"):
                    href = "https://www.geo.tv" + href
                # Geo uses /latest/ pattern
                if "/latest/" in href and href not in seen_urls:
                    article_urls.append(href)
                    seen_urls.add(href)

            print(f"[GEO] Found {len(article_urls)} article links")

            for url in article_urls[:20]:
                try:
                    time.sleep(0.5)
                    resp = requests.get(url, headers=HEADERS, timeout=15)
                    soup2 = BeautifulSoup(resp.text, "html.parser")

                    headline_tag = (
                        soup2.find("h1", class_="story-title") or
                        soup2.find("h1", class_="title") or
                        soup2.find("h1")
                    )
                    body_tag = (
                        soup2.find("div", class_="story-content") or
                        soup2.find("div", class_="content-area") or
                        soup2.find("div", class_="detail") or
                        soup2.find("article")
                    )

                    if not headline_tag or not body_tag:
                        continue

                    headline = headline_tag.get_text(strip=True)
                    if len(headline) < 20:
                        continue

                    body = body_tag.get_text(separator=" ", strip=True)

                    if not is_crime_related(headline + " " + body):
                        continue

                    articles.append({
                        "source": "geo",
                        "url": url,
                        "headline": headline,
                        "body": body[:2000],
                        "scraped_at": datetime.now().isoformat()
                    })
                    print(f"[GEO] ✓ {headline[:60]}")

                except Exception as e:
                    print(f"[GEO] Error scraping {url}: {e}")
                    continue

    finally:
        driver.quit()

    save_articles(articles, "geo")
    return articles


if __name__ == "__main__":
    scrape_geo()