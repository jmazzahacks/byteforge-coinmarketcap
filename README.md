# About This Project

This project is a fork of Martin Simon's 'coinmarketcap' module, which had not been updated for a long while ([original repository](https://github.com/barnumbirr/coinmarketcap)). This version has been extensively reworked to be compatible with the current CoinMarketCap API, diverging significantly from the original source. As a result, it is not backwards compatible, but it brings new capabilities and improvements tailored to the current API's structure and requirements.

This project currently supports the following CoinMarketCap API endpoints:

- `v1/cryptocurrency/listings/latest`: Get the latest market data for all cryptocurrencies
- `v1/cryptocurrency/map`: Get a mapping of all cryptocurrencies to their CoinMarketCap IDs
- `v2/cryptocurrency/quotes/historical`: Get historical quotes for cryptocurrencies (requires Hobbyist tier or higher)
- `v3/cryptocurrency/quotes/historical`: Get historical quotes for cryptocurrencies with enhanced features (requires Hobbyist tier or higher)

The `listings_latest` and `map` endpoints are available with a free API key from CoinMarketCap. Obtain your free API key by signing up at [CoinMarketCap API](https://pro.coinmarketcap.com/signup/). 

## Prerequisites

- An API key from [CoinMarketCap Pro](https://pro.coinmarketcap.com/signup/).

## Installation

Install byteforge-coinmarketcap

```bash
pip install byteforge-coinmarketcap
```

## Initialization

First, create an instance of the `Market` class with your API key:

```python
from coinmarketcap import Market
from coinmarketcap import SortOption

API_KEY = 'your_api_key_here'
coinmarketcap = Market(api_key=API_KEY)
```

CMC's API has rate limits, and will throttle you if you exceed them. If you know what your rate limit is (and you should!) you can initialize the engine with the appropriate value as follows.

```python
coinmarketcap = Market(api_key=API_KEY, rate_limit_per_minute=30)
```

## General Instructions

This SDK is crafted to fetch market data at specific points in time, offering a comprehensive snapshot of cryptocurrency metrics. Each method returns a list of `TokenState` objects, encapsulating detailed quotes for a cryptocurrency asset corresponding to particular timestamps. The `TokenState` object can include multiple quotes for the asset. For additional information, refer to the usage examples provided. 


## Usage: API listings_latest

Get the top 5 token states by market cap (A TokenState is a snapshot of a token at a certain point of time, for listings_latest, that time will always be "now")

### Simple Usage

```python
token_states = coinmarketcap.listings_latest(sort_by=SortOption.MARKET_CAP, limit=5)

for token in tokens:
    print(token.name, token.symbol, token.quote_map['USD'].price)

# Bitcoin BTC 51121.78037849647
# Ethereum ETH 2912.0337516792188
# Tether USDt USDT 0.9996898483447065
# BNB BNB 369.2725354702457
# Solana SOL 103.68827889524766
```
### The `convert` parameter

The `convert` parameter enhances your ability to receive cryptocurrency quotes in multiple currencies simultaneously. This feature is especially useful for comparing market values across different fiat and cryptocurrencies, allowing up to three currency conversions in a single request.

**Please Note:** You'll need a hobbyist account or higher to do more than one conversion at a time.

Here's how you can retrieve the latest listings and obtain quotes in USD and BTC for the top 5 cryptocurrencies by market capitalization:

```python
# Fetch listings with market cap sort, limited to the top 5, converting quotes to USD and BTC
tokens = coinmarketcap.listings_latest(sort_by=SortOption.MARKET_CAP, limit=5, convert=['USD', 'BTC'])

# Iterate through each token to display its name, symbol, and quotes in BTC and USD
for token in tokens:
   btc_price = token.quote_map['BTC'].price
   usd_price = token.quote_map['USD'].price
   print(f"{token.name} ({token.symbol}): {btc_price} BTC | {usd_price} USD")

# Example output:
Bitcoin (BTC): 1 BTC | 67393.03455553834 USD
Ethereum (ETH): 0.052078986669438124 BTC | 3509.760948230864 USD
Tether USDt (USDT): 1.4836675143579e-05 BTC | 0.9998885606405162 USD
Solana (SOL): 0.002940752776384911 BTC | 198.1862534782036 USD
BNB (BNB): 0.008168244957149958 BTC | 550.4828146553089 USD
```

### The `SortOption` parameter

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

### The `FilterOptions` parameter

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
    print(f"{token.name} - {token.symbol}: ${token.quote_map['USD'].price}")
```

### The `AuxFields` paramater

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

## Usage: API quotes_historical


The `quotes_historical` method facilitates fetching historical quotes for a specific cryptocurrency over a given time range. This feature allows for detailed analysis of cryptocurrency value trends over time in different fiat or cryptocurrencies.  You can query either directly by ticker using the ```ticker``` paramater or using the ```id``` parameter and supply the coinmarketcap id (cmc_id).  Using the cmd_id can avoid edge cases when multiple assets share the same ticker.

This API requires a 'Hobbyist' or higher tier CMC subscription.

### Example Usage

```python
from byteforge_coinmarketcap import Market
from datetime import datetime

coinmarketcap = Market(api_key='your_api_key')

historical_quotes = coinmarketcap.quotes_historical(
    ticker='BTC',
    timestamp_start=1709269200,
    timestamp_end=1710046800,
    interval='daily',
    convert=['USD', 'EUR']
)

for token_state in historical_quotes:
    print(f"{token_state.name} ({token_state.symbol}) - Date: {datetime.fromtimestamp(token_state.timestamp)}")
    for currency, quote in token_state.quote_map.items():
        print(f"  {currency}: {quote.price}")
        
# Example output
# Bitcoin (BTC) - Date: 2024-03-01 19:00:00
#  EUR: 57565.10517077225
#  USD: 62431.65248172238
# Bitcoin (BTC) - Date: 2024-03-02 19:00:00
#  EUR: 57196.216977007156
#  USD: 62031.57852286433
# Bitcoin (BTC) - Date: 2024-03-03 19:00:00
#  EUR: 58233.4060759458
#  USD: 63137.00468154272
# Bitcoin (BTC) - Date: 2024-03-04 19:00:00
#  EUR: 62964.80344823259
#  USD: 68341.05778181224        
```

### Interval Parameter Options

When fetching historical quotes, you can specify the `interval` parameter to determine the granularity of the time series data. There are two types of interval formats you can use:

### Calendar Intervals (UTC Time)
- `hourly`: Retrieves the first quote available at the beginning of each calendar hour.
- `daily`: Retrieves the first quote available at the beginning of each calendar day.
- `weekly`: Retrieves the first quote available at the beginning of each calendar week.
- `monthly`: Retrieves the first quote available at the beginning of each calendar month.
- `yearly`: Retrieves the first quote available at the beginning of each calendar year.

### Relative Time Intervals
- `m`: Retrieves a quote available every "m" minutes. Supported intervals: `5m`, `10m`, `15m`, `30m`, `45m`.
- `h`: Retrieves a quote available every "h" hours. Supported intervals: `1h`, `2h`, `3h`, `4h`, `6h`, `12h`.
- `d`: Retrieves a quote available every "d" days. Supported intervals: `1d`, `2d`, `3d`, `7d`, `14d`, `15d`, `30d`, `60d`, `90d`, `365d`.

Please ensure to select the interval that best matches your data analysis needs.

## Usage: API map

The `map` endpoint provides a mapping of all cryptocurrencies to their CoinMarketCap IDs, which is essential for making other API calls. This endpoint is particularly useful for obtaining basic information about cryptocurrencies and their identifiers.

### Basic Usage

```python
from coinmarketcap import Market, ListingStatus, MapSortOption, MapAuxFields

coinmarketcap = Market(api_key='your_api_key')

# Get basic mapping of active cryptocurrencies
token_infos = coinmarketcap.map(
    listing_status=ListingStatus.ACTIVE,
    limit=5
)

for token in token_infos:
    print(f"{token.name} ({token.symbol}) - ID: {token.id}")

# Example output:
# Bitcoin (BTC) - ID: 1
# Ethereum (ETH) - ID: 1027
# Tether USDt (USDT) - ID: 825
# BNB (BNB) - ID: 1839
# Solana (SOL) - ID: 5426
```

### Advanced Usage with Filters and Additional Fields

```python
# Get detailed mapping with additional fields
token_infos = coinmarketcap.map(
    listing_status=ListingStatus.ACTIVE,
    symbols=['BTC', 'ETH', 'SOL'],
    sort=MapSortOption.CMC_RANK,
    aux_fields=[
        MapAuxFields.PLATFORM,
        MapAuxFields.FIRST_HISTORICAL_DATA,
        MapAuxFields.LAST_HISTORICAL_DATA,
        MapAuxFields.IS_ACTIVE
    ]
)

for token in token_infos:
    print(f"{token.name} ({token.symbol})")
    print(f"  ID: {token.id}")
    print(f"  Platform: {token.platform}")
    print(f"  First Historical Data: {token.first_historical_data}")
    print(f"  Last Historical Data: {token.last_historical_data}")
    print(f"  Is Active: {token.is_active}")
```

### Parameters

- `listing_status` (ListingStatus): Filter by listing status
  - `ACTIVE`: Only active cryptocurrencies
  - `INACTIVE`: Only inactive cryptocurrencies
  - `UNTRACKED`: Only untracked cryptocurrencies

- `start` (int): Starting point for pagination (default: 1)

- `limit` (int): Number of results to return (default: 100)

- `symbols` (List[str]): List of cryptocurrency symbols to filter by

- `sort` (MapSortOption): Field to sort results by
  - `ID`: Sort by CoinMarketCap ID
  - `CMC_RANK`: Sort by CoinMarketCap rank

- `aux_fields` (List[MapAuxFields]): Additional fields to include in response
  - `PLATFORM`: Platform information
  - `FIRST_HISTORICAL_DATA`: First historical data timestamp
  - `LAST_HISTORICAL_DATA`: Last historical data timestamp
  - `IS_ACTIVE`: Active status

## Usage: API fear_and_greed_historical

The `fear_and_greed_historical` endpoint provides access to the historical Fear & Greed Index data from CoinMarketCap. This index is a market sentiment indicator that helps gauge whether the market is being driven by fear or greed.

### Basic Usage

```python
from coinmarketcap import Market

coinmarketcap = Market(api_key='your_api_key')

# Get historical fear and greed index data
fear_greed_data = coinmarketcap.fear_and_greed_historical(
    start=1,  # Starting point for pagination
    limit=10  # Number of results to return
)

for entry in fear_greed_data:
    print(f"Timestamp: {entry['timestamp']}")
    print(f"Value: {entry['value']}")
    print(f"Classification: {entry['value_classification']}")
    print("---")

# Example output:
# Timestamp: 1748131200
# Value: 67
# Classification: Greed
# ---
# Timestamp: 1748044800
# Value: 67
# Classification: Greed
# ---
```

### Parameters

- `start` (int): Starting point for pagination (default: 1)
- `limit` (int): Number of results to return (default: 500)

### Return Value

The method returns a list of dictionaries, where each dictionary contains:
- `timestamp` (str): Unix timestamp of the measurement
- `value` (int): The fear and greed index value (0-100)
- `value_classification` (str): Classification of the value (e.g., 'Greed', 'Fear', etc.)

The Fear & Greed Index ranges from 0 to 100:
- 0-24: Extreme Fear
- 25-49: Fear
- 50: Neutral
- 51-74: Greed
- 75-100: Extreme Greed

## Monitoring API Usage

As you utilize the API, it's important to manage the number of requests to stay within your plan's limits. The `safe_daily_call_limit` function provides an easy way to verify your daily API limits against your monthly call budget.

### Purpose

The `safe_daily_call_limit` method estimates the number of API calls you can make during the current day without exceeding your monthly limit. This is crucial for applications that need to manage request rates or distribute API calls evenly throughout a billing period.

### Usage

2. **Call the `safe_daily_call_limit` Method**:
   Use the `safe_daily_call_limit` method to find out how many API calls you can safely make per day without exhausting your quota.  It's up to you to store a counter for this and track your daily usage.  The SDK call is stateless and just uses some simple math to determine this value.

```python
safe_calls_per_day = coinmarkectap.safe_daily_call_limit()
print(f"You can safely make {safe_calls_per_day} calls per day.")
```

### Note

- **Accuracy**: Please note that this function provides an approximation. If your daily API call volume varies significantly, consider implementing more detailed tracking mechanisms.
- **Reset Timing**: Be aware of your API subscription details, especially when the monthly call count resets, as this will affect the calculations.


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
