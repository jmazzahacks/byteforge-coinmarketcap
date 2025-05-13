from dataclasses import dataclass, field
from typing import List, Optional, Dict
import time
import datetime
import json
import logging

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import datetime
from dateutil import parser

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
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None


@dataclass
class TokenState:
    id: int
    name: str
    symbol: str
    last_updated: datetime.datetime
    quote_map: Dict[str, Quote]

    timestamp: int = int(time.time())
    infinite_supply: bool = None
    slug: Optional[str] = None
    num_market_pairs: Optional[int] = None
    date_added: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None
    max_supply: Optional[int] = None
    circulating_supply: Optional[int] = None
    total_supply: Optional[float] = None
    platform: Optional[str] = None
    cmc_rank: Optional[int] = None
    self_reported_circulating_supply: Optional[int] = None
    self_reported_market_cap: Optional[float] = None
    tvl_ratio: Optional[float] = None
    is_market_cap_included_in_calc: Optional[bool] = None
    is_active: Optional[bool] = None
    is_fiat: Optional[bool] = None

