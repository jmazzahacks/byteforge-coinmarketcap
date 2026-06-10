from typing import Dict, Optional
from dateutil import parser
from crypto_commons.types.token_info import TokenInfo


def _iso_to_unix(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    return int(parser.parse(value).timestamp())


class TokenInfoFactory:
    @staticmethod
    def from_dict(data: Dict) -> 'TokenInfo':
        """Create a TokenInfo instance from a dictionary."""
        return TokenInfo(
            id=data['id'],
            rank=data.get('rank'),
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            is_active=data.get('is_active'),
            status=data.get('status'),
            first_historical_data=_iso_to_unix(data.get('first_historical_data')),
            last_historical_data=_iso_to_unix(data.get('last_historical_data')),
            platform=data.get('platform')
        )