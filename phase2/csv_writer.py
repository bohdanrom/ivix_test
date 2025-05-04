# Standard Library
import os
import csv
import logging
from threading import Lock
from collections import namedtuple

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
    def __init__(self, config):
        self._config = config

    @staticmethod
    def _write_row(writer, row):
        with output_lock:
            try:
                writer.writerow(row)
            except Exception as e:
                logger.error(f"Row wasn't added to the file. Details: {e}")

    def write_to_file(self, rows, parse_function):
        """
        Writes all parsed data rows to CSV file.

        Args:
            rows: A collection of HTML objects or API data JSON objects.
            parse_function: A method that extracts data for CSV row.
        """
        filename = self._config.OUTPUT_FILE
        write_header = not os.path.exists(filename)
        with open(filename, "a+", newline="") as csv_file:
            writer = csv.writer(csv_file)

            if write_header:
                logger.info("File doesn't exist. Adding headers...")
                self._write_row(writer, CSVRow._fields)

            logger.info(f"Writing parsed data to CSV file[{filename}]...")
            for row in rows:
                csv_row = parse_function(row)
                self._write_row(writer, csv_row)


__all__ = ["CoinMarketGathererWriter", "CSVRow", "logger"]
