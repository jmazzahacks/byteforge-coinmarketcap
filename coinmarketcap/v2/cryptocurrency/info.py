from typing import Dict, List, Optional

from crypto_commons.types.cryptocurrency_info import CryptocurrencyInfo
from coinmarketcap.types.cryptocurrency_info_factory import CryptocurrencyInfoFactory


def _cryptocurrency_info(
    market,
    ids: Optional[List[int]] = None,
    slugs: Optional[List[str]] = None,
    aux: Optional[List[str]] = None,
) -> Dict[int, CryptocurrencyInfo]:
    """
    Fetch rich token metadata from CMC's /v2/cryptocurrency/info endpoint.

    Returns a dict keyed by CMC ID, with CryptocurrencyInfo values
    containing name, symbol, slug, description, logo, tags, platform
    (with on-chain contract address for cross-chain tokens), and URLs.

    Exactly one of (ids, slugs) must be provided. Batches up to 100 items
    per request — caller chunks if more are needed. Both query modes
    return data keyed by CMC ID.

    Note: CMC's endpoint also accepts symbol= and address= query modes,
    but their response shapes differ (symbol returns lists because of
    ticker collisions); not supported here until there's a consumer.

    Costs 1 credit per call regardless of batch size.
    """
    provided = sum(x is not None for x in (ids, slugs))
    if provided != 1:
        raise ValueError("Exactly one of ids, slugs must be provided")

    params: Dict[str, str] = {}
    if ids is not None:
        if len(ids) > 100:
            raise ValueError("CMC info endpoint accepts up to 100 IDs per call")
        params["id"] = ",".join(str(i) for i in ids)
    elif slugs is not None:
        params["slug"] = ",".join(slugs)

    if aux is not None:
        params["aux"] = ",".join(aux)

    response = market._request("v2/cryptocurrency/info", params=params, no_cache=True)
    raw_data = response.get("data", {})

    result: Dict[int, CryptocurrencyInfo] = {}
    for cmc_id_str, token_data in raw_data.items():
        info = CryptocurrencyInfoFactory.from_dict(token_data)
        result[int(cmc_id_str)] = info
    return result
