"""Shared, polite HTTP support for the practice-site scrapers."""
import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, delay: float = 0.5, timeout: float = 15.0):
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ScrapingAssignment/1.0 (educational project)"})
        retry = Retry(total=3, connect=3, read=2, status=3, backoff_factor=0.5,
                      status_forcelist=(429, 500, 502, 503, 504),
                      allowed_methods=frozenset(["GET"]), respect_retry_after_header=True)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self._requested = False

    def get_soup(self, url):
        from bs4 import BeautifulSoup
        if self._requested:
            time.sleep(self.delay)
        self._requested = True
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")

    def close(self):
        self.session.close()
