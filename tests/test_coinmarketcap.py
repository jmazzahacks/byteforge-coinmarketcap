import pytest
import os
import time
from coinmarketcap.v3.cryptocurrency.quotes.historical_v3 import _quotes_historical_v3
from coinmarketcap import Market
from crypto_commons.types.quote import Quote
from coinmarketcap.v1.cryptocurrency.listings.common import SortOption, AuxFields, SortDir, FilterOptions

@pytest.fixture
def coinmarketcap_instance():
    # You can initialize your CoinMarketCap instance with your API key here if needed
    api_key = "***REDACTED***"
    coinmarketcap_instance = Market(api_key=api_key, debug_mode=True)
    yield coinmarketcap_instance



def test_cryptocurrency_quotes_historical_with_id(coinmarketcap_instance):

    timestamp_now = int(time.time())
    timestamp_1_day_ago = timestamp_now - 60*60*24

    # Make the API call
    token_states = coinmarketcap_instance.quotes_historical(
        id="1",
        timestamp_start=timestamp_1_day_ago,
        timestamp_end=timestamp_now,
        interval='1h',
        convert=['USD', 'BTC']
    )

    # Check if the response is a list and contains at least one item
    assert isinstance(token_states, list)
    assert len(token_states) >= 1

    # Check the attributes of the first token state
    token_state = token_states[0]
    assert isinstance(token_state.id, int)
    assert isinstance(token_state.name, str)
    assert isinstance(token_state.symbol, str)
    assert isinstance(token_state.last_updated, int)
    assert isinstance(token_state.timestamp, int)
    assert isinstance(token_state.is_active, bool)
    assert isinstance(token_state.is_fiat, bool)
    assert isinstance(token_state.quote_map, dict)
    assert token_state.tags is None or isinstance(token_state.tags, list)

    # Check the attributes of the USD quote
    quote = token_state.quote_map['USD']
    assert isinstance(quote.price, float)
    assert isinstance(quote.volume_24h, float)
    assert isinstance(quote.percent_change_1h, float)
    assert isinstance(quote.percent_change_24h, float)
    assert isinstance(quote.percent_change_7d, float)
    assert isinstance(quote.market_cap, float)
    assert isinstance(quote.last_updated, int)

    # Check the attributes of the BTC quote
    quote = token_state.quote_map['BTC']
    assert isinstance(quote.price, float)
    assert isinstance(quote.volume_24h, float)
    assert isinstance(quote.percent_change_1h, float)
    assert isinstance(quote.percent_change_24h, float)
    assert isinstance(quote.percent_change_7d, float)
    assert isinstance(quote.market_cap, float)
    assert isinstance(quote.last_updated, int)


def test_cryptocurrency_quotes_historical_with_ticker(coinmarketcap_instance):
    
    timestamp_now = int(time.time())
    timestamp_1_day_ago = timestamp_now - 60*60*24
    
    # Make the API call
    token_states = coinmarketcap_instance.quotes_historical(
        ticker='ETH',
        timestamp_start=timestamp_1_day_ago,
        timestamp_end=timestamp_now,
        interval='1h',
        convert=['USD', 'BTC']
    )

    # Check if the response is a list and contains at least one item
    assert isinstance(token_states, list)
    assert len(token_states) >= 1

    # Check the attributes of the first token state
    token_state = token_states[0]
    assert isinstance(token_state.id, int)
    assert isinstance(token_state.name, str)
    assert isinstance(token_state.symbol, str)
    assert isinstance(token_state.last_updated, int)
    assert isinstance(token_state.timestamp, int)
    assert isinstance(token_state.is_active, bool)
    assert isinstance(token_state.is_fiat, bool)
    assert isinstance(token_state.quote_map, dict)

    # Check the attributes of the USD quote
    quote = token_state.quote_map['USD']
    assert isinstance(quote.price, float)
    assert isinstance(quote.volume_24h, float)
    assert isinstance(quote.percent_change_1h, float)
    assert isinstance(quote.percent_change_24h, float)
    assert isinstance(quote.percent_change_7d, float)
    assert isinstance(quote.market_cap, float)
    assert isinstance(quote.last_updated, int)

    # Check the attributes of the BTC quote
    quote = token_state.quote_map['BTC']
    assert isinstance(quote.price, float)
    assert isinstance(quote.volume_24h, float)
    assert isinstance(quote.percent_change_1h, float)
    assert isinstance(quote.percent_change_24h, float)
    assert isinstance(quote.percent_change_7d, float)
    assert isinstance(quote.market_cap, float)
    assert isinstance(quote.last_updated, int)


