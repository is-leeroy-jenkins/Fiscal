###### tempus

![](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/images/github/project_tempus.png)

<p align="center">
  <a href="#features">Features</a>
  &nbsp;&bull;&nbsp;
  <a href="#installation">Installation</a>
  &nbsp;&bull;&nbsp;
  <a href="#configuration">Configuration</a>
  &nbsp;&bull;&nbsp;
  <a href="#quick-start">Quick Start</a>
  &nbsp;&bull;&nbsp;
  <a href="#api-overview">API Overview</a>
  &nbsp;&bull;&nbsp;
  <a href="#design-notes">Design Notes</a>
  &nbsp;&bull;&nbsp;
  <a href="#roadmap">Roadmap</a>
  &nbsp;&bull;&nbsp;
  <a href="#license">License</a>
</p>

___



<a id="features"></a>

## 📝 Features

- **Database-Backed Fiscal Years**  
  Load one `BudgetFiscalYears` record by fiscal year, beginning period of availability (`BPOA`),
  and ending period of availability (`EPOA`).

- **Calendar and Fiscal Progress**  
  Calculate day-of-year, total days, elapsed days, remaining days, elapsed months, remaining
  months, and percent elapsed.

- **Federal Holiday Records**  
  Load the federal holidays associated with a fiscal year and return holiday names with their
  stored values.

- **Actual and Observed Holiday Dates**  
  Apply the standard Friday/Monday observation rule when a holiday falls on Saturday or Sunday.

- **Inclusive Range Utilities**  
  Count weekends, federal holidays, and workdays between two dates.

- **Typed Data Exports**  
  Export fiscal-year and holiday records as dictionaries for reporting, serialization, or analysis.

- **Input Validation and Error Wrapping**  
  Validate required values with `throw_if()` and wrap operational failures with `boogr.Error`.

<a id="installation"></a>

## 🏗️ Installation

Install the package with pip:

```bash
pip install tempus
```

Or add it to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
tempus = "^1.0.0"
```

The current implementation also requires:

```bash
pip install pandas boogr
```

<a id="configuration"></a>

## ⚙️ Configuration

The package imports `config.py` as `cfg` and expects the following members:

```python
DB_PATH: str
TABLES: list[str]
```

`DB_PATH` must identify the SQLite database file. `TABLES` must contain the approved table names
in this order:

```python
TABLES = [
    "BudgetFiscalYears",
    "FederalHolidays",
]
```

The fiscal-year table is selected from `TABLES[0]`, and the federal-holiday table is selected from
`TABLES[1]`.

### Required `BudgetFiscalYears` columns

```text
ID
FiscalYear
BPOA
EPOA
StartDate
EndDate
ExpirationDate
CancellationDate
Weekdays
Weekends
Workdays
CompensableDays
CompensableHours
Type
Availability
```

### Required `FederalHolidays` columns

```text
ID
FiscalYear
ColumbusDay
VeteransDay
ThanksgivingDay
ChristmasDay
NewYearsDay
MartinLutherKingDay
PresidentsDay
MemorialDay
JuneteenthDay
IndependenceDay
LaborDay
```

Each query must return exactly one row. A missing or duplicate record raises `LookupError`, which
is wrapped by `boogr.Error`.

<a id="quick-start"></a>

## 🎯 Quick Start

```python
from datetime import date

from tempus import FederalHoliday, FiscalYear
```

## 📊 Load a Fiscal Year

`FiscalYear` accepts a fiscal-year identifier and optional periods of availability. When `bpoa` or
`epoa` is empty, it defaults to the supplied fiscal year.

```python
fy = FiscalYear("2026")

