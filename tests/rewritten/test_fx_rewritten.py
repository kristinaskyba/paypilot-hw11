import pytest

from app.engines import fx

def test_allowance_is_counted_in_eur_not_source_currency():
    quote = fx.quote(
        amount=540,
        from_currency="USD",
        to_currency="EUR",
        tier="tier1",
        allowance_used_eur=0,
    )

    assert quote.allowance_applied is True
    assert quote.spread_pct == 0
    assert quote.spread_amount == 0
    assert quote.final_amount == quote.gross_amount

def test_partial_allowance_charges_whole_amount_when_allowance_used_up():
    quote = fx.quote(
        amount=100,
        from_currency="EUR",
        to_currency="EUR",
        tier="tier1",
        allowance_used_eur=600,
        partial_allowance=True,
    )

    assert quote.allowance_applied is False
    assert quote.spread_pct == 1.5
    assert quote.spread_amount == pytest.approx(1.5)
    assert quote.final_amount == pytest.approx(98.5)