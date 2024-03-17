import pytest
from datetime import datetime
import os
import time

from coinmarketcap import Market
from coinmarketcap.types.token_state import Quote
from coinmarketcap.v1.cryptocurrency.listings.common import SortOption, AuxFields, SortDir, FilterOptions

@pytest.fixture
def coinmarketcap_instance():
    # You can initialize your CoinMarketCap instance with your API key here if needed
    api_key=API_KEY = os.environ.get('COIN_MARKET_CAP_API_KEY')
    coinmarketcap_instance = Market(api_key=api_key, debug_mode=True)
    yield coinmarketcap_instance


def test_cryptocurrency_quotes_historical(coinmarketcap_instance):
    
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
    assert isinstance(token_state.last_updated, datetime)
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
    assert isinstance(quote.last_updated, datetime)

    # Check the attributes of the BTC quote
    quote = token_state.quote_map['BTC']
    assert isinstance(quote.price, float)
    assert isinstance(quote.volume_24h, float)
    assert isinstance(quote.percent_change_1h, float)
    assert isinstance(quote.percent_change_24h, float)
    assert isinstance(quote.percent_change_7d, float)
    assert isinstance(quote.market_cap, float)
    assert isinstance(quote.last_updated, datetime)


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
    assert token.total_supply is None or isinstance(token.total_supply, float)
    assert token.platform is None or isinstance(token.platform, str)
    assert token.cmc_rank is None or isinstance(token.cmc_rank, int)
    assert token.self_reported_circulating_supply is None or isinstance(token.self_reported_circulating_supply, int)
    assert token.self_reported_market_cap is None or isinstance(token.self_reported_market_cap, float)
    assert token.tvl_ratio is None or isinstance(token.tvl_ratio, float)
    assert token.is_market_cap_included_in_calc is None or isinstance(token.is_market_cap_included_in_calc, bool)
