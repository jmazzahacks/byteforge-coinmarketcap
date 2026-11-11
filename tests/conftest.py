import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from coinmarketcap import Market

REPO_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(REPO_ROOT / '.env')


@pytest.fixture
def market_instance() -> Market:
    """Shared Market instance for live-API tests.

    Reads COIN_MARKET_CAP_API_KEY from the repo-root .env file (see
    example.env). Skips the test if the key isn't set so the suite
    works in CI without credentials.
    """
    api_key = os.environ.get('COIN_MARKET_CAP_API_KEY')
    if not api_key:
        pytest.skip("COIN_MARKET_CAP_API_KEY not set in .env")
    return Market(api_key=api_key, debug_mode=True)
