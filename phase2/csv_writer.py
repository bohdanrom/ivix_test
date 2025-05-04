# Standard Library
import csv
import os
import logging
from threading import Lock
from collections import namedtuple

# Third Party
from dotenv import load_dotenv

load_dotenv()
output_lock = Lock()

CSVRow = namedtuple(
    "CSVRow",
    ("Rank", "CoinName", "CoinSymbol", "Price", "Difference24H", "MarketCap"),
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class CoinMarketGathererWriter:
    @staticmethod
    def _gather_all_data(data) -> CSVRow:
        """
        Should be implemented in a subclass to handle a single data item.
        """
        raise NotImplementedError

    def _write_data(self, writer, data):
        parsed_data = self._gather_all_data(data)
        with output_lock:
            writer.writerow(parsed_data)

    def _write_to_file(self, rows):
        """
        Writes all parsed data rows to CSV file.

        Args:
            rows: A collection of HTML objects or API data JSON objects.
        """
        filename = os.getenv("OUTPUT_FILE")
        write_header = not os.path.exists(filename)
        with open(filename, "a+", newline="") as csv_file:
            writer = csv.writer(csv_file)
            if write_header:
                logger.info("File doesn't exist. Adding headers...")
                writer.writerow(CSVRow._fields)
            logger.info(f"Writing parsed data to CSV file[{filename}]...")
            for row in rows:
                self._write_data(writer, row)


__all__ = ["CoinMarketGathererWriter", "CSVRow", "logger"]
