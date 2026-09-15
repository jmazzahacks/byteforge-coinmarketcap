from copy import deepcopy
from dataclasses import asdict
from unittest.mock import Mock

import pytest

from coinmarketcap.types.cryptocurrency_info_factory import CryptocurrencyInfoFactory
from coinmarketcap.v2.cryptocurrency.info import _cryptocurrency_info

ETHEREUM_USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
ZKSYNC_USDC = "0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4"


@pytest.fixture
def usdc_payload():
    # Reduced CMC response from 2026-09-15: zkSync precedes Ethereum.
    return {
        "id": 3408,
        "name": "USDC",
        "symbol": "USDC",
        "slug": "usd-coin",
        "platform": {
            "id": "24091",
            "name": "ZKsync",
            "symbol": "ZK",
            "slug": "zksync",
            "token_address": ZKSYNC_USDC,
        },
        "contract_address": [
            {
                "contract_address": ZKSYNC_USDC,
                "platform": {
                    "name": "zkSync Era",
                    "coin": {
                        "id": "24091",
                        "name": "ZKsync",
                        "symbol": "ZK",
                        "slug": "zksync",
                    },
                },
            },
            {
                "contract_address": ETHEREUM_USDC,
                "platform": {
                    "name": "Ethereum",
                    "coin": {
                        "id": "1027",
                        "name": "Ethereum",
                        "symbol": "ETH",
                        "slug": "ethereum",
                    },
                },
            },
        ],
    }


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("has_platform", [False, True])
def test_contracts_are_independent_of_platform_and_order(
    usdc_payload, reverse, has_platform
):
    if reverse:
        usdc_payload["contract_address"].reverse()
    if not has_platform:
        usdc_payload["platform"] = None
    original = deepcopy(usdc_payload)

    info = CryptocurrencyInfoFactory.from_dict(usdc_payload)

    assert usdc_payload == original
    assert len(info.contract_addresses) == 2
    assert [entry.id for entry in info.contract_addresses] == (
        [1027, 24091] if reverse else [24091, 1027]
    )
    ethereum = next(entry for entry in info.contract_addresses if entry.id == 1027)
    assert asdict(ethereum) == {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "token_address": ETHEREUM_USDC,
    }
    zksync = next(entry for entry in info.contract_addresses if entry.id == 24091)
    assert zksync.name == "ZKsync"  # coin.name, not the display name "zkSync Era"
    assert zksync.token_address == ZKSYNC_USDC  # Preserve address case.
    if has_platform:
        assert asdict(info.platform) == {**original["platform"], "id": 24091}
        assert info.platform is not zksync
    else:
        assert info.platform is None


@pytest.mark.parametrize("array_state", ["missing", "null", "empty"])
@pytest.mark.parametrize("has_platform", [False, True])
def test_unavailable_contracts_are_empty(usdc_payload, array_state, has_platform):
    if array_state == "missing":
        del usdc_payload["contract_address"]
    else:
        usdc_payload["contract_address"] = None if array_state == "null" else []
    if not has_platform:
        usdc_payload["platform"] = None

    info = CryptocurrencyInfoFactory.from_dict(usdc_payload)

    assert info.contract_addresses == []
    if has_platform:
        assert info.platform.token_address == ZKSYNC_USDC
    else:
        assert info.platform is None


@pytest.mark.parametrize("query", [{"ids": [3408]}, {"slugs": ["usd-coin"]}])
def test_info_endpoint_returns_contracts(usdc_payload, query):
    market = Mock()
    market._request.return_value = {"data": {"3408": usdc_payload}}

    result = _cryptocurrency_info(market, **query)

    assert set(result) == {3408}
    ethereum = next(
        entry for entry in result[3408].contract_addresses if entry.id == 1027
    )
    assert ethereum.token_address == ETHEREUM_USDC
