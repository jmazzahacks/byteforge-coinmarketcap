from dateutil import parser  
from datetime import datetime, timezone

def _key_info(market):
    """
    Retrieves key configuration and usage information from the market API.

    This function requests the API endpoint associated with key credentials and specific limits
    or configurations that are set for the user's API key, and returns these configuration details.
    
    Parameters:
        market (Market): An instance of the Market class, configured for API access.

    Returns:
        dict: A dictionary containing detailed key configuration information such as API limits.
    """
    dct_response = market._request('v1/key/info', ignore_cache=True)
    return dct_response['data']


def _calls_left_today(market):
    """
    Calculates how many API calls are left for today, based on the service plan's monthly call limit.

    This function takes the user's API call limit and subtracts the number of calls used to date,
    providing a simple ratio to estimate daily available calls until the reset date. Note that 
    this is an approximation based on equal usage each day until the reset.

    Parameters:
        market (Market): An instance of the Market class, which handles the API communications.

    Returns:
        int: Approximate number of API calls left for the current day, based on daily usage 
             till the reset date and a monthly limit.
    """
    dct_response = market._request('v1/key/info', no_cache=True)
    quota_reset_dt = parser.parse(dct_response['data']['plan']['credit_limit_monthly_reset_timestamp'])
    monthly_calls_remaining = dct_response['data']['usage']['current_month']['credits_left']
    
    # Ensure the current datetime is timezone-aware with UTC timezone  
    now_datetime = datetime.now(timezone.utc)

    # Calculate the timedelta  
    time_difference = quota_reset_dt - now_datetime

    # Extract the number of days as an integer  
    number_of_days = time_difference.days

    # Convert daily calls calculation into an integer
    return int(monthly_calls_remaining / number_of_days) if number_of_days > 0 else 0  # Added safety for division
