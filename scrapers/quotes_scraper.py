"""Quotes to Scrape listing-page scraper; pagination follows each next link."""
import logging
from urllib.parse import urljoin
import requests
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)
START_URL = "https://quotes.toscrape.com/"

class QuotesScraper(BaseScraper):
    def scrape(self):
        url, page, records = START_URL, 1, []
        visited = set()
        while url and url not in visited:
            visited.add(url)
            logger.info("Quotes page %d: %s", page, url)
            try:
                soup = self.get_soup(url)
            except requests.RequestException as exc:
                logger.error("Quotes request failed at %s: %s", url, exc)
                break
            for quote in soup.select("div.quote"):
                try:
                    body = quote.select_one("span.text")
                    author = quote.select_one("small.author")
                    records.append({"source": "Quotes to Scrape", "source_url": url,
                        "name_or_title": body.get_text(" ", strip=True) if body else None,
                        "category": None, "price": None, "rating": None,
                        "author": author.get_text(" ", strip=True) if author else None,
                        "tags": [tag.get_text(" ", strip=True) for tag in quote.select("a.tag")],
                        "description": None})
                except (AttributeError, TypeError, ValueError) as exc:
                    logger.warning("Skipping malformed quote on %s: %s", url, exc)
            nxt = soup.select_one("li.next > a")
            url = urljoin(url, nxt.get("href")) if nxt and nxt.get("href") else None
            page += 1
        return records
