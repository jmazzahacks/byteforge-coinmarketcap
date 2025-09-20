from typing import List, Optional, Union
from enum import Enum
from coinmarketcap.types.dex_info import DexInfo
from coinmarketcap.types.dex_info_factory import DexInfoFactory

class DexAuxFields(Enum):
    URLS = "urls"
    LOGO = "logo"
    DESCRIPTION = "description"
    DATE_LAUNCHED = "date_launched"
    NOTICE = "notice"

def _dex_listings_info(market,
                      ids: Union[int, List[int]],
                      aux_fields: Optional[List[DexAuxFields]] = None) -> List[DexInfo]:
    """
    Get information about specific DEX (Decentralized Exchanges) by their IDs.

    This endpoint requires at least one DEX ID and does not support pagination,
    sorting, or filtering. It returns detailed information about the specified DEXs.

    Args:
        market: The Market instance
        ids: Single DEX ID or list of DEX IDs to retrieve information for
        aux_fields: Additional fields to include (urls, logo, description, date_launched, notice)

    Returns:
        List of DexInfo objects containing DEX information

    Raises:
        ValueError: If no IDs are provided
    """

    if not ids:
        raise ValueError("At least one DEX ID must be provided")

    # Convert single ID to list
    if isinstance(ids, int):
        ids = [ids]

    params = {
        'id': ','.join(map(str, ids))
    }

    if aux_fields:
        aux_field_values = [field.value for field in aux_fields]
        params['aux'] = ','.join(aux_field_values)

    response = market._request('v4/dex/listings/info', params=params, no_cache=True)

    dex_list = []
    for dex_data in response.get('data', []):
        dex_list.append(DexInfoFactory.from_dict(dex_data))

    return dex_list