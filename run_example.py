"""Example run against the sample company."""
from __future__ import annotations

import sample_company as sc
from finance import cash_flow, metrics, working_capital


def money(v):
    return f"{v:>14,.0f}"


if __name__ == "__main__":
    cf = cash_flow.build(
        sc.INCOME, sc.BALANCE_CURRENT, sc.BALANCE_PRIOR,
        investing=sc.INVESTING, financing=sc.FINANCING,
    )

    print("=" * 56)
    print("  CASH FLOW — indirect method")
    print("=" * 56)
    for section in ("Operating", "Investing", "Financing"):
        print(f"\n  {section}")
        for _, r in cf.lines[cf.lines.section == section].iterrows():
            print(f"    {r.line:<34}{money(r.amount)}")

    print()
    print(f"  {'Operating cash flow':<34}{money(cf.operating)}")
    print(f"  {'Investing cash flow':<34}{money(cf.investing)}")
    print(f"  {'Financing cash flow':<34}{money(cf.financing)}")
    print(f"  {'Net change in cash':<34}{money(cf.net_change)}")
    print(f"  {'Opening cash':<34}{money(cf.opening_cash)}")
    print(f"  {'Closing cash':<34}{money(cf.closing_cash)}")
    print(f"\n  Reconciles: {cf.reconciles}  "
          f"(gap {cash_flow.reconciliation_gap(cf):,.2f})")

    p = metrics.profitability(sc.INCOME)
    print("\n" + "=" * 56)
    print("  PROFITABILITY")
    print("=" * 56)
    print(f"  {'Revenue':<34}{money(p.revenue)}")
    print(f"  {'Gross profit':<34}{money(p.gross_profit)}   {p.gross_margin:6.1%}")
    print(f"  {'EBITDA':<34}{money(p.ebitda)}   {p.ebitda_margin:6.1%}")
    print(f"  {'Operating expense ratio':<34}{'':>14}   "
          f"{p.operating_expense_ratio:6.1%}")

    pc = metrics.prime_cost(sc.INCOME)
    print(f"  {'Prime cost':<34}{money(pc['prime_cost'])}   "
          f"{pc['prime_cost_pct']:6.1%}")

    wc_now = working_capital.analyze(
        sc.BALANCE_CURRENT, sc.INCOME["revenue"], sc.INCOME["cogs"])
    wc_prior = working_capital.analyze(
        sc.BALANCE_PRIOR, sc.INCOME["revenue"], sc.INCOME["cogs"])

    print("\n" + "=" * 56)
    print("  WORKING CAPITAL")
    print("=" * 56)
    print(f"  {'Operating working capital':<34}{money(wc_now.operating_wc)}")
    print(f"  {'As % of revenue':<34}{'':>14}   {wc_now.wc_to_revenue:6.1%}")
    print(f"  {'Days sales outstanding':<34}{wc_now.dso:>14.1f}")
    print(f"  {'Days inventory outstanding':<34}{wc_now.dio:>14.1f}")
    print(f"  {'Days payable outstanding':<34}{wc_now.dpo:>14.1f}")
    print(f"  {'Cash conversion cycle':<34}{wc_now.cash_cycle:>14.1f}")
    print(f"  {'Cash absorbed by movement':<34}"
          f"{money(working_capital.funding_requirement(wc_now, wc_prior))}")

    actual = {k: sc.INCOME[k] for k in ("revenue", "cogs", "labour",
                                        "operating_expenses")}
    var = metrics.variance(actual, sc.BUDGET)

    print("\n" + "=" * 56)
    print("  BUDGET VARIANCE")
    print("=" * 56)
    print(var.to_string(index=False,
                        formatters={"actual": money, "budget": money,
                                    "variance": money,
                                    "variance_pct": lambda v: f"{v:7.1%}"}))
