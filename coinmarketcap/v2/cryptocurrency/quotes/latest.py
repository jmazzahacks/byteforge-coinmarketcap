from typing import List, Optional
import time

from crypto_commons.types.token_state import TokenState
from coinmarketcap.types.token_state_factory import TokenStateFactory


def _quotes_latest(
    market,
    ids: List[int],
    convert: Optional[List[str]] = None,
) -> List[TokenState]:
    """
    Retrieves the latest market quote for one or more cryptocurrencies from the
    CoinMarketCap API v2, looked up by CMC ID.

    Unlike listings_latest, this endpoint returns any token by ID — including
    wrapped tokens (e.g. WBTC, WETH) that CMC excludes from ranked listings.

    Requests are never served from cache: the purpose of this endpoint is a
    fresh spot price, so a stale cached response would silently defeat that.

    Parameters:
            market: The CoinMarketCap API market client instance
            ids (List[int]): CMC IDs of the cryptocurrencies to quote. At least one required.
            convert (List[str]): List of currencies to convert values to (max 3). Default is ['USD'].

    Returns:
            List[TokenState]: A list of TokenState objects, one per requested ID,
                                             each with current quote data in quote_map.

    Raises:
            ValueError: If no IDs are provided or more than 3 conversion currencies are specified.
            ServerException: If the API request fails.
    """
    if not ids:
        raise ValueError("At least one CMC id must be provided")

    if convert is None:
        convert = ["USD"]

    # validate convert
    if len(convert) > 3:
        raise ValueError("The convert list must have a maximum of 3 elements")

    params = {
        "id": ",".join(str(cmc_id) for cmc_id in ids),
        "convert": ",".join(convert),
    }

    # Freshness is the point of this endpoint — bypass the response cache.
    response = market._request(
        "v2/cryptocurrency/quotes/latest", params=params, no_cache=True
    )

    token_states = []
    for dct_token in response["data"].values():
        # Add timestamp if not present (and not expected to be for this API)
        dct_token["timestamp"] = int(time.time())
        token_states.append(TokenStateFactory.from_dict(dct_token))

    return token_states
