class SMACalculator:
    @staticmethod
    def calc_last_ten(last_ten_records):
        total_sum = 0
        for crypto, usd_price, last_updated_at in last_ten_records:
            total_sum += float(usd_price)
        return total_sum, len(last_ten_records)


__all__ = ["SMACalculator"]
