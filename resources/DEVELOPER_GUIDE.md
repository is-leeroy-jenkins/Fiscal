# Fiscal Developer Guide

Fiscal is a Python library for U.S. federal fiscal-year, calendar-year, federal-holiday, workday, weekend, and reporting calculations. This guide describes the current implementation contract, internal architecture, database dependencies, development workflow, testing approach, and extension points.

## Project Layout

A minimal project layout is:

```text
Fiscal/
├── fiscal/
│   └── __init__.py
├── resources/
│   └── data/
│       └── fiscal.db
├── config.py
├── pyproject.toml
├── README.md
├── USER_GUIDE.md
└── DEVELOPER_GUIDE.md
```

The package name is `fiscal`.

```python
from fiscal import DB, FederalHoliday, FiscalYear, throw_if, to_date
```

## Runtime Dependencies

The current implementation imports:

```text
calendar
sqlite3
datetime
typing
pandas
config
boogr
```

Third-party dependencies:

```bash
pip install pandas boogr
```

Development dependencies may include:

```bash
pip install pytest pytest-cov ruff mypy
```

## Configuration Contract

The package expects `config.py` to expose two members:

```python
DB_PATH: str = "resources/data/fiscal.db"

TABLES: list[str] = [
    "BudgetFiscalYears",
    "FederalHolidays",
]
```

`DB_PATH` identifies the SQLite database used by `DB.create_connection()`.

`TABLES` is positional:

| Index | Purpose |
|---:|---|
| `0` | Fiscal-year table |
| `1` | Federal-holiday table |

Changing this order changes which table is queried by `FiscalYear` and `FederalHoliday`.

## Database Contract

### Fiscal-year table

`FiscalYear` expects one matching row for the requested combination of fiscal year, beginning period of availability, and ending period of availability.

Expected fields:

| Column | Purpose |
|---|---|
| `ID` | Row identifier |
| `FiscalYear` | Fiscal-year label |
| `BPOA` | Beginning period of availability |
| `EPOA` | Ending period of availability |
| `StartDate` | Fiscal-year start date |
| `EndDate` | Fiscal-year end date |
| `ExpirationDate` | Expiration date or supported sentinel |
| `CancellationDate` | Cancellation date or supported sentinel |
| `Weekdays` | Stored weekday count |
| `Weekends` | Stored weekend count |
| `Workdays` | Stored workday count |
| `CompensableDays` | Stored compensable-day count |
| `CompensableHours` | Stored compensable-hour count |
| `Type` | Appropriation type |
| `Availability` | Availability description |

### Federal-holiday table

`FederalHoliday` expects one matching row for the requested fiscal year.

Expected fields:

| Column | Purpose |
|---|---|
| `ID` | Row identifier |
| `FiscalYear` | Fiscal-year label |
| `ColumbusDay` | Columbus Day |
| `VeteransDay` | Veterans Day |
| `ThanksgivingDay` | Thanksgiving Day |
| `ChristmasDay` | Christmas Day |
| `NewYearsDay` | New Year's Day |
| `MartinLutherKingDay` | Birthday of Martin Luther King, Jr. |
| `PresidentsDay` | Washington's Birthday |
| `MemorialDay` | Memorial Day |
| `JuneteenthDay` | Juneteenth National Independence Day |
| `IndependenceDay` | Independence Day |
| `LaborDay` | Labor Day |

## Architecture

The implementation consists of two utility functions and three public classes.

### `throw_if`

```python
def throw_if(
    name: str,
    value: object,
) -> None:
```

Validates required arguments before database or calculation logic proceeds.

### `to_date`

```python
def to_date(
    value: date | datetime | str | None,
) -> Optional[date]:
```

Normalizes supported date values to `datetime.date`.

Supported string formats:

```text
YYYY-MM-DD
MM/DD/YYYY
MM/DD/YY
```

Supported null-like values include:

```text
None
""
"NS"
"N/A"
"NA"
"NONE"
"NULL"
```

### `DB`

Responsibilities:

- retain the configured database path and table collection;
- create SQLite connections;
- query fiscal-year records;
- query federal-holiday records;
- return query results as pandas DataFrames.

The database layer intentionally performs no calendar calculations.

### `FiscalYear`

Responsibilities:

