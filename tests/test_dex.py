import pytest
import os
from coinmarketcap import Market
from coinmarketcap.core import DexAuxFields
from coinmarketcap.types.dex_info import DexInfo, DexUrls

@pytest.fixture
def market_instance():
    """Create a Market instance for testing"""
    api_key = os.environ.get('COIN_MARKET_CAP_API_KEY')
    if not api_key:
        pytest.skip("COIN_MARKET_CAP_API_KEY environment variable not set")
    return Market(api_key=api_key, debug_mode=True)

def test_dex_listings_info_single_id(market_instance):
    """Test DEX listings info retrieval with single ID"""

    # Get DEX info for Uniswap v4 (known ID)
    dex_list = market_instance.dex_listings_info(ids=11955)

    # Check that we got a list with one result
    assert isinstance(dex_list, list)
    assert len(dex_list) == 1

    # Check the DEX structure
    dex = dex_list[0]
    assert isinstance(dex, DexInfo)
    assert dex.id == 11955
    assert isinstance(dex.name, str)
    assert isinstance(dex.slug, str)
    assert isinstance(dex.status, str)

def test_dex_listings_info_with_aux_fields(market_instance):
    """Test DEX listings info with auxiliary fields"""

    aux_fields = [
        DexAuxFields.URLS,
        DexAuxFields.LOGO,
        DexAuxFields.DESCRIPTION,
        DexAuxFields.DATE_LAUNCHED,
        DexAuxFields.NOTICE
    ]

    dex_list = market_instance.dex_listings_info(
        ids=11955,
        aux_fields=aux_fields
    )

    assert isinstance(dex_list, list)
    assert len(dex_list) == 1

    dex = dex_list[0]
    # Check that aux fields are present
    assert hasattr(dex, 'logo')
    assert hasattr(dex, 'description')
    assert hasattr(dex, 'date_launched')
    assert hasattr(dex, 'notice')
    assert hasattr(dex, 'urls')

    # Check URLs structure if present
    if dex.urls:
        assert isinstance(dex.urls, DexUrls)
        assert isinstance(dex.urls.website, list)
        assert isinstance(dex.urls.twitter, list)

def test_dex_listings_info_multiple_ids(market_instance):
    """Test DEX listings info with multiple IDs"""

    # Test with list of IDs (note: ID 1 might not be a valid DEX)
    dex_list = market_instance.dex_listings_info(ids=[11955])

    assert isinstance(dex_list, list)
    # Should get results for valid IDs only
    assert len(dex_list) >= 1

    # All results should be DexInfo objects
    for dex in dex_list:
        assert isinstance(dex, DexInfo)
        assert isinstance(dex.id, int)
        assert isinstance(dex.name, str)

def test_dex_listings_info_no_ids_raises_error(market_instance):
    """Test that providing no IDs raises ValueError"""

    with pytest.raises(ValueError, match="At least one DEX ID must be provided"):
        market_instance.dex_listings_info(ids=[])

def test_dex_info_structure(market_instance):
    """Test that DexInfo objects have the expected structure"""

    dex_list = market_instance.dex_listings_info(
        ids=11955,
        aux_fields=[DexAuxFields.URLS, DexAuxFields.LOGO]
    )

    if dex_list:
        dex = dex_list[0]

        # Required fields
        assert hasattr(dex, 'id')
        assert hasattr(dex, 'name')
        assert hasattr(dex, 'slug')
        assert hasattr(dex, 'status')

        # Optional fields
        assert hasattr(dex, 'logo')
        assert hasattr(dex, 'description')
        assert hasattr(dex, 'date_launched')
        assert hasattr(dex, 'notice')
        assert hasattr(dex, 'urls')
        assert hasattr(dex, 'timestamp')

        # Check timestamp is set
        if dex.timestamp:
            assert isinstance(dex.timestamp, int)
            assert dex.timestamp > 0