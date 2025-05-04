# Standard Library
from concurrent.futures.thread import ThreadPoolExecutor

# Third Party
import click

# Relative
from cmc_api_manager import CoinMarketAPIManager
from cmc_web_scrapper import CoinMarketWebScraper


@click.command()
@click.option(
    "--mode",
    type=click.Choice(["web", "api"]),
    default="web",
    show_default=True,
    help="Select data source: web or API.",
)
@click.option(
    "--pages",
    type=int,
    default=5,
    show_default=True,
    help="Number of pages/start values to fetch.",
)
def main(mode, pages):
    with ThreadPoolExecutor(max_workers=5) as executor:
        handler = CoinMarketWebScraper
        if mode == "api":
            handler = CoinMarketAPIManager
        executor.map(lambda page: handler(page).parse(), range(1, pages + 1))


if __name__ == "__main__":
    main()