fy.fiscal_year       # "2026"
fy.bpoa              # "2026"
fy.epoa              # "2026"
fy.start_date        # date loaded from BudgetFiscalYears
fy.end_date          # date loaded from BudgetFiscalYears
fy.type              # appropriation type
fy.availability      # availability description
```

Load a multi-year appropriation by supplying explicit availability bounds:

```python
fy = FiscalYear(
    fy="2026",
    bpoa="2024",
    epoa="2026",
)
```

The active calculation date is initialized from `datetime.today().date()`.

## 📅 Calendar and Fiscal Calculations

```python
fy.calendar_day_of_year()
fy.calendar_days_in_year()
fy.calendar_days_elapsed()
fy.calendar_days_remaining()
fy.calendar_months_elapsed()
fy.calendar_months_remaining()
fy.calendar_percent_elapsed()

fy.fiscal_day_of_year()
fy.fiscal_days_in_year()
fy.fiscal_month_number()
fy.fiscal_days_elapsed()
fy.fiscal_days_remaining()
fy.fiscal_months_elapsed()
fy.fiscal_months_remaining()
fy.fiscal_percent_elapsed()
```

The elapsed-day methods exclude the current date. The day-of-year methods are one-based.

## 🚀 Range Utilities

Range calculations are inclusive of both `start` and `end`.

```python
start = date(2026, 7, 1)
end = date(2026, 7, 31)

weekend_count = fy.count_weekends(start, end)
holiday_count = fy.count_holidays(start, end)
workday_count = fy.count_workdays(start, end)
```

Use actual holiday dates instead of observed dates when required:

```python
holiday_count = fy.count_holidays(
    start,
    end,
    use_observed=False,
)

workday_count = fy.count_workdays(
    start,
    end,
    use_observed=False,
)
```

A range whose start date is later than its end date returns `0`.

## 🎉 Fiscal-Year Holiday Values

The `FiscalYear.holidays` property returns the holiday columns stored in the matching
`FederalHolidays` row. `ID` and `FiscalYear` are excluded.

```python
holiday_values = fy.holidays

# Example structure:
[
    {"ColumbusDay": "10/13/2025"},
    {"VeteransDay": "11/11/2025"},
    {"ThanksgivingDay": "11/27/2025"},
]
```

Null database values are returned as empty strings.

## ⚡ Federal Holiday Operations

`FederalHoliday` loads one `FederalHolidays` row for the requested fiscal year.

```python
holidays = FederalHoliday("2026")

holidays.fiscal_year
holidays.independence_day
holidays.labor_day
```

Return actual and observed dates by holiday name:

```python
holiday_map = holidays.holidays()

independence_day = holiday_map["Independence Day"]

independence_day["actual"]
independence_day["observed"]
```

Check holiday and weekend membership:

```python
holidays.is_holiday(date(2026, 7, 4))
holidays.is_holiday(date(2026, 7, 3), observed=True)
holidays.is_holiday(date(2026, 7, 4), observed=False)

holidays.is_weekend(date(2026, 7, 4))
```

Calculate an observed date directly:

```python
observed = holidays.observed_date(date(2026, 7, 4))
```

Observation rules are:

- Saturday holiday → preceding Friday
- Sunday holiday → following Monday
- Weekday holiday → unchanged

## 🧭 Bounds and Year Checks

```python
calendar_start, calendar_end = fy.calendar_bounds()
fiscal_start, fiscal_end = fy.fiscal_bounds()

