from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class TokenInfo:
    id: int
    rank: Optional[int]
    name: str
    symbol: str
    slug: str
    is_active: int
    status: int
    first_historical_data: Optional[datetime] = None
    last_historical_data: Optional[datetime] = None
    platform: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'TokenInfo':
        """Create a TokenInfo instance from a dictionary."""
        return cls(
            id=data['id'],
            rank=data.get('rank'),
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            is_active=data['is_active'],
            status=data['status'],
            first_historical_data=datetime.fromisoformat(data['first_historical_data'].replace('Z', '+00:00')) if 'first_historical_data' in data else None,
            last_historical_data=datetime.fromisoformat(data['last_historical_data'].replace('Z', '+00:00')) if 'last_historical_data' in data else None,
            platform=data.get('platform')
        )
