from coinmarketcap.types.token_info import TokenInfo
from enum import Enum
from typing import List
from pprint import pprint

class ListingStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNTRACKED = "untracked"

class MapSortOption(Enum):
    ID = "id"
    CMC_RANK = "cmc_rank"

def _map(market, 
         status: ListingStatus = ListingStatus.ACTIVE, 
         start: int = 1,
         limit: int = 100,
         symbols: List[str] = None,
         sort: MapSortOption = MapSortOption.ID):

    # quick and dirty test
    params = dict()
    params['listing_status'] = status.value
    params['start'] = start
    params['limit'] = limit
    params['sort'] = sort.value
    if symbols:
        params['symbol'] = ','.join(symbols)

    response = market._request('v1/cryptocurrency/map', params=params)
   
    return [TokenInfo.from_dict(item) for item in response['data']]