# Standard Library
import time
import logging

# Third Party
import requests
from pydantic import BaseModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class APIResponse(BaseModel):
    crypto: str
    usd: int
    last_updated_at: int


class CoinGeckoParser:
    """
    Fetch current BTC price compared to USD.
    """

    def __init__(self, config):
        self._api_key = config.API_KEY
        self._base_url = config.API_KEY

    def _prepare_url(self):
        return self._base_url + f"&{self._api_key}"

    def _wait(self, errors_count: int = 0):
        time_to_sleep = 2 ** errors_count
        logger.info(
            f"Something went wrong with request. We are retrying in {time_to_sleep} seconds..."
        )
        time.sleep(time_to_sleep)

    def _prepare_response(self, request):
        response = request.json()
        crypto_data = response.get("bitcoin")
        crypto_data["crypto"] = "bitcoin"
        return APIResponse(**crypto_data)

    def _send_request(self, number_of_retries: int = 0):
        url = self._prepare_url()
        headers = {
            "accept": "application/json",
        }
        try:
            request = requests.get(url, headers=headers)
        except Exception as e:
            self._wait(number_of_retries)
            if number_of_retries >= 4:
                logger.error(f"Failed to fetch the data from {url}. Details: {e}")
            return self.get_crypto_data(number_of_retries + 1)
        else:
            return self._prepare_response(request)

    def get_crypto_data(self, errors_count: int = 0):
        return self._send_request(errors_count)


__all__ = ["CoinGeckoParser"]
