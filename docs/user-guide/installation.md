# Installation

## Install the Package

```bash
pip install fiscal
```

Install direct runtime dependencies when developing from source:

```bash
pip install pandas boogr
```

## Configure the Database

Create or update `config.py`:

```python
DB_PATH: str = "path/to/fiscal.db"

TABLES: list[ str ] = [
    "BudgetFiscalYears",
    "FederalHolidays",
]
```

The first table must contain fiscal-year records. The second must contain federal-holiday records.

## Verify the Installation

```python
from fiscal import FiscalYear

fy = FiscalYear( 2026 )
print( fy.fiscal_year )
```

A missing database, table, record, or required column raises `boogr.Error`.
