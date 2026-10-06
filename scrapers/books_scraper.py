"""Books to Scrape listing-page scraper; pagination follows each next link."""
import logging
from urllib.parse import urljoin
import requests
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)
START_URL = "https://books.toscrape.com/"

class BooksScraper(BaseScraper):
    def scrape(self):
        url, page, records = START_URL, 1, []
        visited = set()
        while url and url not in visited:
            visited.add(url)
            logger.info("Books page %d: %s", page, url)
            try:
                soup = self.get_soup(url)
            except requests.RequestException as exc:
                logger.error("Books request failed at %s: %s", url, exc)
                break
            for article in soup.select("article.product_pod"):
                try:
                    link = article.select_one("h3 > a")
                    price = article.select_one("p.price_color")
                    rating = article.select_one("p.star-rating")
                    records.append({"source": "Books to Scrape",
                        "source_url": urljoin(url, link.get("href", "")) if link else None,
                        "name_or_title": link.get("title") if link else None,
                        "category": None, "price": price.get_text(" ", strip=True) if price else None,
                        "rating": " ".join(rating.get("class", [])) if rating else None,
                        "author": None, "tags": None, "description": None})
                except (AttributeError, TypeError, ValueError) as exc:
                    logger.warning("Skipping malformed book on %s: %s", url, exc)
            nxt = soup.select_one("li.next > a")
            url = urljoin(url, nxt.get("href")) if nxt and nxt.get("href") else None
            page += 1
        return records
