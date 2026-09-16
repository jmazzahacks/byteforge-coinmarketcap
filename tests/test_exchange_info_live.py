import pytest

from coinmarketcap.types.exchange_info import ExchangeInfo, ExchangeUrls


@pytest.mark.parametrize(
    "query",
    [
        {"ids": [11955, 1348]},
        {"slugs": ["uniswap-v4", "uniswap-v3"]},
    ],
)
def test_exchange_info_live_dex_metadata(market_instance, query):
    exchanges = market_instance.exchange_info(
        **query,
        aux=["urls", "logo", "description", "date_launched", "notice", "status"],
    )

    assert set(exchanges) == {11955, 1348}
    for cmc_id, info in exchanges.items():
        assert isinstance(info, ExchangeInfo)
        assert info.id == cmc_id
        assert info.name
        assert info.slug
        assert info.status in ("active", "inactive")
        assert isinstance(info.urls, ExchangeUrls)
        assert info.urls.website
        assert isinstance(info.urls.actual, list)
        assert isinstance(info.urls.register, list)
        assert info.date_launched is None or isinstance(info.date_launched, int)
        assert isinstance(info.timestamp, int) and info.timestamp > 0


def test_exchange_info_live_cex_defaults(market_instance):
    exchanges = market_instance.exchange_info(ids=270)  # Binance
    assert set(exchanges) == {270}
    info = exchanges[270]
    assert info.id == 270
    assert info.name
    assert info.slug == "binance"
    assert info.logo
    assert info.urls.website
    assert info.status is None or isinstance(info.status, str)
