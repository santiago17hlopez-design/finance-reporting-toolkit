"""Profitability metrics and budget variance."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


def _safe_div(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if denominator else float("nan")


@dataclass
class Profitability:
    revenue: float
    gross_profit: float
    gross_margin: float
    ebitda: float
    ebitda_margin: float
    operating_expense_ratio: float


def ebitda(income: dict) -> float:
    """Operating income before depreciation and amortization."""
    return (
        float(income.get("operating_income", 0.0))
        + float(income.get("depreciation", 0.0))
        + float(income.get("amortization", 0.0))
    )


def profitability(income: dict) -> Profitability:
    """Headline margins for one period."""
    revenue = float(income.get("revenue", 0.0))
    cogs = float(income.get("cogs", 0.0))
    opex = float(income.get("operating_expenses", 0.0))
    gross = revenue - cogs
    e = ebitda(income)

    return Profitability(
        revenue=revenue,
        gross_profit=gross,
        gross_margin=_safe_div(gross, revenue),
        ebitda=e,
        ebitda_margin=_safe_div(e, revenue),
        operating_expense_ratio=_safe_div(opex, revenue),
    )


def prime_cost(income: dict) -> dict:
    """Direct cost plus labour, as a share of revenue."""
    revenue = float(income.get("revenue", 0.0))
    direct = float(income.get("cogs", 0.0))
    labour = float(income.get("labour", 0.0))
    total = direct + labour

    return {
        "direct_cost": direct,
        "labour_cost": labour,
        "prime_cost": total,
        "direct_cost_pct": _safe_div(direct, revenue),
        "labour_cost_pct": _safe_div(labour, revenue),
        "prime_cost_pct": _safe_div(total, revenue),
    }


def variance(actual: dict, budget: dict, favourable_when_higher: set | None = None
             ) -> pd.DataFrame:
    """Line-by-line actual against budget.

    ``favourable_when_higher`` names the lines where exceeding budget is good
    (revenue, for example). Every other line is treated as a cost.
    """
    favourable_when_higher = favourable_when_higher or {"revenue"}
    lines = sorted(set(actual) | set(budget))
    rows = []

    for line in lines:
        a = float(actual.get(line, 0.0))
        b = float(budget.get(line, 0.0))
        delta = a - b
        favourable = delta >= 0 if line in favourable_when_higher else delta <= 0
        rows.append({
            "line": line,
            "actual": a,
            "budget": b,
            "variance": delta,
            "variance_pct": _safe_div(delta, abs(b)) if b else float("nan"),
            "favourable": favourable,
        })

    return pd.DataFrame(rows)


def attainment(actual: float, target: float) -> float:
    """Actual as a share of target."""
    return _safe_div(actual, target)
