# Standard Library
import sys
import time

# Relative
from config import AppConfig
from database import DBWriter
from presenter import Presenter
from coin_gecko_parser import CoinGeckoParser


class CoinGeckoApplication:
    """
    Application to receive current BTC price.
    """

    def __init__(
        self,
        config: AppConfig,
        parser: CoinGeckoParser,
        db_writer: DBWriter,
        presenter: Presenter,
    ):
        self._run = True
        self._config = config
        self._parser = parser
        self._writer = db_writer
        self._presenter = presenter

    @staticmethod
    def shutdown():
        print("\nShutting down…")
        sys.exit(0)

    def run(self):
        DBWriter.db_init()
        try:
            parser = self._parser(self._config)
            while self._run:
                data = parser.get_crypto_data()
                self._writer.insert_into_db(data)
                self._presenter.formatted_print(data)
                time.sleep(1)
        except KeyboardInterrupt:
            self._run = False
            self.shutdown()


if __name__ == "__main__":
    config = AppConfig()
    app = CoinGeckoApplication(config, CoinGeckoParser, DBWriter, Presenter)
    app.run()
