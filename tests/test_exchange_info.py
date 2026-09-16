from copy import deepcopy
from unittest.mock import Mock

import pytest

from coinmarketcap import Market, MalformedResponseError, ServerException
from coinmarketcap.types.exchange_info import ExchangeInfo, ExchangeUrls
from coinmarketcap.types.exchange_info_factory import ExchangeInfoFactory


@pytest.fixture
def exchange_payload():
    # Reduced /v1/exchange/info response from 2026-09-16, with an unknown
    # URL field added to verify compatibility with future API additions.
    return {
        "id": 1348,
        "name": "Uniswap v3 (Ethereum)",
        "slug": "uniswap-v3",
        "logo": "https://s2.coinmarketcap.com/static/img/exchanges/64x64/1348.png",
        "description": "Exchange description",
        "notice": "",
        "status": "active",
        "date_launched": "2021-05-05T00:00:00.000Z",
        "urls": {
            "website": ["https://app.uniswap.org/#/swap"],
            "actual": ["https://example.com/actual"],
            "register": ["https://example.com/register"],
            "twitter": None,
            "future_url": ["https://example.com/new"],
        },
        "countries": [],
        "fiats": ["USD"],
        "tags": [{"name": "DEX", "slug": "dex", "group": "PROPERTY"}],
        "type": "swap",
        "maker_fee": 0,
        "taker_fee": 0.3,
        "weekly_visits": 367742,
        "spot_volume_usd": 444999658.57185924,
        "spot_volume_last_updated": "2026-09-16T06:30:17.168Z",
        "unknown_field": "ignored",
    }


@pytest.fixture
def market():
    client = Market(api_key="offline-test-key")
    client._request = Mock()
    return client


def test_exchange_metadata_preserves_fields_and_does_not_alias_payload(
    exchange_payload,
):
    original = deepcopy(exchange_payload)
    result = ExchangeInfoFactory.from_dict(exchange_payload)

    assert isinstance(result, ExchangeInfo)
    for name in (
        "id",
        "name",
        "slug",
        "logo",
        "description",
        "notice",
        "status",
        "countries",
        "fiats",
        "tags",
        "type",
        "maker_fee",
        "taker_fee",
        "weekly_visits",
        "spot_volume_usd",
    ):
        assert getattr(result, name) == original[name]
    assert result.date_launched == 1620172800
    assert result.spot_volume_last_updated == 1789540217
    assert isinstance(result.timestamp, int) and result.timestamp > 0
    assert isinstance(result.urls, ExchangeUrls)
    assert result.urls.website == original["urls"]["website"]
    assert result.urls.actual == original["urls"]["actual"]
    assert result.urls.register == original["urls"]["register"]
    assert result.urls.twitter == []
    assert result.urls.fee == []

    result.urls.website.append("https://example.com/changed")
    result.fiats.append("EUR")
    result.tags[0]["name"] = "Changed"
    assert exchange_payload == original


@pytest.mark.parametrize("optional", ["missing", "null"])
def test_exchange_optional_fields_and_independent_defaults(optional):
    payload = {"id": "1348", "name": "Uniswap", "slug": "uniswap-v3"}
    if optional == "null":
        payload.update(
            {
                name: None
                for name in (
                    "urls",
                    "countries",
                    "fiats",
                    "tags",
                    "date_launched",
                    "spot_volume_last_updated",
                    "status",
                )
            }
        )
    first = ExchangeInfoFactory.from_dict(payload)
    second = ExchangeInfoFactory.from_dict(payload)
    assert first.id == 1348
    assert first.status is None
    assert first.date_launched is None
    assert first.spot_volume_last_updated is None
    assert first.urls == ExchangeUrls()
    assert first.countries == first.fiats == first.tags == []
    first.urls.website.append("https://example.com")
    first.tags.append({"name": "DEX"})
    assert second.urls.website == second.tags == []


@pytest.mark.parametrize(
    "query, expected",
    [
        ({"ids": 1348}, {"id": "1348"}),
        ({"ids": [1348, 11955]}, {"id": "1348,11955"}),
        ({"slugs": ["uniswap-v3"]}, {"slug": "uniswap-v3"}),
    ],
)
@pytest.mark.parametrize("aux", [None, [], ["urls", "status"]])
def test_exchange_info_selectors_and_aux(
    market, exchange_payload, query, expected, aux
):
    payloads = {"1348": exchange_payload}
    if query.get("ids") == [1348, 11955]:
        payloads["11955"] = {"id": 11955, "name": "Uniswap v4", "slug": "uniswap-v4"}
    expected_ids = {entry["id"] for entry in payloads.values()}
    if "slugs" in query:
        payloads = {entry["slug"]: entry for entry in payloads.values()}
    market._request.return_value = {"data": payloads}

    result = market.exchange_info(**query, aux=aux)

    assert set(result) == expected_ids
    assert all(isinstance(value, ExchangeInfo) for value in result.values())
    assert result[1348].urls.register == exchange_payload["urls"]["register"]
    if aux is not None:
        expected = {**expected, "aux": ",".join(aux)}
    market._request.assert_called_once_with(
        "v1/exchange/info", params=expected, no_cache=True
    )


@pytest.mark.parametrize(
    "query",
    [
        {},
        {"ids": [1348], "slugs": ["uniswap-v3"]},
        {"ids": []},
        {"ids": True},
        {"ids": [0]},
        {"ids": [1348.5]},
        {"ids": "1348"},
        {"slugs": []},
        {"slugs": "uniswap-v3"},
        {"slugs": [""]},
        {"slugs": ["one,two"]},
        {"ids": 1348, "aux": ["invalid"]},
        {"ids": 1348, "aux": "status"},
    ],
)
def test_invalid_exchange_query_fails_before_network(market, query):
    with pytest.raises(ValueError):
        market.exchange_info(**query)
    market._request.assert_not_called()


@pytest.mark.parametrize("payload", [[], {}, {"data": None}, {"data": []}])
def test_missing_exchange_map_is_not_an_empty_success(market, payload):
    market._request.return_value = payload
    with pytest.raises(MalformedResponseError, match="Expected an exchange map"):
        market.exchange_info(ids=1348)


@pytest.mark.parametrize(
    "record",
    [
        None,
        [],
        {"id": 1348},
        {"id": 1348.5, "name": "Uniswap", "slug": "uniswap-v3"},
        {"id": True, "name": "Uniswap", "slug": "uniswap-v3"},
        {"id": 0, "name": "Uniswap", "slug": "uniswap-v3"},
        {"id": 1348, "name": "Uniswap", "slug": "uniswap-v3", "urls": "bad"},
        {"id": 1348, "name": "Uniswap", "slug": "uniswap-v3", "date_launched": "bad"},
    ],
)
def test_malformed_exchange_record_raises_sdk_error(market, record):
    market._request.return_value = {"data": {"uniswap-v3": record}}

    with pytest.raises(
        MalformedResponseError, match="Invalid exchange record"
    ) as error:
        market.exchange_info(slugs=["uniswap-v3"])

    assert error.value.endpoint == "v1/exchange/info"


def test_exchange_http_error_is_preserved_without_fallback(market):
    failure = ServerException(500, "Upstream error")
    market._request.side_effect = failure
    with pytest.raises(ServerException) as error:
        market.exchange_info(ids=1348)
    assert error.value is failure
    market._request.assert_called_once()
