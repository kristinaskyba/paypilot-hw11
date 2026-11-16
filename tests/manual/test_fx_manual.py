"""Ручний baseline L11 (крок 1). Пишіть тести тут, асистента не відкривайте.

Модуль під тестом: app/engines/fx.py — функція fx.quote(...).
Очікувані значення беріть із таблиці тарифів app/engines/policy.py,
а не з виводу самої функції.

    fx.quote(amount, from_currency, to_currency, tier, allowance_used_eur=0.0)
    tier: "tier1" | "tier2" | "tier3"
    повертає FxQuote: spread_pct, allowance_applied, gross_amount,
                      spread_amount, final_amount, ...
"""
import pytest

from app.engines import fx, policy


def test_quote_at_allowance_limit_has_no_spread():
    quote = fx.quote(
        amount=100,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
        allowance_used_eur=400,
    )

    assert quote.allowance_applied is True
    assert quote.spread_pct == 0
    assert quote.spread_amount == 0
    assert quote.final_amount == quote.gross_amount


def test_quote_above_allowance_uses_tier_spread():
    quote = fx.quote(
        amount=200,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
        allowance_used_eur=400,
    )

    expected_gross = 200 / policy.RATES_TO_EUR["USD"]
    expected_spread = expected_gross * policy.FX_SPREAD_PCT["tier1"] / 100

    assert quote.allowance_applied is False
    assert quote.spread_pct == policy.FX_SPREAD_PCT["tier1"]
    assert quote.gross_amount == pytest.approx(expected_gross)
    assert quote.spread_amount == pytest.approx(expected_spread)
    assert quote.final_amount == pytest.approx(expected_gross - expected_spread)


def test_quote_with_partial_allowance_charges_only_excess_amount():
    quote = fx.quote(
        amount=200,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
        allowance_used_eur=400,
        partial_allowance=True,
    )

    expected_gross = 200 / policy.RATES_TO_EUR["USD"]

    # EUR 100 remains in the allowance, so only half of the quote is charged.
    expected_spread = expected_gross * 0.5 * policy.FX_SPREAD_PCT["tier1"] / 100

    assert quote.allowance_applied is False
    assert quote.spread_amount == pytest.approx(expected_spread)
    assert quote.final_amount == pytest.approx(expected_gross - expected_spread)


def test_quote_uses_spread_override_above_allowance():
    quote = fx.quote(
        amount=100,
        from_currency="EUR",
        to_currency="USD",
        tier="tier1",
        allowance_used_eur=500,
        spread_pct_override=2.25,
    )

    expected_gross = 100 / policy.RATES_TO_EUR["USD"]
    expected_spread = expected_gross * 2.25 / 100

    assert quote.allowance_applied is False
    assert quote.spread_pct == 2.25
    assert quote.spread_amount == pytest.approx(expected_spread)
    assert quote.final_amount == pytest.approx(expected_gross - expected_spread)


def test_quote_rejects_unknown_tier():
    with pytest.raises(ValueError) as error:
        fx.quote(
            amount=100,
            from_currency="EUR",
            to_currency="USD",
            tier="tier4",
        )

    assert str(error.value) == "Unknown tier: tier4"


def test_quote_rejects_unknown_currency():
    with pytest.raises(ValueError) as error:
        fx.quote(
            amount=100,
            from_currency="SEK",
            to_currency="EUR",
            tier="tier1",
        )

    assert str(error.value) == "Unknown currency: SEK"
