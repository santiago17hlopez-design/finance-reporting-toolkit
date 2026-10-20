"""Indirect-method cash flow statement."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class CashFlow:
    operating: float
    investing: float
    financing: float
    net_change: float
    opening_cash: float
    closing_cash: float
    reconciles: bool
    lines: pd.DataFrame

    def to_frame(self) -> pd.DataFrame:
        return self.lines


def _delta(current: dict, prior: dict, key: str) -> float:
    return float(current.get(key, 0.0)) - float(prior.get(key, 0.0))


def build(income: dict, balance_current: dict, balance_prior: dict,
          investing: dict | None = None, financing: dict | None = None,
          tolerance: float = 0.01) -> CashFlow:
    """Build an indirect-method statement from a P&L and two balance sheets.

    Parameters
    ----------
    income
        Requires ``net_income`` and ``depreciation``. Optional:
        ``amortization``, ``other_non_cash``.
    balance_current, balance_prior
        Require ``accounts_receivable``, ``inventory``, ``accounts_payable``,
        ``cash``. Optional: ``accrued_liabilities``, ``prepaid_expenses``.
    investing, financing
        Named line items. Negative values are outflows.
    """
    investing = investing or {}
    financing = financing or {}

    net_income = float(income.get("net_income", 0.0))
    non_cash = (
        float(income.get("depreciation", 0.0))
        + float(income.get("amortization", 0.0))
        + float(income.get("other_non_cash", 0.0))
    )

    d_ar = _delta(balance_current, balance_prior, "accounts_receivable")
    d_inv = _delta(balance_current, balance_prior, "inventory")
    d_prepaid = _delta(balance_current, balance_prior, "prepaid_expenses")
    d_ap = _delta(balance_current, balance_prior, "accounts_payable")
    d_accrued = _delta(balance_current, balance_prior, "accrued_liabilities")

    wc_change = -d_ar - d_inv - d_prepaid + d_ap + d_accrued

    operating = net_income + non_cash + wc_change
    investing_total = sum(float(v) for v in investing.values())
    financing_total = sum(float(v) for v in financing.values())
    net_change = operating + investing_total + financing_total

    opening = float(balance_prior.get("cash", 0.0))
    closing = float(balance_current.get("cash", 0.0))

    rows = [
        ("Operating", "Net income", net_income),
        ("Operating", "Depreciation", float(income.get("depreciation", 0.0))),
    ]
    if income.get("amortization"):
        rows.append(("Operating", "Amortization", float(income["amortization"])))
    if income.get("other_non_cash"):
        rows.append(("Operating", "Other non-cash", float(income["other_non_cash"])))
    rows += [
        ("Operating", "Change in receivables", -d_ar),
        ("Operating", "Change in inventory", -d_inv),
    ]
    if d_prepaid:
        rows.append(("Operating", "Change in prepaid expenses", -d_prepaid))
    rows.append(("Operating", "Change in payables", d_ap))
    if d_accrued:
        rows.append(("Operating", "Change in accrued liabilities", d_accrued))

    rows += [("Investing", k, float(v)) for k, v in investing.items()]
    rows += [("Financing", k, float(v)) for k, v in financing.items()]

    lines = pd.DataFrame(rows, columns=["section", "line", "amount"])

    return CashFlow(
        operating=operating,
        investing=investing_total,
        financing=financing_total,
        net_change=net_change,
        opening_cash=opening,
        closing_cash=closing,
        reconciles=abs((opening + net_change) - closing) <= tolerance,
        lines=lines,
    )


def reconciliation_gap(cf: CashFlow) -> float:
    """Difference between the derived closing cash and the reported balance."""
    return (cf.opening_cash + cf.net_change) - cf.closing_cash
