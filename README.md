# About This Project

This project is a fork of Martin Simon's 'coinmarketcap' module, which had not been updated for a while ([original repository](https://github.com/barnumbirr/coinmarketcap)). This version has been extensively reworked to be compatible with the latest CoinMarketCap API, diverging significantly from the original source. As a result, it is not backwards compatible, but it brings new capabilities and improvements tailored to the current API's structure and requirements.

As of now, the project only supports the `v1/cryptocurrency/listings/latest` endpoint which is usable by anyone with a a free API key from CoinMarketCap. Obtain your free API key by signing up at [CoinMarketCap API](https://pro.coinmarketcap.com/signup/). 

## Prerequisites

- An API key from [CoinMarketCap Pro](https://pro.coinmarketcap.com/signup/).

## Installation

Install byteforge-coinmarketcap

```bash
pip install byteforge-coinmarketcap
```

## Usage

This section will guide you through the process of using the Market object to fetch the latest listings from CoinMarketCap.

### Initialization

First, create an instance of the `Market` class with your API key:

```python
from coinmarketcap import Market
from coinmarketcap import SortOption

API_KEY = 'your_api_key_here'
coinmarketcap = Market(api_key=API_KEY)
```

Get the top 5 token states by market cap (A TokenState is a snapshot of a token at a certain point of time, for listings_latest, that time will always be "now")


```python
token_states = coinmarketcap.listings_latest(sort_by=SortOption.MARKET_CAP, limit=5)

for token in tokens:
    print(token.name, token.symbol, token.quote['USD'].price)

Bitcoin BTC 51121.78037849647
Ethereum ETH 2912.0337516792188
Tether USDt USDT 0.9996898483447065
BNB BNB 369.2725354702457
Solana SOL 103.68827889524766
```

## Sort Option Parameters

The `SortOption` enum provides various parameters you can use to sort the listings fetched from CoinMarketCap. Below are the available sort options:

- `MARKET_CAP`: Sort by market capitalization.
- `MARKET_CAP_STRICT`: Strict sorting by market capitalization.
- `NAME`: Sort by the name of the token.
- `SYMBOL`: Sort by the symbol of the token.
- `DATE_ADDED`: Sort by the date the token was added to CoinMarketCap.
- `PRICE`: Sort by the price of the token.
- `CIRCULATING_SUPPLY`: Sort by circulating supply.
- `TOTAL_SUPPLY`: Sort by total supply.
- `MAX_SUPPLY`: Sort by maximum supply.
- `NUM_MARKET_PAIRS`: Sort by the number of market pairs.
- `MARKET_CAP_BY_TOTAL_SUPPLY_STRICT`: Strict sorting by market capitalization by total supply.
- `VOLUME_24H`: Sort by 24-hour volume.
- `VOLUME_7D`: Sort by 7-day volume.
- `VOLUME_30D`: Sort by 30-day volume.
- `PERCENT_CHANGE_1H`: Sort by percent change in the last hour.
- `PERCENT_CHANGE_24H`: Sort by percent change in the last 24 hours.
- `PERCENT_CHANGE_7D`: Sort by percent change in the last 7 days.

To use a sort option, simply pass the desired `SortOption` value to the `listings_latest` method's `sort_by` parameter, and use `SortDir` to specificy sort direction:

```python
from coinmarketcap import SortOption, SortDir

# Example: Sort by price in descending order
tokens = coinmarketcap.listings_latest(sort_by=SortOption.PRICE, sort_dir=SortDir.DESC)
```

## Using Filter Options

The `FilterOptions` class allows you to filter the listings by various criteria. Below are the fields you can set to apply filters:

- `price_min` and `price_max`: Filter tokens based on their price range.
- `market_cap_min` and `market_cap_max`: Filter tokens based on their market capitalization range.
- `volume_24h_min` and `volume_24h_max`: Filter tokens based on their 24-hour trading volume range.
- `circulating_supply_min` and `circulating_supply_max`: Filter tokens based on their circulating supply range.
- `percent_change_24h_min` and `percent_change_24h_max`: Filter tokens based on their 24-hour percent change range.
- `tags`: Filter tokens that have specified tags.

To use the filter options, create an instance of `FilterOptions` and pass it to the `listings_latest` method's `filters` parameter:

```python
from coinmarketcap import Market, FilterOptions

coinmarketcap = Market(api_key="your_api_key")

# Define your filter criteria
filter_options = FilterOptions(
    price_min=0.01,
    price_max=1.00,
    market_cap_min=1000000,
    volume_24h_min=50000,
    tags=['defi', 'smart-contracts']
)

# Fetch listings with the defined filters
tokens = coinmarketcap.listings_latest(filters=filter_options, limit=10)

for token in tokens:
    print(f"{token.name} - {token.symbol}: ${token.quote['USD'].price}")
```

## Using Auxiliary Fields

The `AuxFields` enum allows you to specify additional fields to be included in the response data for each token listing. This can provide more detailed information about each token. Below are the auxiliary fields you can request:

- `NUM_MARKET_PAIRS`: Number of market pairs available for the token.
- `CMC_RANK`: The CoinMarketCap ranking of the token.
- `DATE_ADDED`: The date the token was added to CoinMarketCap.
- `TAGS`: Tags associated with the token.
- `PLATFORM`: The platform on which the token was issued (e.g., Ethereum).
- `MAX_SUPPLY`: The maximum supply of the token.
- `TOTAL_SUPPLY`: The total supply of the token.
- `MARKET_CAP_BY_TOTAL_SUPPLY`: Market cap calculated using the total supply.
- `VOLUME_24H_REPORTED`: Reported 24-hour trading volume.
- `VOLUME_7D`: Trading volume over the last 7 days.
- `VOLUME_7D_REPORTED`: Reported trading volume over the last 7 days.
- `VOLUME_30D`: Trading volume over the last 30 days.
- `VOLUME_30D_REPORTED`: Reported trading volume over the last 30 days.
- `IS_MARKET_CAP_INCLUDED`: Indicates whether the market cap is included in the calculation.

To use these auxiliary fields, pass a list of `AuxFields` to the `listings_latest` method:

```python
from coinmarketcap import Market, SortOption, AuxFields

coinmarketcap = Market(api_key="your_api_key")

# Specify auxiliary fields to include in the response
aux_fields = [
    AuxFields.NUM_MARKET_PAIRS,
    AuxFields.CMC_RANK,
    AuxFields.DATE_ADDED,
    AuxFields.TAGS,
]

tokens = coinmarketcap.listings_latest(
    sort_by=SortOption.MARKET_CAP, 
    aux_fields=aux_fields, 
    limit=5
)

for token in tokens:
    print(f"{token.name} ({token.symbol}) - CMC Rank: {token.cmc_rank}, Market Pairs: {token.num_market_pairs}")
```


## License:

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

```
