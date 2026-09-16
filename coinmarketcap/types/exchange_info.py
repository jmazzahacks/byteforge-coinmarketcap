from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExchangeUrls:
    """Links returned by /v1/exchange/info, including exchange registration URLs."""

    website: List[str] = field(default_factory=list)
    twitter: List[str] = field(default_factory=list)
    blog: List[str] = field(default_factory=list)
    chat: List[str] = field(default_factory=list)
    fee: List[str] = field(default_factory=list)
    actual: List[str] = field(default_factory=list)
    register: List[str] = field(default_factory=list)


@dataclass
class ExchangeInfo:
    """Metadata for a centralized or decentralized exchange identified by CMC ID.

    Dates and timestamp use Unix seconds. Status is None unless returned by CMC;
    request aux=['status', ...] to include it. Missing URL collections are empty.
    """

    id: int
    name: str
    slug: str
    logo: Optional[str] = None
    description: Optional[str] = None
    date_launched: Optional[int] = None
    notice: Optional[str] = None
    status: Optional[str] = None
    urls: ExchangeUrls = field(default_factory=ExchangeUrls)
    countries: List[str] = field(default_factory=list)
    fiats: List[str] = field(default_factory=list)
    tags: List[Dict[str, Any]] = field(default_factory=list)
    type: Optional[str] = None
    maker_fee: Optional[float] = None
    taker_fee: Optional[float] = None
    weekly_visits: Optional[int] = None
    spot_volume_usd: Optional[float] = None
    spot_volume_last_updated: Optional[int] = None
    timestamp: Optional[int] = None