- load one fiscal-year record;
- expose stored appropriation and availability values;
- calculate calendar-year and fiscal-year progress;
- calculate fiscal month, quarter, and week boundaries;
- count weekdays, weekends, holidays, and workdays;
- produce fiscal date collections and monthly groupings;
- return serializable dictionary representations.

The class is database-backed. Construction is therefore both object initialization and data hydration.

```python
fy = FiscalYear(
    fy="2026",
    bpoa="2026",
    epoa="2026",
)
```

### `FederalHoliday`

Responsibilities:

- load one federal-holiday row;
- expose stored holiday dates;
- derive observed dates;
- distinguish actual and observed holiday dates;
- evaluate holiday and weekend membership;
- return serializable dictionary representations.

```python
holiday = FederalHoliday("2026")
```

## Object Hydration

`FiscalYear.__init__()` resolves empty availability values to the supplied fiscal year:

```python
self.fiscal_year = fy
self.bpoa = bpoa or fy
self.epoa = epoa or fy
```

It then queries the fiscal-year table and requires exactly one matching row.

`FederalHoliday.__init__()` queries by fiscal year and likewise requires exactly one matching row.

Developers adding new constructor parameters should preserve this sequence:

1. validate the argument;
2. assign it to an instance member;
3. use the instance member in downstream calls;
4. hydrate the returned row;
5. convert database values to their runtime types.

## Date Semantics

Fiscal years run from October 1 through September 30.

For FY 2026:

```text
Start: 2025-10-01
End:   2026-09-30
```

Fiscal-month numbering is:

| Fiscal Month | Calendar Month |
|---:|---|
| `1` | October |
| `2` | November |
| `3` | December |
| `4` | January |
| `5` | February |
| `6` | March |
| `7` | April |
| `8` | May |
| `9` | June |
| `10` | July |
| `11` | August |
| `12` | September |

Observed federal holidays follow the weekday adjustment used by the implementation:

- Saturday holidays are observed on Friday.
- Sunday holidays are observed on Monday.
- Weekday holidays retain their actual date.

## Error Handling

The package uses `boogr.Error` to preserve contextual failure information.

The established pattern is:

```python
except Exception as e:
    ex = Error(e)
    ex.module = "fiscal"
    ex.cause = "FiscalYear"
    ex.method = (
        "method_name( self, parameter: type ) "
        "-> return_type"
    )
    raise ex
```

When adding or changing methods:

- preserve the original exception as the cause;
- set `module`;
- set `cause`;
- set the complete method signature;
- raise the same `Error` instance;
- do not create a second wrapper object.

## Adding a Calculation Method

A new calculation method should:

1. use existing hydrated members when possible;
2. validate external arguments with `throw_if`;
3. assign validated arguments to instance members before use;
4. return a fully annotated value;
5. use inclusive or exclusive date semantics consistently;
6. add the public method name to `__dir__()`;
7. include a Google-style docstring;
8. preserve the established `Error` wrapping pattern.

Example structure:

```python
def example_count(
    self,
    start: date,
    end: date,
) -> int:
    """Count matching dates in an inclusive range.

    Purpose:
        Counts dates satisfying the operation's rule between
        the supplied start and end dates, inclusive.

    Args:
        start (date): First date included in the range.
        end (date): Final date included in the range.

    Returns:
        int: Number of matching dates.
    """
    try:
        throw_if("start", start)
        throw_if("end", end)

        self.start = start
        self.end = end

        return 0
    except Exception as e:
        ex = Error(e)
        ex.module = "fiscal"
        ex.cause = "FiscalYear"
        ex.method = (
            "example_count( self, start: date, "
            "end: date ) -> int"
        )
        raise ex
```

## Extending the Database Model

When a new database column is introduced:

1. add the column to the SQLite table;
2. populate it for every supported fiscal year;
3. add the corresponding class annotation;
4. hydrate it in the constructor;
5. convert it to the correct Python type;
6. expose it through `to_dict()` when it is part of the public record;
7. update tests for null, sentinel, and malformed values;
8. update the user and developer documentation.

Do not rely on numeric row positions when a named-column access pattern is available. Named columns make schema changes easier to audit.

## Public Surface Maintenance

The package uses explicit `__dir__()` implementations to expose its supported members.

Whenever a public method or property is added or renamed:

