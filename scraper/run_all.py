from scraper.dawn import scrape_dawn
from scraper.geo import scrape_geo
from scraper.express import scrape_express

def run_all():
    print("=" * 50)
    print("Starting full scrape run")
    print("=" * 50)

    dawn_articles = scrape_dawn()
    geo_articles = scrape_geo()
    express_articles = scrape_express()

    total = len(dawn_articles) + len(geo_articles) + len(express_articles)
    print(f"\nScrape complete. Total crime articles collected: {total}")

if __name__ == "__main__":
    run_all()