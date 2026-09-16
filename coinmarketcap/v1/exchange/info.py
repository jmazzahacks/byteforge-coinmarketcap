from typing import Dict, List, Optional, Union

from coinmarketcap.types.exchange_info import ExchangeInfo
from coinmarketcap.types.exchange_info_factory import ExchangeInfoFactory


def _exchange_info(
    market,
    ids: Optional[Union[int, List[int]]] = None,
    slugs: Optional[List[str]] = None,
    aux: Optional[List[str]] = None,
) -> Dict[int, ExchangeInfo]:
    """Fetch /v1/exchange/info with exactly one nonempty ID or slug selector."""
    if (ids is None) == (slugs is None):
        raise ValueError("Exactly one of ids, slugs must be provided")

    params = {}
    if ids is not None:
        selected_ids = [ids] if isinstance(ids, int) else ids
        if (
            not isinstance(selected_ids, list)
            or not selected_ids
            or any(type(value) is not int or value <= 0 for value in selected_ids)
        ):
            raise ValueError(
                "ids must be a positive integer or a nonempty list of positive integers"
            )
        params["id"] = ",".join(map(str, selected_ids))
    else:
        if (
            not isinstance(slugs, list)
            or not slugs
            or any(
                not isinstance(value, str) or not value.strip() or "," in value
                for value in slugs
            )
        ):
            raise ValueError("slugs must be a nonempty list of exchange slugs")
        params["slug"] = ",".join(slugs)

    if aux is not None:
        allowed_aux = {
            "urls",
            "logo",
            "description",
            "date_launched",
            "notice",
            "status",
        }
        if not isinstance(aux, list) or any(
            not isinstance(value, str) or value not in allowed_aux for value in aux
        ):
            raise ValueError(
                "aux must be a list containing urls, logo, description, date_launched, notice or status"
            )
        params["aux"] = ",".join(aux)

    endpoint = "v1/exchange/info"
    response = market._request(endpoint, params=params, no_cache=True)
    # Imported at call time because core imports this endpoint module.
    from coinmarketcap.core import MalformedResponseError

    raw_data = response.get("data") if isinstance(response, dict) else None
    if not isinstance(raw_data, dict):
        raise MalformedResponseError(endpoint, "Expected an exchange map in 'data'")

    # CMC keys the map by slug for slug queries, and by ID for ID queries.
    # Normalize both modes using each record's own CMC identity.
    result = {}
    for key, exchange in raw_data.items():
        try:
            info = ExchangeInfoFactory.from_dict(exchange)
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise MalformedResponseError(
                endpoint, f"Invalid exchange record {key!r}: {exc}"
            ) from exc
        result[info.id] = info
    return result
