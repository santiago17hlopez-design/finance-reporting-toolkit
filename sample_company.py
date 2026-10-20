"""A small fictional company, used by the example and the tests."""
from __future__ import annotations

INCOME = {
    "revenue": 4_820_000.0,
    "cogs": 2_795_600.0,
    "labour": 964_000.0,
    "operating_expenses": 1_156_800.0,
    "operating_income": 867_600.0,
    "depreciation": 184_000.0,
    "amortization": 36_000.0,
    "net_income": 612_400.0,
}

BALANCE_CURRENT = {
    "cash": 728_700.0,
    "accounts_receivable": 742_000.0,
    "inventory": 318_500.0,
    "prepaid_expenses": 41_200.0,
    "accounts_payable": 395_800.0,
    "accrued_liabilities": 128_400.0,
}

BALANCE_PRIOR = {
    "cash": 311_900.0,
    "accounts_receivable": 668_500.0,
    "inventory": 296_100.0,
    "prepaid_expenses": 38_700.0,
    "accounts_payable": 352_300.0,
    "accrued_liabilities": 119_600.0,
}

INVESTING = {
    "Purchase of equipment": -268_000.0,
    "Proceeds from asset disposal": 24_500.0,
}

FINANCING = {
    "Loan drawdown": 150_000.0,
    "Loan repayment": -96_000.0,
    "Dividends paid": -180_000.0,
}

BUDGET = {
    "revenue": 5_000_000.0,
    "cogs": 2_850_000.0,
    "labour": 925_000.0,
    "operating_expenses": 1_100_000.0,
}
