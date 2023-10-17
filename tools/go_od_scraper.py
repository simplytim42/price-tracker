import httpx
import logging
from selectolax.parser import HTMLParser
from .base_scraper import BaseScraper, ScraperException


class GoOutdoorsScraper(BaseScraper):
    html = None
    PRICE_SELECTOR = "span.regular-price"
    TITLE_SELECTOR = "span.product-name"

    def __init__(self, id: str):
        sku = id.split("-")[-1]
        self.URL = f"https://www.gooutdoors.co.uk/{sku}/{id}"

    def __get_html(self):
        try:
            response = httpx.get(self.URL, headers=self.headers)
            response.raise_for_status()
            self.html = HTMLParser(response.text)
        except Exception as e:
            logging.error(f"Error getting HTML: {e}")
            raise ScraperException("Failed to get HTML")

    def get_price(self) -> str:
        if not self.html:
            self.__get_html()
        try:
            return self.html.css_first(self.PRICE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(f"Error getting price: {e}")
            return "Price not found"

    def get_title(self) -> str:
        if not self.html:
            self.__get_html()
        try:
            return self.html.css_first(self.TITLE_SELECTOR).text(strip=True)
        except AttributeError as e:
            logging.warning(f"Error getting title: {e}")
            return "Title not found"
