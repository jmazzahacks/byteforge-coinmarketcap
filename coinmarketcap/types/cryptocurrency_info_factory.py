from typing import Any, Dict, Optional
from dateutil import parser

from crypto_commons.types.cryptocurrency_info import CryptocurrencyInfo
from crypto_commons.types.cryptocurrency_platform import CryptocurrencyPlatform
from crypto_commons.types.cryptocurrency_urls import CryptocurrencyUrls


def _iso_to_unix(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    return int(parser.parse(value).timestamp())


class CryptocurrencyInfoFactory:
    """Builds CryptocurrencyInfo dataclasses from raw CMC API payloads."""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> CryptocurrencyInfo:
        platform = None
        platform_data = data.get('platform')
        if platform_data is not None:
            platform = CryptocurrencyPlatform(
                id=int(platform_data['id']),
                name=platform_data['name'],
                symbol=platform_data['symbol'],
                slug=platform_data['slug'],
                token_address=platform_data['token_address'],
            )

        urls = None
        urls_data = data.get('urls')
        if urls_data is not None:
            urls = CryptocurrencyUrls(
                website=urls_data.get('website') or [],
                technical_doc=urls_data.get('technical_doc') or [],
                explorer=urls_data.get('explorer') or [],
                source_code=urls_data.get('source_code') or [],
                message_board=urls_data.get('message_board') or [],
                chat=urls_data.get('chat') or [],
                announcement=urls_data.get('announcement') or [],
                reddit=urls_data.get('reddit') or [],
                twitter=urls_data.get('twitter') or [],
                facebook=urls_data.get('facebook') or [],
            )

        return CryptocurrencyInfo(
            id=int(data['id']),
            name=data['name'],
            symbol=data['symbol'],
            slug=data['slug'],
            description=data.get('description'),
            category=data.get('category'),
            logo=data.get('logo'),
            date_added=_iso_to_unix(data.get('date_added')),
            date_launched=_iso_to_unix(data.get('date_launched')),
            notice=data.get('notice'),
            tags=data.get('tags') or [],
            platform=platform,
            urls=urls,
        )
