from dataclasses import dataclass, field
from typing import List, Optional, Dict
import datetime

@dataclass
class Quote:
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    percent_change_60d: float
    percent_change_90d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    tvl: Optional[float]
    last_updated: datetime.datetime

    # aux fields
    volume_30d: Optional[float] = None
    volume_30d_reported: Optional[float] = None
    volume_24h_reported: Optional[float] = None
    volume_7d_reported: Optional[float] = None
    market_cap_by_total_supply: Optional[float] = None
    volume_7d: Optional[float] = None

    @staticmethod
    def from_dict(data: Dict) -> 'Quote':
        return Quote(**data)

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
    is_market_cap_included_in_calc: Optional[bool]

    @staticmethod
    def from_dict(data: Dict) -> 'TokenState':
        data = data.copy()

        # Convert 'is_market_cap_included_in_calc' from 0/1 to False/True
        if 'is_market_cap_included_in_calc' in data:
            data['is_market_cap_included_in_calc'] = bool(data['is_market_cap_included_in_calc'])

        data['quote'] = {k: Quote.from_dict(v) for k, v in data['quote'].items()}

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

