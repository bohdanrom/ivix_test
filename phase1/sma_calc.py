# Relative
from database import DBWriter


class SMACalculator:
    @staticmethod
    def calc_last_ten():
        total_sum = 0
        last_ten_records = DBWriter.get_last_ten_records()
        for crypto, usd_price, last_updated_at in last_ten_records:
            total_sum += float(usd_price)
        return total_sum, len(last_ten_records)


__all__ = ["SMACalculator"]
