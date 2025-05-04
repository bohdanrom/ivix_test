# Standard Library
import os

# Third Party
import requests
from dotenv import load_dotenv

# Relative
from csv_writer import CoinMarketGathererWriter, CSVRow, logger

load_dotenv()


class CoinMarketAPIManager(CoinMarketGathererWriter):
    URL = os.getenv("API_URL")

    def __init__(self, start: int = 1):
        self._url = self.__prepare_url(start)

    def __prepare_url(self, start):
        limit = 100
        return self.URL + f"?{start=}&{limit=}&convert=USD"

    @staticmethod
    def _gather_all_data(coin_data) -> CSVRow:
        """
        Parses a single coin's JSON object from the API into a CSVRow.

        Args:
            coin_data: A dictionary representing a single coin's data.
        Returns:
            obj(`NamedTuple`): A structured row of coin data.
        """
        price = coin_data["quote"]["USD"]["price"]
        rank = coin_data.get("cmc_rank", "")
        coin_name = coin_data.get("name", "")
        coin_symbol = coin_data.get("symbol", "")
        difference_24h = coin_data["quote"]["USD"]["percent_change_24h"]
        market_cap = coin_data["quote"]["USD"]["market_cap"]
        return CSVRow(
            rank,
            coin_name,
            coin_symbol,
            price,
            difference_24h,
            market_cap,
        )

    def _fire_request(self):
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": os.getenv("API_KEY"),
        }
        try:
            logger.info(f"Sending request to CoinMarketCap API [{self._url}]...")
            request = requests.get(self._url, headers=headers)
        except Exception as e:
            logger.warning(f"Failed to fetch the data from API. Detaisl: {e}")
        else:
            response = request.json()
            return response

    def parse(self):
        """
        Fetches data from the CoinMarketCap API and writes it to a CSV file.
        """
        response = self._fire_request()
        data = response["data"]
        self._write_to_file(data)


__all__ = ["CoinMarketAPIManager"]
