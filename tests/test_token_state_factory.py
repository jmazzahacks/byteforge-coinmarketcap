from copy import deepcopy

import pytest

from coinmarketcap.types.token_state_factory import TokenStateFactory

SUPPLY_FIELDS = (
    "max_supply",
    "circulating_supply",
    "total_supply",
    "self_reported_circulating_supply",
)


@pytest.mark.parametrize("supply_kind", ["fractional", "integer", "null", "missing"])
def test_supply_values_are_preserved(supply_kind):
    payload = {
        "id": 32196,
        "name": "Hyperliquid",
        "symbol": "HYPE",
        "timestamp": 1789539432,
        "quote": {},
    }
    # Maximum, circulating and total supply observed from CMC on 2026-09-16.
    values = (951692037.1891452, 251625911.97511208, 951692037.1891452, 333931719.5)
    if supply_kind == "integer":
        values = tuple(int(value) for value in values)
    elif supply_kind in ("null", "missing"):
        values = (None,) * len(SUPPLY_FIELDS)
    if supply_kind != "missing":
        payload.update(zip(SUPPLY_FIELDS, values))
    original = deepcopy(payload)

    state = TokenStateFactory.from_dict(payload)

    for field, expected in zip(SUPPLY_FIELDS, values):
        actual = getattr(state, field)
        assert actual == expected
        assert type(actual) is type(expected)
    assert payload == original
