"""Each case is small enough to verify by hand."""
from __future__ import annotations

import math

from finance import cash_flow, metrics, working_capital


def test_cash_flow_reconciles_to_the_reported_balance():
    income = {"net_income": 1000.0, "depreciation": 200.0}
    prior = {"cash": 500.0, "accounts_receivable": 300.0,
             "inventory": 100.0, "accounts_payable": 150.0}
    current = {"cash": 1700.0, "accounts_receivable": 300.0,
               "inventory": 100.0, "accounts_payable": 150.0}

    cf = cash_flow.build(income, current, prior)

    assert cf.operating == 1200.0
    assert cf.net_change == 1200.0
    assert cf.closing_cash == 1700.0
    assert cf.reconciles
    assert math.isclose(cash_flow.reconciliation_gap(cf), 0.0, abs_tol=1e-9)


def test_receivable_increase_consumes_cash():
    income = {"net_income": 1000.0, "depreciation": 0.0}
    prior = {"cash": 0.0, "accounts_receivable": 100.0}
    current = {"cash": 900.0, "accounts_receivable": 200.0}

    cf = cash_flow.build(income, current, prior)

    assert cf.operating == 900.0
    assert cf.reconciles


def test_payable_increase_releases_cash():
    income = {"net_income": 1000.0, "depreciation": 0.0}
    prior = {"cash": 0.0, "accounts_payable": 100.0}
    current = {"cash": 1100.0, "accounts_payable": 200.0}

    cf = cash_flow.build(income, current, prior)

    assert cf.operating == 1100.0
    assert cf.reconciles


def test_non_reconciling_statement_is_flagged():
    income = {"net_income": 1000.0, "depreciation": 0.0}
    prior = {"cash": 0.0}
    current = {"cash": 999.0}

    cf = cash_flow.build(income, current, prior)

    assert not cf.reconciles
    assert math.isclose(cash_flow.reconciliation_gap(cf), 1.0)


def test_investing_and_financing_flow_into_net_change():
    income = {"net_income": 500.0, "depreciation": 0.0}
    prior = {"cash": 0.0}
    current = {"cash": 350.0}

    cf = cash_flow.build(
        income, current, prior,
        investing={"Equipment": -300.0},
        financing={"Loan": 150.0},
    )

    assert cf.investing == -300.0
    assert cf.financing == 150.0
    assert cf.net_change == 350.0
    assert cf.reconciles


def test_ebitda_adds_back_depreciation_and_amortization():
    assert metrics.ebitda({"operating_income": 800.0,
                           "depreciation": 150.0,
                           "amortization": 50.0}) == 1000.0


def test_margins():
    p = metrics.profitability({"revenue": 1000.0, "cogs": 600.0,
                               "operating_expenses": 250.0,
                               "operating_income": 150.0,
                               "depreciation": 50.0})
    assert p.gross_profit == 400.0
    assert math.isclose(p.gross_margin, 0.40)
    assert p.ebitda == 200.0
    assert math.isclose(p.ebitda_margin, 0.20)
    assert math.isclose(p.operating_expense_ratio, 0.25)


def test_prime_cost():
    pc = metrics.prime_cost({"revenue": 1000.0, "cogs": 300.0, "labour": 280.0})
    assert pc["prime_cost"] == 580.0
    assert math.isclose(pc["prime_cost_pct"], 0.58)


def test_operating_working_capital():
    assert working_capital.operating_working_capital({
        "accounts_receivable": 500.0,
        "inventory": 200.0,
        "accounts_payable": 300.0,
    }) == 400.0


def test_cash_cycle():
    wc = working_capital.analyze(
        {"accounts_receivable": 1000.0, "inventory": 500.0,
         "accounts_payable": 750.0},
        revenue=7300.0, cogs=3650.0, days=365,
    )
    assert math.isclose(wc.dso, 50.0)
    assert math.isclose(wc.dio, 50.0)
    assert math.isclose(wc.dpo, 75.0)
    assert math.isclose(wc.cash_cycle, 25.0)


def test_zero_denominator_returns_nan_not_an_error():
    assert math.isnan(working_capital.days_sales_outstanding(100.0, 0.0))
    assert math.isnan(metrics.attainment(100.0, 0.0))


def test_variance_direction_depends_on_the_line():
    df = metrics.variance(
        actual={"revenue": 900.0, "cogs": 400.0},
        budget={"revenue": 1000.0, "cogs": 500.0},
    )
    rev = df[df.line == "revenue"].iloc[0]
    cogs = df[df.line == "cogs"].iloc[0]

    assert rev.variance == -100.0 and not rev.favourable
    assert cogs.variance == -100.0 and cogs.favourable
