"""Згенеровані unit-тести для app/engines/fx.py.

Константи policy підміняються фікстурою, тож тести не залежать від
реальних тарифів. Припущення: policy.to_eur(amount, cur) == amount * RATES_TO_EUR[cur].
"""
import pytest

from app.engines import fx, policy


@pytest.fixture(autouse=True)
def fake_policy(monkeypatch):
    monkeypatch.setattr(policy, "RATES_TO_EUR",
                        {"EUR": 1.0, "USD": 0.5, "GBP": 2.0})
    monkeypatch.setattr(policy, "TIERS", ["basic", "premium"])
    monkeypatch.setattr(policy, "FX_FREE_MONTHLY_ALLOWANCE_EUR",
                        {"basic": 100.0, "premium": 1000.0})
    monkeypatch.setattr(policy, "FX_SPREAD_PCT",
                        {"basic": 2.0, "premium": 0.5})
    monkeypatch.setattr(policy, "TRANSFER_FEES",
                        {"sepa": (1.0, 0.0), "swift": (5.0, 0.1)})
    monkeypatch.setattr(policy, "to_eur",
                        lambda amount, cur: amount * policy.RATES_TO_EUR[cur])


# ---- mid_rate ----

def test_mid_rate_cross_currency():
    assert fx.mid_rate("GBP", "USD") == pytest.approx(4.0)


def test_mid_rate_same_currency_is_one():
    assert fx.mid_rate("USD", "USD") == 1.0


@pytest.mark.parametrize("src,dst,bad", [("XXX", "EUR", "XXX"),
                                         ("EUR", "YYY", "YYY")])
def test_mid_rate_unknown_currency(src, dst, bad):
    with pytest.raises(ValueError, match=f"Unknown currency: {bad}"):
        fx.mid_rate(src, dst)


# ---- quote ----

def test_quote_unknown_tier():
    with pytest.raises(ValueError, match="Unknown tier: gold"):
        fx.quote(10, "EUR", "USD", "gold")


def test_quote_unknown_currency():
    with pytest.raises(ValueError, match="Unknown currency"):
        fx.quote(10, "EUR", "XXX", "basic")


def test_quote_within_allowance_has_no_spread():
    q = fx.quote(50, "EUR", "USD", "basic")
    assert q.allowance_applied is True
    assert q.spread_pct == 0.0
    assert q.spread_amount == 0.0
    assert q.gross_amount == pytest.approx(100.0)  # 50 * (1/0.5)
    assert q.final_amount == q.gross_amount


def test_quote_exactly_at_allowance_boundary_is_free():
    q = fx.quote(100, "EUR", "EUR", "basic")
    assert q.allowance_applied is True
    assert q.spread_amount == 0.0


def test_quote_just_over_allowance_charges_full_spread():
    q = fx.quote(100.01, "EUR", "EUR", "basic")
    assert q.allowance_applied is False
    assert q.spread_pct == 2.0
    assert q.spread_amount == pytest.approx(100.01 * 0.02)
    assert q.final_amount == pytest.approx(100.01 * 0.98)


def test_quote_prior_usage_counts_toward_allowance():
    q = fx.quote(60, "EUR", "EUR", "basic", allowance_used_eur=50)
    assert q.allowance_applied is False
    assert q.allowance_used_before_eur == 50
    assert q.spread_amount == pytest.approx(60 * 0.02)


def test_quote_allowance_measured_in_eur_not_source_currency():
    # 150 USD == 75 EUR -> у межах ліміту 100 EUR
    q = fx.quote(150, "USD", "EUR", "basic")
    assert q.allowance_applied is True


def test_quote_tier_changes_spread_and_allowance():
    basic = fx.quote(500, "EUR", "EUR", "basic")
    premium = fx.quote(500, "EUR", "EUR", "premium")
    assert basic.spread_pct == 2.0 and not basic.allowance_applied
    assert premium.allowance_applied and premium.spread_amount == 0.0
    assert premium.allowance_total_eur == 1000.0


