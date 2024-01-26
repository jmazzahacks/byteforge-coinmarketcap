import os
import sys
import json
import requests
import tempfile
import requests_cache
from .types.token_state import TokenState
from typing import List
from enum import Enum

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


	# TODO - there are a TON of optional parameters for this endpoint
	# let's start with adding the sort order options.
	def listings(self, sort_by : SortOption = SortOption.MARKET_CAP) -> List[TokenState]:
		"""
		This endpoint displays all active cryptocurrency listings in one call. Use the
		"id" field on the Ticker endpoint to query more information on a specific
		cryptocurrency.
		"""

		params = {'sort': sort_by.value}
		response = self.__request('v1/cryptocurrency/listings/latest', params=params)
		token_states = []
		for token in response['data']:
			token_states.append(TokenState.from_dict(token))

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