def test_listings_latest(coinmarketcap_instance):
    # Define the filter options
    filter = FilterOptions(
        price_min=10,
        price_max=100,
        volume_24h_min=1000000,
        percent_change_24h_min=-5,
        tags=["defi"]
    )

    # Define the aux fields
    aux_fields = [
        AuxFields.NUM_MARKET_PAIRS,
        AuxFields.PLATFORM,
        AuxFields.TOTAL_SUPPLY,
        AuxFields.TAGS,
        AuxFields.VOLUME_30D, 
        AuxFields.CMC_RANK, 
        AuxFields.DATE_ADDED, 
        AuxFields.IS_MARKET_CAP_INCLUDED, 
        AuxFields.MARKET_CAP_BY_TOTAL_SUPPLY, 
        AuxFields.MAX_SUPPLY,
        AuxFields.VOLUME_30D_REPORTED,
        AuxFields.VOLUME_30D, 
        AuxFields.VOLUME_24H_REPORTED, 
        AuxFields.VOLUME_7D,
        AuxFields.VOLUME_7D_REPORTED
    ]

    # Make the API call
    tokens = coinmarketcap_instance.listings_latest(
        sort_by=SortOption.MARKET_CAP,
        sort_dir=SortDir.DESC,
        convert=['USD'],
        limit=1,
        filters=filter,
        aux_fields=aux_fields
    )

    # Check if the response is a list and contains at least one item
    assert isinstance(tokens, list)
    assert len(tokens) >= 1

    # Check the attributes of the first token
    token = tokens[0]
    assert isinstance(token.id, int)
    assert isinstance(token.name, str)
    assert isinstance(token.symbol, str)
    assert isinstance(token.slug, str)
    assert isinstance(token.infinite_supply, bool)
    assert isinstance(token.quote_map, dict)

    # Check optional attributes (can be None)
    assert token.num_market_pairs is None or isinstance(token.num_market_pairs, int)
    assert token.tags is None or isinstance(token.tags, list)
    assert token.max_supply is None or isinstance(token.max_supply, int)
    assert token.circulating_supply is None or isinstance(token.circulating_supply, int)
    assert token.total_supply is None or isinstance(token.total_supply, (int, float))
    assert token.platform is None or isinstance(token.platform, (str, dict))
    assert token.cmc_rank is None or isinstance(token.cmc_rank, int)
    assert token.self_reported_circulating_supply is None or isinstance(token.self_reported_circulating_supply, int)
    assert token.self_reported_market_cap is None or isinstance(token.self_reported_market_cap, float)
    assert token.tvl_ratio is None or isinstance(token.tvl_ratio, float)
    assert token.is_market_cap_included_in_calc is None or isinstance(token.is_market_cap_included_in_calc, bool)

def test_quotes_historical_v3_implementation(coinmarketcap_instance):
    """Test the internal _quotes_historical_v3 implementation directly."""
    from coinmarketcap.v3.cryptocurrency.quotes.historical_v3 import _quotes_historical_v3
    
    timestamp_now = int(time.time())
    timestamp_1_day_ago = timestamp_now - 60*60*24
    
    # Test with ID
    token_states = _quotes_historical_v3(
        market=coinmarketcap_instance,
        id="1",  # Bitcoin
        timestamp_start=timestamp_1_day_ago,
        timestamp_end=timestamp_now,
        interval='hourly',
        convert=['USD', 'BTC']
    )
    
    # Basic validation
    assert isinstance(token_states, list)
    assert len(token_states) > 0
    
    # Check first token state
    first_state = token_states[0]
    assert first_state.id == 1
    assert first_state.name == "Bitcoin"
    assert first_state.symbol == "BTC"
    assert 'USD' in first_state.quote_map
    assert 'BTC' in first_state.quote_map
    
    # Test with ticker
    token_states_ticker = _quotes_historical_v3(
        market=coinmarketcap_instance,
        ticker="ETH",
        timestamp_start=timestamp_1_day_ago,
        timestamp_end=timestamp_now,
        interval='hourly',
        convert=['USD']
    )
    
    # Basic validation for ticker-based query
    assert isinstance(token_states_ticker, list)
    assert len(token_states_ticker) > 0
    
    # Check first token state
    first_ticker_state = token_states_ticker[0]
    assert first_ticker_state.symbol == "ETH"
    assert 'USD' in first_ticker_state.quote_map
    
    # Test error cases
    with pytest.raises(ValueError, match="Either id or ticker must be provided"):
        _quotes_historical_v3(market=coinmarketcap_instance)
    
    with pytest.raises(ValueError, match="The start timestamp occurr before than the end timestamp"):
        _quotes_historical_v3(
            market=coinmarketcap_instance,
            id="1",
            timestamp_start=timestamp_now,
            timestamp_end=timestamp_1_day_ago
        )
    
    with pytest.raises(ValueError, match="The convert list must have a maximum of 3 elements"):
        _quotes_historical_v3(
            market=coinmarketcap_instance,
            id="1",
            convert=['USD', 'BTC', 'EUR', 'JPY']
        )


