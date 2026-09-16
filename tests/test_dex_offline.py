import json
from unittest.mock import Mock

import pytest
from requests import Response

from coinmarketcap import Market
from coinmarketcap.core import DexAuxFields, ServerException
from coinmarketcap.types.dex_info import DexInfo, DexUrls


@pytest.fixture
def market():
    client = Market(api_key="offline-test-key")
    client._session = Mock()
    client._caching_session = Mock()
    client._caching_session.get.side_effect = AssertionError(
        "DEX metadata must use the uncached session"
    )
    return client


def response(status_code, body):
    result = Response()
    result.status_code = status_code
    result._content = json.dumps(body).encode()
    return result


@pytest.mark.parametrize("ids", [11955, [11955], [11955, 1348]])
@pytest.mark.parametrize("aux_fields", [None, list(DexAuxFields)])
def test_dex_request_and_metadata_conversion(market, ids, aux_fields):
    requested_ids = [ids] if isinstance(ids, int) else ids
    entries = [
        {
            "id": dex_id,
            "name": "Uniswap",
            "slug": "uniswap-v4" if dex_id == 11955 else "uniswap-v3",
            "status": "active",
            "logo": "https://example.com/logo.png",
            "description": "Decentralized exchange metadata fixture",
            "notice": "Test notice",
            "date_launched": "2025-01-31T00:00:00Z",
            "urls": {"website": ["https://app.uniswap.org"], "twitter": []},
        }
        for dex_id in requested_ids
    ]
    market.session.get.return_value = response(200, {"data": entries})

    result = market.dex_listings_info(ids=ids, aux_fields=aux_fields)

    assert [dex.id for dex in result] == requested_ids
    for dex, entry in zip(result, entries):
        assert isinstance(dex, DexInfo)
        assert dex.name == entry["name"]
        assert dex.slug == entry["slug"]
        assert dex.logo == entry["logo"]
        assert dex.description == entry["description"]
        assert dex.notice == entry["notice"]
        assert dex.status == "active"
        assert dex.date_launched == 1738281600
        assert isinstance(dex.timestamp, int) and dex.timestamp > 0
        assert isinstance(dex.urls, DexUrls)
        assert dex.urls.website == ["https://app.uniswap.org"]
        assert dex.urls.twitter == []
        assert dex.urls.fee == []
    params = {"id": ",".join(map(str, requested_ids))}
    if aux_fields:
        params["aux"] = "urls,logo,description,date_launched,notice"
    market.session.get.assert_called_once_with(
        "https://pro-api.coinmarketcap.com/v4/dex/listings/info",
        params=params,
        timeout=market.request_timeout,
    )


@pytest.mark.parametrize("optional_fields", ["missing", "null"])
def test_dex_optional_metadata_can_be_unavailable(market, optional_fields):
    entry = {
        "id": 11955,
        "name": "Uniswap v4 (Ethereum)",
        "slug": "uniswap-v4",
        "status": "active",
    }
    nullable_fields = ("logo", "description", "notice", "date_launched", "urls")
    if optional_fields == "null":
        entry.update({field: None for field in nullable_fields})
    market.session.get.return_value = response(200, {"data": [entry]})

    result = market.dex_listings_info(ids=11955)

    assert len(result) == 1
    dex = result[0]
    assert dex.id == 11955
    assert dex.logo is None
    assert dex.description is None
    assert dex.notice is None
    assert dex.date_launched is None
    assert isinstance(dex.urls, DexUrls)
    assert dex.urls.website == []
    assert dex.urls.twitter == []
    assert dex.urls.blog == []
    assert dex.urls.chat == []
    assert dex.urls.fee == []


def test_dex_empty_ids_fail_without_network(market):
    with pytest.raises(ValueError, match="At least one DEX ID must be provided"):
        market.dex_listings_info(ids=[])
    market.session.get.assert_not_called()


def test_dex_server_error_is_propagated(market):
    # CMC response observed on 2026-09-16; never turn this into empty results.
    market.session.get.return_value = response(
        500,
        {
            "status": {
                "error_code": "500",
                "error_message": "An internal server error occurred.",
            }
        },
    )

    with pytest.raises(
        ServerException, match="An internal server error occurred"
    ) as error:
        market.dex_listings_info(ids=11955)

    assert error.value.status_code == 500
    market.session.get.assert_called_once()
