# IVIX Coding Exercise CoinMarketCap Data Gatherer

## Phase 1

A Python tool to gather current BTC price form [CoinGecko](https://www.coingecko.com/) compared to USD every second. As well as calculation SMA for last 10 prices.

## Phase 2

A Python tool to gather cryptocurrency data from [CoinMarketCap](https://coinmarketcap.com/) using either their **official API** or **public website** (via Playwright). 
The data is saved to a CSV file and supports concurrent execution using threads.

---
### Installation

1. **Clone the repository**

```shell
git clone https://github.com/yourusername/coinmarketcap-gatherer.git
cd coinmarketcap-gatherer
```

2. **Install dependencies with Pipenv**
```shell
pipenv install
pipenv shell
```

3. **Install Playwright browser binaries**
```shell
playwright install
```

4. **Set up environment variables**

Please specify your appropriate API keys in every .env files

```shell
API_KEY=<YOUR API KEY>
```

---

### Usage

1. **Phase 1**
```shell
cd phase1
pipenv run python app.py
```

2. **Phase 2**
```shell
cd phase2
# Scrape first 5 pages of the website
pipenv run python run.py --mode web --pages 5

# Fetch first 3 pages (300 coins) from the API
pipenv run python run.py --mode api --pages 3
```