def test_cryptocurrency_info(coinmarketcap_instance):
    # BTC (id=1) and ETH (id=1027) — both native L1, platform should be None
    info_map = coinmarketcap_instance.cryptocurrency_info(ids=[1, 1027])

    assert isinstance(info_map, dict)
    assert set(info_map.keys()) == {1, 1027}

    btc = info_map[1]
    assert btc.id == 1
    assert btc.symbol == "BTC"
    assert btc.name == "Bitcoin"
    assert btc.platform is None
    assert isinstance(btc.description, str) and len(btc.description) > 0
    assert isinstance(btc.date_added, int)
    assert btc.tags  # established token has tags

    eth = info_map[1027]
    assert eth.symbol == "ETH"
    assert eth.platform is None

    # USDC (id=3408) — ERC-20, platform should be populated with contract address
    usdc_map = coinmarketcap_instance.cryptocurrency_info(ids=[3408])
    usdc = usdc_map[3408]
    assert usdc.platform is not None
    assert usdc.platform.symbol == "ETH"
    assert usdc.platform.token_address.startswith("0x")


def test_cryptocurrency_info_validation(coinmarketcap_instance):
    with pytest.raises(ValueError, match="Exactly one of"):
        coinmarketcap_instance.cryptocurrency_info()

    with pytest.raises(ValueError, match="Exactly one of"):
        coinmarketcap_instance.cryptocurrency_info(ids=[1], slugs=["bitcoin"])

    with pytest.raises(ValueError, match="up to 100 IDs"):
        coinmarketcap_instance.cryptocurrency_info(ids=list(range(101)))


def test_fear_and_greed_historical(coinmarketcap_instance):
    # Regression test for commit 2689a41 — the endpoint was returning 403
    # from CloudFront due to a leading '/' in the request path that produced
    # a double-slashed URL. If this test ever fails with a 403, check the
    # endpoint path in coinmarketcap/v3/fear_and_greed/historical.py.
    data = coinmarketcap_instance.fear_and_greed_historical(start=1, limit=5)

    assert isinstance(data, list)
    assert len(data) == 5

    first = data[0]
    assert isinstance(first, dict)
    assert set(first.keys()) >= {'timestamp', 'value', 'value_classification'}
    assert isinstance(first['value_classification'], str)
    # 'value' is a 0-100 integer; CMC returns it as int
    assert 0 <= int(first['value']) <= 100


def test_map(coinmarketcap_instance):
    # Covers TokenInfoFactory plus the v1/cryptocurrency/map wrapper.
    # Also a regression test for the crypto-commons 0.5 migration: the
    # first_historical_data and last_historical_data fields must be int
    # unix timestamps, not datetime objects.
    tokens = coinmarketcap_instance.map(limit=3)

    assert isinstance(tokens, list)
    assert len(tokens) == 3

    btc = tokens[0]
    assert btc.id == 1
    assert btc.symbol == "BTC"
    assert btc.name == "Bitcoin"
    assert isinstance(btc.slug, str)

    # The crypto-commons 0.5 contract: dates are unix ints.
    assert btc.first_historical_data is None or isinstance(btc.first_historical_data, int)
    assert btc.last_historical_data is None or isinstance(btc.last_historical_data, int)


def test_safe_daily_call_limit(coinmarketcap_instance):
    # Exercises v1/key/info.py via _safe_daily_call_limit. Returns an
    # approximate per-day budget based on remaining monthly quota and
    # days until reset. Value depends on account state; just assert it's
    # a non-negative int.
    daily_limit = coinmarketcap_instance.safe_daily_call_limit()
    assert isinstance(daily_limit, int)
    assert daily_limit >= 0
