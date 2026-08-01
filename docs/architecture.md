# Architecture

## Overview

Fiscal is organized around three existing classes in the package module:

- `DB`: SQLite connection and query behavior
- `FiscalYear`: fiscal-year records and calculations
- `FederalHoliday`: federal-holiday records and observed-date behavior

No additional domain classes are required for calendar rendering. Text and HTML calendar methods are integrated directly into `FiscalYear`.

## Data Flow

```text
config.py
   │
   ├── DB_PATH
   └── TABLES
          │
          ▼
         DB
      ┌───┴───────────────┐
      ▼                   ▼
 FiscalYear        FederalHoliday
      │                   │
      └──── holiday calculations ────┘
```

## Configuration

`config.py` supplies:

```python
DB_PATH: str
TABLES: list[ str ]
```

The expected table order is:

1. `BudgetFiscalYears`
2. `FederalHolidays`

## Fiscal-Year Entity

`FiscalYear` hydrates one database row and derives:

- calendar and fiscal progress
- fiscal month, quarter, and week boundaries
- weekday, weekend, holiday, and workday collections
- date-range counts and holiday mappings
- text and HTML calendars for months, fiscal years, and date ranges

## Federal-Holiday Entity

`FederalHoliday` loads actual holiday dates and calculates observed dates:

- Saturday holidays are observed on Friday
- Sunday holidays are observed on Monday
- weekday holidays are unchanged

## Error Handling

Operational methods wrap exceptions with `boogr.Error`, including module, cause, and method metadata. This preserves the original exception as the underlying cause while presenting a consistent package-level error contract.
