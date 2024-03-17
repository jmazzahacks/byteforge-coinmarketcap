
from typing import Optional, List
import json
from dateutil import parser
import time
from pprint import pprint

from coinmarketcap.types.token_state import TokenState, Quote

def _validate_interval(interval: str) -> None:
    # Define allowed calendar year and time constants
    calendar_intervals = {"hourly", "daily", "weekly", "monthly", "yearly"}

    # Define allowed relative time intervals
    relative_intervals = {
        "5m", "10m", "15m", "30m", "45m",
        "1h", "2h", "3h", "4h", "6h", "12h",
        "1d", "2d", "3d", "7d", "14d", "15d", "30d", "60d", "90d", "365d"
    }

    # Check if the interval is in one of the allowed sets
    if interval not in calendar_intervals and interval not in relative_intervals:
        # If not, raise a ValueError with a message about the invalid interval
        raise ValueError(f"Invalid interval: '{interval}'. Please provide a valid interval.")


def _quotes_historical_v2(market, 
						  ticker: str, 
						  timestamp_start: Optional[int], 
						  timestamp_end: Optional[int],
						  interval: str = 'hourly',
						  convert: List[str] = ['USD']) -> List[TokenState]:

	# Check if the start timestamp is greater than the end timestamp
	if timestamp_start > timestamp_end:
		raise ValueError('The start timestamp occurr before than the end timestamp')

	# Check if the interval is valid
	_validate_interval(interval)

	# validate convert
	if (len(convert) > 3):
		raise ValueError('The convert list must have a maximum of 3 elements')

	params = {
		'symbol': ticker,
		'time_start': timestamp_start,
		'time_end': timestamp_end,
		'interval': interval,
		'convert': ','.join(convert)
	}
		
	response = market._request('v2/cryptocurrency/quotes/historical', params=params)

	lst_token_states = []

	# weird structure, we have to drill down into the quotes object for our ticker,
	# we call this the quote summary because it's the quotes, plus some extra
	# meta data we can extract for the TokenState object
	dct_quote_summary = response['data'][ticker][0]

	# and we also get some general meta-data that can go into the TokenState object
	id = dct_quote_summary['id']
	name = dct_quote_summary['name']
	symbol = dct_quote_summary['symbol']
	is_active = dct_quote_summary['is_active'] == 1
	is_fiat = dct_quote_summary['is_fiat'] == 1

	# and the quotes themselves, still wrapped up in a list of convoluted stuff
	lst_quotes = dct_quote_summary['quotes']

	# for each quote block, we can create a token state
	for dct_quote_block in lst_quotes:

		# Parse the timestamp string into a datetime object
		timestamp_dt = parser.parse(dct_quote_block['timestamp'])

		# create a token state, the quotes are empty for now
		token_state = TokenState(
			id=id,
			name=name,
			symbol=symbol,
			last_updated=timestamp_dt,
			timestamp=int(timestamp_dt.timestamp()),
			is_active=is_active,
			quote_map={},
			is_fiat=is_fiat)

		# init each quote object and add it to the tokenstate
		for base_currency, dct_quote_data in dct_quote_block['quote'].items():
			quote = Quote.from_dict(base_currency, dct_quote_data)
			token_state.quote_map[base_currency] = quote
					
		lst_token_states.append(token_state)

	return lst_token_states
