import pytest
from datetime import datetime
from coinmarketcap import FilterOptions, SortOption, AuxFields, Market
import os

@pytest.fixture
def coinmarketcap_instance():
    # You can initialize your CoinMarketCap instance with your API key here if needed
    api_key=API_KEY = os.environ.get('COIN_MARKET_CAP_API_KEY')
    coinmarketcap_instance = Market(api_key=api_key, debug_mode=True)
    yield coinmarketcap_instance

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
        sort_dir='desc',
        convert="USD",
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
    assert isinstance(token.quote, dict)

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
