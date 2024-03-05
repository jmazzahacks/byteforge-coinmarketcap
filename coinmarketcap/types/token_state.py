from dataclasses import dataclass, field
from typing import List, Optional, Dict
import time
import datetime
import json

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import datetime

from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class Quote:
    base_currency: str
    price: float
    volume_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    market_cap: float
    last_updated: datetime.datetime

    # Now all optional/default parameters follow
    volume_change_24h: float = 0.0
    percent_change_60d: float = 0.0
    percent_change_90d: float = 0.0
    market_cap_dominance: float = 0.0
    fully_diluted_market_cap: float = 0.0
    tvl: Optional[float] = None
    volume_30d: Optional[float] = None
    volume_30d_reported: Optional[float] = None
    volume_24h_reported: Optional[float] = None
    volume_7d_reported: Optional[float] = None
    market_cap_by_total_supply: Optional[float] = None
    volume_7d: Optional[float] = None

    @staticmethod
    def from_dict(currency: str, dct_quote_data: Dict) -> 'Quote':
        
        # Ensure to handle the 'last_updated' conversion properly here
        data = {k: v for k, v in dct_quote_data.items() if k != 'last_updated'}
        last_updated = datetime.datetime.fromisoformat(dct_quote_data.get('last_updated'))
        
        return Quote(base_currency=currency, last_updated=last_updated, **data)


@dataclass
class TokenState:
    id: int
    name: str
    symbol: str
    slug: str
    last_updated: datetime.datetime
    infinite_supply: bool
    quote: Dict[str, Quote]
    num_market_pairs: Optional[int]
    date_added: Optional[datetime.datetime]
    tags: Optional[List[str]]
    max_supply: Optional[int]
    circulating_supply: Optional[int]
    total_supply: Optional[float]
    platform: Optional[str]
    cmc_rank: Optional[int]
    self_reported_circulating_supply: Optional[int]
    self_reported_market_cap: Optional[float]
    tvl_ratio: Optional[float]
    timestamp: int = int(time.time())
    is_market_cap_included_in_calc: Optional[bool] = None


    @staticmethod
    def from_dict(data: Dict) -> 'TokenState':
        data = data.copy()

        # Convert 'is_market_cap_included_in_calc' from 0/1 to False/True
        if 'is_market_cap_included_in_calc' in data:
            data['is_market_cap_included_in_calc'] = bool(data['is_market_cap_included_in_calc'])
            
        data['quote'] = {currency: Quote.from_dict(currency, dct_quote_data) for currency, dct_quote_data in data['quote'].items()}

        # Set optional attributes to None if not present in the data
        optional_fields = [
            'num_market_pairs', 'date_added', 'tags', 'max_supply', 'circulating_supply',
            'total_supply', 'platform', 'cmc_rank', 'self_reported_circulating_supply',
            'self_reported_market_cap', 'tvl_ratio'
        ]
        for attr_name in optional_fields:
            if attr_name not in data:
                data[attr_name] = None

        return TokenState(**data)

