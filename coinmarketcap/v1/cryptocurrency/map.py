from coinmarketcap.types.token_info import TokenInfo
from enum import Enum
from pprint import pprint

class ListingStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNTRACKED = "untracked"

def _map(market, 
         status: ListingStatus = ListingStatus.ACTIVE, 
         limit: int = 100):

    # quick and dirty test
    params = dict()
    params['listing_status'] = status.value
    params['limit'] = limit

    response = market._request('v1/cryptocurrency/map', params=params)
   
    return [TokenInfo.from_dict(item) for item in response['data']]