fy.is_fiscal_start_year()
fy.is_fiscal_end_year()
fy.is_calendar_start_year()
fy.is_calendar_end_date()
```

The current implementation defines these checks as follows:

- `is_fiscal_start_year()` compares the year of `current_date` with the year of `start_date`.
- `is_fiscal_end_year()` compares the year of `current_date` with the year of `end_date`.
- `is_calendar_start_year()` compares the year of `current_date` with the year of `cy_start_date`.
- `is_calendar_end_date()` tests whether `current_date` equals December 31 of the active calendar
  year.

## 📦 Dictionary Exports

Export the mapped fiscal-year record:

```python
fiscal_record = fy.to_dict()
```

The result contains:

```text
FiscalYear
BPOA
EPOA
StartDate
EndDate
ExpirationDate
CancellationDate
Weekdays
Weekends
Workdays
CompensableDays
CompensableHours
Type
Availability
```

Export the mapped federal-holiday record:

```python
holiday_record = holidays.to_dict()
```

<a id="api-overview"></a>

## 🧠 API Overview

### Public package exports

```python
from tempus import DB, FederalHoliday, FiscalYear, throw_if, to_date
```

### `DB`

- `create_connection() -> sqlite3.Connection`
- `query_year(name, fy, bpoa, epoa) -> pandas.DataFrame`
- `query_holiday(name, fy) -> pandas.DataFrame`

### `FiscalYear`

- `holidays -> list[dict[str, str]]`
- `calendar_day_of_year() -> int`
- `calendar_days_in_year() -> int`
- `calendar_days_elapsed() -> int`
- `calendar_days_remaining() -> int`
- `calendar_months_elapsed() -> int`
- `calendar_months_remaining() -> int`
- `calendar_percent_elapsed() -> float`
- `fiscal_day_of_year() -> int`
- `fiscal_days_in_year() -> int`
- `fiscal_month_number() -> int`
- `fiscal_days_elapsed() -> int`
- `fiscal_days_remaining() -> int`
- `fiscal_months_elapsed() -> int`
- `fiscal_months_remaining() -> int`
- `fiscal_percent_elapsed() -> float`
- `count_weekends(start, end) -> int`
- `count_holidays(start, end, use_observed=True) -> int`
- `count_workdays(start, end, use_observed=True) -> int`
- `calendar_bounds() -> tuple[date, date]`
- `fiscal_bounds() -> tuple[date, date]`
- `is_fiscal_start_year() -> bool`
- `is_fiscal_end_year() -> bool`
- `is_calendar_start_year() -> bool`
- `is_calendar_end_date() -> bool`
- `to_dict() -> dict[str, object]`

### `FederalHoliday`

- `observed_date(value) -> date`
- `holidays() -> dict[str, dict[str, date]]`
- `is_holiday(when, observed=True) -> bool`
- `is_weekend(when) -> bool`
- `to_dict() -> dict[str, object]`

### Utility functions

- `throw_if(name, value) -> None`
- `to_date(value) -> date | None`

`to_date()` accepts `date`, `datetime`, ISO `YYYY-MM-DD` text, `MM/DD/YYYY` text, and
`MM/DD/YY` text. The values `""`, `NS`, `N/A`, `NA`, `NONE`, and `NULL` resolve to `None`.

<a id="design-notes"></a>

## 📝 Design Notes

- **Fiscal-year source of truth:** Fiscal boundaries and appropriation metadata are read from
  `BudgetFiscalYears`; they are not generated solely from a supplied date.
- **Holiday source of truth:** Federal holiday dates are read from `FederalHolidays`.
- **Current date:** Calendar and fiscal progress calculations use the date captured when
  `FiscalYear` is instantiated.
- **Observed dates:** Weekend observation rules are calculated in Python from the stored actual
  holiday dates.
- **Parameterized queries:** Fiscal-year values and availability bounds are passed to SQLite as
  query parameters.
- **Approved tables:** Queries reject table names not present in `cfg.TABLES`.
- **No silent multi-row selection:** Queries require exactly one matching database row.
- **No long-term cache:** Query results are retained only on the active object as pandas
  `DataFrame` state.

<a id="roadmap"></a>

## 🏁 Roadmap

- Fiscal week and ISO week helpers
- Optional state and local holiday overlays
- Command-line interface for fiscal and holiday queries
- Additional pandas transformations for fiscal reporting
- Explicit calculation-date injection for historical or forecast analysis

<a id="license"></a>

## 📜 [License](https://github.com/is-leeroy-jenkins/Tempus/blob/master/LICENSE.txt)

MIT © 2022 Terry D. Eppler
