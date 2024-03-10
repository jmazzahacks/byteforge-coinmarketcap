
from typing import List

from coinmarketcap.types.token_state import TokenState, Quote

def _quotes_historical_v2(market, ticker: str, timestamp_start: int, timestamp_end: int, interval: str = '24h') -> List[TokenState]:

	if timestamp_start > timestamp_end:
		raise ValueError('The start timestamp occurr before than the end timestamp')

	params = {
		'symbol': ticker,
		'time_start': timestamp_start,
		'time_end': timestamp_end,
		'interval': interval
	}
		
	response = market._request('v2/cryptocurrency/quotes/historical', params=params)

	lst_token_states = []

	for ticker in response['data']:

		for dct_ticker_data in response['data'][ticker]:

			lst_quotes = dct_ticker_data['quotes']
			id = dct_ticker_data['id']
			name = dct_ticker_data['name']
			symbol = dct_ticker_data['symbol']
			is_active = dct_ticker_data['is_active']
			is_fiat = dct_ticker_data['is_fiat']
			total_supply = None
			circulating_supply = None

			for quote in lst_quotes:
				base_currency, dct_quote_data = quote['quote'].popitem()
				if 'total_supply' in dct_quote_data:
					total_supply = dct_quote_data.pop('total_supply')
				if 'circulating_supply' in dct_quote_data:
					circulating_supply = dct_quote_data.pop('circulating_supply')

				ts_quote = Quote.from_dict(base_currency, dct_quote_data)
					
				token_state = TokenState(
					id=id, 
					name=name, 
					symbol=symbol, 
					last_updated=ts_quote.last_updated, 
					quote=ts_quote, 
					circulating_supply=circulating_supply, 
					total_supply=total_supply,
					timestamp=int(ts_quote.last_updated.timestamp()),
					is_active=is_active,
					is_fiat=is_fiat)
					
				lst_token_states.append(token_state)

	return lst_token_states

