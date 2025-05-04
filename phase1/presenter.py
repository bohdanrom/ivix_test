# Standard Library
from datetime import datetime

# Relative
from database import DBWriter
from sma_calc import SMACalculator


class Presenter:
    @staticmethod
    def formatted_print(crypto_data):
        last_updated_datetime = datetime.fromtimestamp(crypto_data.last_updated_at)
        formatted_datetime = last_updated_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        last_ten_records = DBWriter.get_last_ten_records()
        total_price, last_n = SMACalculator.calc_last_ten(last_ten_records)
        print(
            f"[{formatted_datetime}] BTC → USD: ${crypto_data.usd:0,.2f} SMA({last_n}): {total_price / last_n:,.2f}"
        )


__all__ = ["Presenter"]
