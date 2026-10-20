# Finance Reporting Toolkit

Core financial reporting calculations in Python: indirect-method cash flow,
working capital and the cash conversion cycle, profitability metrics, and budget
variance.

Every function is covered by a test small enough to check by hand.

All figures are from a fictional sample company.

---

## Use

```bash
pip install -r requirements.txt
python run_example.py
python -m pytest -q
```

```python
from finance import cash_flow, metrics, working_capital

cf = cash_flow.build(income, balance_current, balance_prior,
                     investing=investing, financing=financing)
cf.reconciles          # closing cash derived == closing cash reported
cf.to_frame()          # line-by-line statement

p  = metrics.profitability(income)       # gross margin, EBITDA, opex ratio
wc = working_capital.analyze(balance, revenue, cogs)   # OWC, DSO/DIO/DPO, cycle
v  = metrics.variance(actual, budget)                  # line-by-line variance
```

## Example output

```
  Operating cash flow                      786,300
  Investing cash flow                     -243,500
  Financing cash flow                     -126,000
  Net change in cash                       416,800
  Opening cash                             311,900
  Closing cash                             728,700

  Reconciles: True  (gap 0.00)

  Revenue                                4,820,000
  Gross profit                           2,024,400    42.0%
  EBITDA                                 1,087,600    22.6%
  Prime cost                             3,759,600    78.0%

  Operating working capital                664,700    13.8% of revenue
  Cash conversion cycle                       46.1 days
```

## Contents

| Module | What it does |
|---|---|
| `finance/cash_flow.py` | Indirect-method statement from a P&L and two balance sheets, with a reconciliation check against reported closing cash |
| `finance/working_capital.py` | Operating working capital, DSO / DIO / DPO, cash conversion cycle, period-on-period funding requirement |
| `finance/metrics.py` | EBITDA, gross and EBITDA margin, operating expense ratio, prime cost, budget variance, attainment |

## Tests

```bash
python -m pytest -q      # 12 tests
```

Cash flow is tested for reconciliation, for the direction of receivable and
payable movements, for investing and financing flowing into net change, and for
a non-reconciling statement being flagged rather than passed. Variance is tested
for treating revenue and cost lines in opposite directions. Zero denominators
return `nan` rather than raising.

## Notes

- Monthly or annual periods; pass `days` to the working-capital functions to
  match the period.
- Account mapping is the caller's responsibility: these functions take dicts of
  already-classified totals.
- Requires `pandas`. Nothing else.
