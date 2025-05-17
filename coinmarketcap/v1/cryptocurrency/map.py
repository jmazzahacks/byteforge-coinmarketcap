from coinmarketcap.types.token_info import TokenInfo
from pprint import pprint

def _map(market):

    # quick and dirty test
    params = dict()
    response = market._request('v1/cryptocurrency/map', params=params)
   
    return [TokenInfo.from_dict(item) for item in response['data']]