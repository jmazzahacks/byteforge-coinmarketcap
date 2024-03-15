import os
import sys
import json
import requests
import tempfile
import requests_cache
from typing import List

from .types.token_state import TokenState, Quote
from .v2.cryptocurrency.quotes.historical import _quotes_historical_v2
from .v1.cryptocurrency.listings.latest import _listings_latest
from .v1.cryptocurrency.listings.common import SortOption, AuxFields, SortDir, FilterOptions

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
	

	def _request(self, endpoint, params = {}):
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

	def quotes_historical(self,
					   ticker: str,
					   timestamp_start: int,
					   timestamp_end: int,
					   interval: str = '24h',
					   convert: List[str] = ['USD']) -> List[TokenState]:
		
		return _quotes_historical_v2(self, ticker, timestamp_start, timestamp_end, interval, convert)

	def listings_latest(self, sort_by: SortOption = SortOption.MARKET_CAP, 
					sort_dir: SortDir = SortDir.DESC, 
					start: int = 1, 
					limit: int = 100, 
					convert: List[str] = ['USD'],
					aux_fields: AuxFields = None, 
					filters: FilterOptions = None) -> List[TokenState]:
		
		return _listings_latest(self, sort_by, sort_dir, start, limit, convert, aux_fields, filters)


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
		response = self._request('global/', params)
		return response
