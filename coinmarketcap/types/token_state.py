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

    @staticmethod
    def from_dict(data: Dict) -> 'Quote':
        return Quote(**data)

@dataclass
class TokenState:
    id: int
    name: str
    symbol: str
    slug: str
    num_market_pairs: int
    date_added: datetime.datetime
    tags: List[str]
    max_supply: int
    circulating_supply: int
    total_supply: int
    infinite_supply: bool
    platform: Optional[str]
    cmc_rank: int
    self_reported_circulating_supply: Optional[int]
    self_reported_market_cap: Optional[float]
    tvl_ratio: Optional[float]
    last_updated: datetime.datetime
    quote: Dict[str, Quote]

    @staticmethod
    def from_dict(data: Dict) -> 'TokenState':
        data = data.copy()
        data['quote'] = {k: Quote.from_dict(v) for k, v in data['quote'].items()}
        return TokenState(**data)

