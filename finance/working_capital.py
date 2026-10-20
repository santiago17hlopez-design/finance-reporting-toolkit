"""Operating working capital and the cash conversion cycle."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorkingCapital:
    operating_wc: float
    dso: float
    dio: float
    dpo: float
    cash_cycle: float
    wc_to_revenue: float


def _safe_div(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else float("nan")


def operating_working_capital(balance: dict) -> float:
    """Receivables plus inventory less payables."""
    return (
        float(balance.get("accounts_receivable", 0.0))
        + float(balance.get("inventory", 0.0))
        - float(balance.get("accounts_payable", 0.0))
    )


def days_sales_outstanding(receivables: float, revenue: float, days: int = 365) -> float:
    return _safe_div(receivables, revenue) * days


def days_inventory_outstanding(inventory: float, cogs: float, days: int = 365) -> float:
    return _safe_div(inventory, cogs) * days


def days_payable_outstanding(payables: float, cogs: float, days: int = 365) -> float:
    return _safe_div(payables, cogs) * days


def analyze(balance: dict, revenue: float, cogs: float, days: int = 365) -> WorkingCapital:
    """Working capital position and the cycle metrics for one period."""
    dso = days_sales_outstanding(balance.get("accounts_receivable", 0.0), revenue, days)
    dio = days_inventory_outstanding(balance.get("inventory", 0.0), cogs, days)
    dpo = days_payable_outstanding(balance.get("accounts_payable", 0.0), cogs, days)
    owc = operating_working_capital(balance)

    return WorkingCapital(
        operating_wc=owc,
        dso=dso,
        dio=dio,
        dpo=dpo,
        cash_cycle=dso + dio - dpo,
        wc_to_revenue=_safe_div(owc, revenue),
    )


def funding_requirement(current: WorkingCapital, prior: WorkingCapital) -> float:
    """Cash absorbed by the movement in working capital between two periods."""
    return current.operating_wc - prior.operating_wc
