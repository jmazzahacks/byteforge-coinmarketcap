from copy import deepcopy
from dataclasses import fields
import time
from typing import Any, Dict

from dateutil import parser

from .exchange_info import ExchangeInfo, ExchangeUrls


class ExchangeInfoFactory:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> ExchangeInfo:
        """Parse exchange metadata without mutating or aliasing the API payload."""
        if not isinstance(data, dict):
            raise ValueError("Expected an exchange object")
        raw_id = data["id"]
        if type(raw_id) not in (int, str):
            raise ValueError("Exchange ID must be a positive integer")
        cmc_id = int(raw_id)
        if cmc_id <= 0:
            raise ValueError("Exchange ID must be a positive integer")
        known_fields = {field.name for field in fields(ExchangeInfo)}
        values = {
            key: deepcopy(value) for key, value in data.items() if key in known_fields
        }
        values["id"] = cmc_id
        values["timestamp"] = int(time.time())
        for name in ("date_launched", "spot_volume_last_updated"):
            if isinstance(values.get(name), str):
                values[name] = int(parser.parse(values[name]).timestamp())
        for name in ("countries", "fiats", "tags"):
            values[name] = values.get(name) or []

        raw_urls = values.get("urls")
        if raw_urls is None:
            raw_urls = {}
        if not isinstance(raw_urls, dict):
            raise ValueError("Expected a URL object or null")
        values["urls"] = ExchangeUrls(
            **{
                field.name: raw_urls.get(field.name) or []
                for field in fields(ExchangeUrls)
            }
        )
        return ExchangeInfo(**values)