- update the corresponding `__dir__()` method;
- remove obsolete names;
- verify every listed name exists;
- verify every intended public name is listed.

A simple test can enforce the contract:

```python
def test_fiscal_year_dir_members_exist() -> None:
    fy = FiscalYear("2026")

    for name in fy.__dir__():
        assert hasattr(fy, name)
```

## Testing

### Unit tests

Unit tests should cover:

- `throw_if`;
- `to_date`;
- observed-date adjustment;
- fiscal-month mapping;
- fiscal-quarter mapping;
- fiscal-week boundaries;
- leap-day calculations;
- reversed date ranges;
- actual versus observed holiday behavior.

Example:

```python
from datetime import date

from fiscal import FederalHoliday


def test_saturday_holiday_is_observed_friday() -> None:
    holiday = FederalHoliday("2026")

    actual = date(2026, 7, 4)
    observed = holiday.observed_date(actual)

    assert observed == date(2026, 7, 3)
```

### Integration tests

Integration tests should use a temporary SQLite database containing controlled rows for both tables.

Test at least:

- one ordinary fiscal year;
- one leap-day fiscal year;
- one multi-year availability period;
- one weekend holiday;
- one fiscal year with sentinel expiration or cancellation values;
- missing rows;
- duplicate rows;
- malformed date values.

### Cross-checks

Useful consistency assertions include:

```python
assert (
    len(fy.fiscal_weekdays())
    + len(fy.fiscal_weekends())
    == fy.fiscal_days_in_year()
)
```

```python
assert len(
    fy.fiscal_workdays()
) == fy.count_workdays(
    fy.start_date,
    fy.end_date,
)
```

```python
assert fy.fiscal_month_bounds(1)[0] == fy.start_date
assert fy.fiscal_month_bounds(12)[1] == fy.end_date
```

### Compilation

```bash
python -m py_compile fiscal/__init__.py
```

### Test execution

```bash
pytest -q
```

With coverage:

```bash
pytest --cov=fiscal --cov-report=term-missing
```

## Static Analysis

Ruff:

```bash
ruff check fiscal tests
```

Mypy:

```bash
mypy fiscal
```

The current implementation uses `typing.Dict`, `typing.List`, `typing.Optional`, and `typing.Tuple`. Modernization to built-in generics should be performed consistently across the entire package rather than incrementally.

## Development Workflow

Recommended sequence:

```bash
git checkout -b feature/<name>
```

```bash
python -m py_compile fiscal/__init__.py
```

```bash
pytest -q
```

```bash
ruff check fiscal tests
```

```bash
git add fiscal tests DEVELOPER_GUIDE.md USER_GUIDE.md
git commit -m "Describe the change"
```

## Packaging

The distribution name and import package should both remain aligned with the renamed project:

```text
Distribution: fiscal
Import:       fiscal
Project:      Fiscal
```

Example `pyproject.toml` metadata:

```toml
[project]
name = "fiscal"
description = "Federal fiscal-year and holiday utilities"
requires-python = ">=3.11"
dependencies = [
    "boogr",
    "pandas",
]
```

Package discovery must include the `fiscal` package directory.

## Documentation Responsibilities

Use separate documents for separate audiences:

- `README.md`: project overview, installation, and repository-level instructions;
- `USER_GUIDE.md`: task-oriented consumer workflows;
- `DEVELOPER_GUIDE.md`: architecture, internal contracts, testing, and extension procedures;
- API reference: generated class and member documentation.

Do not place database reconstruction instructions or exhaustive member catalogs in the user guide.

## Release Checklist

Before publishing a release:

- confirm the package imports as `fiscal`;
- confirm no public documentation uses the former project name;
- compile the package;
- run the full test suite;
- validate the packaged SQLite database;
- verify every supported fiscal year returns exactly one row;
- verify actual and observed holiday behavior;
- verify `__dir__()` entries;
- regenerate API documentation;
- review `README.md`, `USER_GUIDE.md`, and `DEVELOPER_GUIDE.md`;
- update the version and changelog;
- build and inspect the distribution artifacts.

Build:

```bash
python -m build
```

Inspect:

```bash
python -m zipfile -l dist/fiscal-*.whl
```

Install the wheel into a clean environment before release:

```bash
pip install dist/fiscal-*.whl
python -c "from fiscal import FiscalYear; print(FiscalYear('2026'))"
```
