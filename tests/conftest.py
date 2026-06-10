import os

import pytest

from coinmarketcap import Market


@pytest.fixture
def market_instance():
    """Shared Market instance for live-API tests.

    Reads the API key from the COIN_MARKET_CAP_API_KEY environment
    variable. Skips the test if the variable isn't set so the suite
    works in CI without credentials.
    """
    api_key = os.environ.get('COIN_MARKET_CAP_API_KEY')
    if not api_key:
        pytest.skip("COIN_MARKET_CAP_API_KEY environment variable not set")
    return Market(api_key=api_key, debug_mode=True)
