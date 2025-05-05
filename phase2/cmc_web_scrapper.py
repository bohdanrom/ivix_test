# Standard Library
import time
from urllib.parse import urlencode

# Third Party
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright

# Relative
from csv_writer import CSVRow, logger


class CoinMarketWebScraper:
    """
    Gathers coin data by scraping the CoinMarketCap public website using Playwright.
    """

    def __init__(self, config, writer, page: int = 1):
        self._config = config
        self._url = self.__prepare_url(page)
        self._csv_writer = writer(config)

    def __prepare_url(self, page: int = 1):
        params = {"page": page}
        return self._config.WEB_URL + "?" + urlencode(params)

    def _open_page(self, p: Playwright):
        """
        Opens the specified page using a headless Playwright browser.

        Args:
            p: A Playwright instance.
        Returns:
            page: The loaded page.
        """
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        logger.info(f"Open CoinMarketCap web page[{self._url}]...")
        page.goto(self._url)
        return page

    @staticmethod
    def _scroll_down_all_page(page):
        """
        Scrolls down the page to trigger lazy loading of content.
        Returns:
            None
        """
        for i in range(5):
            page.mouse.wheel(0, 2000)
            time.sleep(0.05)

    @staticmethod
    def _gather_all_data(table_row) -> CSVRow:
        """
        Parses a single HTML table row into a CSVRow.

        Args:
            table_row: A <tr> element from the page.
        Returns:
            obj(`NamedTuple`): A structured row of coin data.
        """
        price_decreasing_class = "icon-Caret-down"
        price = table_row.find("div", {"class": "sc-142c02c-0"})
        price_span = price.find("span")
        rank = table_row.find("p", {"class": "sc-71024e3e-0"})
        coin_name = table_row.find("p", {"class": "coin-item-name"})
        coin_symbol = table_row.find("p", {"class": "coin-item-symbol"})
        difference_24h = table_row.find_all("span", {"class": "sc-1e8091e1-0"})[1]
        diff_24h = difference_24h.text
        if price_decreasing_class in difference_24h.next_element.attrs["class"]:
            diff_24h = "-" + difference_24h.text
        market_cap = table_row.find("span", {"class": "sc-11478e5d-1"})
        return CSVRow(
            rank.text,
            coin_name.text,
            coin_symbol.text,
            price_span.text,
            diff_24h,
            market_cap.text,
        )

    def parse(self):
        """
        Loads the page, scrolls, parses the table, and writes to CSV.
        """
        with sync_playwright() as p:
            page = self._open_page(p)
            self._scroll_down_all_page(page)
            html = BeautifulSoup(page.content(), "html.parser")
            logger.info(f"Scrapping CoinMarketCap HTML page[{self._url}]...")
            table = html.find("tbody")
            rows = table.find_all("tr")
            self._csv_writer.write_to_file(rows, self._gather_all_data)


__all__ = ["CoinMarketWebScraper"]