def test_quote_spread_override_applies_when_over_allowance():
    q = fx.quote(200, "EUR", "EUR", "basic", spread_pct_override=5.0)
    assert q.spread_pct == 5.0
    assert q.spread_amount == pytest.approx(10.0)


def test_quote_spread_override_zero_is_respected():
    # 0.0 не None, тому не має підміняться тарифним спредом
    q = fx.quote(200, "EUR", "EUR", "basic", spread_pct_override=0.0)
    assert q.spread_pct == 0.0
    assert q.spread_amount == 0.0


def test_quote_override_ignored_within_allowance():
    q = fx.quote(10, "EUR", "EUR", "basic", spread_pct_override=9.0)
    assert q.spread_pct == 0.0


def test_quote_partial_allowance_charges_only_excess():
    # ліміт 100, використано 0, сума 200 -> оплачується половина
    q = fx.quote(200, "EUR", "EUR", "basic", partial_allowance=True)
    assert q.allowance_applied is False
    assert q.spread_amount == pytest.approx(200 * 0.5 * 0.02)


def test_quote_partial_allowance_allowance_already_exhausted():
    q = fx.quote(100, "EUR", "EUR", "basic",
                 allowance_used_eur=150, partial_allowance=True)
    # remaining = 0 -> оплачується все
    assert q.spread_amount == pytest.approx(100 * 0.02)


def test_quote_partial_allowance_ignored_when_within():
    q = fx.quote(50, "EUR", "EUR", "basic", partial_allowance=True)
    assert q.spread_amount == 0.0


def test_quote_zero_amount_is_free_and_safe():
    q = fx.quote(0, "EUR", "USD", "basic", partial_allowance=True)
    assert q.allowance_applied is True
    assert q.gross_amount == 0.0
    assert q.final_amount == 0.0


def test_quote_zero_amount_over_exhausted_allowance_no_division_error():
    q = fx.quote(0, "EUR", "EUR", "basic",
                 allowance_used_eur=101, partial_allowance=True)
    assert q.spread_amount == 0.0


def test_quote_final_equals_gross_minus_spread():
    q = fx.quote(333.33, "GBP", "USD", "basic")
    assert q.final_amount == pytest.approx(q.gross_amount - q.spread_amount)


# ---- FxQuote.as_dict ----

def test_as_dict_rounds_floats_to_six_places_and_keeps_other_types():
    q = fx.FxQuote("EUR", "USD", 1.0, 1 / 3, "basic", 2.0,
                   100.0, 0.0, False, 1.23456789, 0.0, 1.23456789)
    d = q.as_dict()
    assert d["mid_rate"] == 0.333333
    assert d["gross_amount"] == 1.234568
    assert d["from_currency"] == "EUR"
    assert d["allowance_applied"] is False
    assert set(d) == set(fx.FxQuote.__dataclass_fields__)


# ---- transfer_fee ----

def test_transfer_fee_flat_only():
    r = fx.transfer_fee(1000, "sepa")
    assert r["total_fee_eur"] == 1.0
    assert r["flat_fee_eur"] == 1.0 and r["percent_fee"] == 0.0


def test_transfer_fee_flat_plus_percent():
    r = fx.transfer_fee(1000, "swift")
    assert r == {"transfer_type": "swift", "amount_eur": 1000,
                 "flat_fee_eur": 5.0, "percent_fee": 0.1,
                 "total_fee_eur": 6.0}


def test_transfer_fee_rounds_to_cents():
    assert fx.transfer_fee(33.333, "swift")["total_fee_eur"] == 5.03


def test_transfer_fee_zero_amount_is_flat_fee():
    assert fx.transfer_fee(0, "swift")["total_fee_eur"] == 5.0


def test_transfer_fee_unknown_type():
    with pytest.raises(ValueError, match="Unknown transfer type: wire"):
        fx.transfer_fee(10, "wire")
