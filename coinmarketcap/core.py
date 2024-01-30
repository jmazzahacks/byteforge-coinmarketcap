import os
import sys
import json
import requests
import tempfile
import requests_cache
from .types.token_state import TokenState
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass

@dataclass
class FilterOptions:
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    market_cap_min: Optional[float] = None
    market_cap_max: Optional[float] = None
    volume_24h_min: Optional[float] = None
    volume_24h_max: Optional[float] = None
    circulating_supply_min: Optional[float] = None
    circulating_supply_max: Optional[float] = None
    percent_change_24h_min: Optional[float] = None
    percent_change_24h_max: Optional[float] = None
    tags: Optional[List[str]] = None


class AuxFields(Enum):
    NUM_MARKET_PAIRS = "num_market_pairs"
    CMC_RANK = "cmc_rank"
    DATE_ADDED = "date_added"
    TAGS = "tags"
    PLATFORM = "platform"
    MAX_SUPPLY = "max_supply"
    TOTAL_SUPPLY = "total_supply"
    MARKET_CAP_BY_TOTAL_SUPPLY = "market_cap_by_total_supply"
    VOLUME_24H_REPORTED = "volume_24h_reported"
    VOLUME_7D = "volume_7d"
    VOLUME_7D_REPORTED = "volume_7d_reported"
    VOLUME_30D = "volume_30d"
    VOLUME_30D_REPORTED = "volume_30d_reported"
    IS_MARKET_CAP_INCLUDED = "is_market_cap_included_in_calc"


class SortOption(Enum):
    MARKET_CAP = "market_cap"
    MARKET_CAP_STRICT = "market_cap_strict"
    NAME = "name"
    SYMBOL = "symbol"
    DATE_ADDED = "date_added"
    PRICE = "price"
    CIRCULATING_SUPPLY = "circulating_supply"
    TOTAL_SUPPLY = "total_supply"
    MAX_SUPPLY = "max_supply"
    NUM_MARKET_PAIRS = "num_market_pairs"
    MARKET_CAP_BY_TOTAL_SUPPLY_STRICT = "market_cap_by_total_supply_strict"
    VOLUME_24H = "volume_24h"
    VOLUME_7D = "volume_7d"
    VOLUME_30D = "volume_30d"
    PERCENT_CHANGE_1H = "percent_change_1h"
    PERCENT_CHANGE_24H = "percent_change_24h"
    PERCENT_CHANGE_7D = "percent_change_7d"


class Market(object):

	_session = None
	_debug_mode = False
	_api_key = None
	__DEFAULT_BASE_URL = 'https://pro-api.coinmarketcap.com/'
	__DEFAULT_TIMEOUT = 30
	__TEMPDIR_CACHE = True

	def __init__(self, api_key = None, base_url = __DEFAULT_BASE_URL, request_timeout = __DEFAULT_TIMEOUT, tempdir_cache = __TEMPDIR_CACHE, debug_mode = False):
		self._api_key = api_key
		self.base_url = base_url
		self.request_timeout = request_timeout
		self._debug_mode = debug_mode
		self.cache_filename = 'coinmarketcap_cache'
		self.cache_name = os.path.join(tempfile.gettempdir(), self.cache_filename) if tempdir_cache else self.cache_filename
		if not self._api_key:
			raise ValueError('An API key is required for using the coinmarketcap API. Please visit https://pro.coinmarketcap.com/signup/ for more information.')


	@property
	def session(self):
		if not self._session:
			self._session = requests_cache.CachedSession(cache_name=self.cache_name, backend='sqlite', expire_after=120)
			self._session.headers.update({
					'Accept': 'application/json',
				  	'X-CMC_PRO_API_KEY': self._api_key,
				})
		return self._session
	

	def __request(self, endpoint, params = {}):
		if self._debug_mode:
			print('Request URL: ' + self.base_url + endpoint)
			if params:
				print("Request Payload:\n" + json.dumps(params, indent=4))

		try:
			response_object = self.session.get(self.base_url + endpoint, params = params, timeout = self.request_timeout)
			
			if self._debug_mode:
				print('Response Code: ' + str(response_object.status_code))
				print('From Cache?: ' + str(response_object.from_cache))
				print("Response Payload:\n" + json.dumps(response_object.json(), indent=4))

			if response_object.status_code == requests.codes.ok:
				return response_object.json()
			else:
				raise Exception(f"Server returned {response_object.status_code} - {response_object.text}")
		except Exception as e:
			raise e


	def listings_latest(self, sort_by: SortOption = SortOption.MARKET_CAP, sort_dir: str = 'desc', start: int = 1, limit: int = 100, convert: str = None, aux_fields: AuxFields = None, filters: FilterOptions = None) -> List[TokenState]:
		
		if sort_dir not in ['asc', 'desc']:
			raise ValueError("sort_dir must be 'asc' or 'desc'")

		params = {
			'sort': sort_by.value,
			'sort_dir': sort_dir,
			'start': start,
			'limit': limit
		}
		
		if convert:
			params['convert'] = convert

		if aux_fields:
			# Include the "aux" fields in the params
			aux_field_values = [field.value for field in aux_fields]
			params['aux'] = ','.join(aux_field_values)

		if filters:
			if filters.price_min is not None:
				params['price_min'] = filters.price_min
			if filters.price_max is not None:
				params['price_max'] = filters.price_max
			if filters.market_cap_min is not None:
				params['market_cap_min'] = filters.market_cap_min
			if filters.market_cap_max is not None:
				params['market_cap_max'] = filters.market_cap_max
			if filters.volume_24h_min is not None:
				params['volume_24h_min'] = filters.volume_24h_min
			if filters.volume_24h_max is not None:
				params['volume_24h_max'] = filters.volume_24h_max
			if filters.circulating_supply_min is not None:
				params['circulating_supply_min'] = filters.circulating_supply_min
			if filters.circulating_supply_max is not None:
				params['circulating_supply_max'] = filters.circulating_supply_max
			if filters.percent_change_24h_min is not None:
				params['percent_change_24h_min'] = filters.percent_change_24h_min
			if filters.percent_change_24h_max is not None:
				params['percent_change_24h_max'] = filters.percent_change_24h_max
			if filters.tags:
				params['tag'] = ','.join(filters.tags)

		response = self.__request('v1/cryptocurrency/listings/latest', params=params)
		token_states = [TokenState.from_dict(token) for token in response['data']]

		return token_states


	# TODO - this should call global metrics endpoint
	def stats(self, **kwargs):
		"""
		This endpoint displays the global data found at the top of coinmarketcap.com.

		Optional parameters:
		(string) convert - return pricing info in terms of another currency.
		Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
		"DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN",
		"MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY",
		"TWD", "ZAR"
		Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"
		"""

		params = {}
		params.update(kwargs)
		response = self.__request('global/', params)
		return response
