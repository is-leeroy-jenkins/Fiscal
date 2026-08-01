# tempus User Guide

![](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/images/github/project_tempus.png)

<p align="center">
  <a href="#installation">Installation</a>
  &nbsp;&bull;&nbsp;
  <a href="#configuration">Configuration</a>
  &nbsp;&bull;&nbsp;
  <a href="#fiscalyear">FiscalYear</a>
  &nbsp;&bull;&nbsp;
  <a href="#federalholiday">FederalHoliday</a>
  &nbsp;&bull;&nbsp;
  <a href="#calendar-rendering">Calendar Rendering</a>
  &nbsp;&bull;&nbsp;
  <a href="#recipes">Recipes</a>
  &nbsp;&bull;&nbsp;
  <a href="#api-reference">API Reference</a>
</p>

> Database-backed federal fiscal-year, calendar, workday, weekend, holiday, and calendar-rendering utilities for Python.

<a id="installation"></a>

## 🏗️ Installation

```bash
pip install tempus
```

```bash
pip install pandas boogr
```

Poetry:

```toml
[tool.poetry.dependencies]
tempus = "^1.0.0"
pandas = "*"
boogr = "*"
```

Imports:

```python
from datetime import date, datetime

from tempus import DB, FederalHoliday, FiscalYear, throw_if, to_date
```

Public exports:

```python
from tempus import (
    DB,
    FederalHoliday,
    FiscalYear,
    throw_if,
    to_date,
)
```

<a id="configuration"></a>

## ⚙️ Configuration

`config.py` must define the SQLite database path and the ordered table collection.

```python
DB_PATH: str = "resources/data/fiscal.db"

TABLES: list[str] = [
    "BudgetFiscalYears",
    "FederalHolidays",
]
```

Table order:

| Index | Table |
|---:|---|
| `0` | `BudgetFiscalYears` |
| `1` | `FederalHolidays` |

Each fiscal-year query must return exactly one row.

### `BudgetFiscalYears`

Required columns:

| Column | Value |
|---|---|
| `ID` | Database row identifier |
| `FiscalYear` | Fiscal-year label |
| `BPOA` | Beginning period of availability |
| `EPOA` | Ending period of availability |
| `StartDate` | Fiscal-year start date |
| `EndDate` | Fiscal-year end date |
| `ExpirationDate` | Appropriation expiration date or sentinel |
| `CancellationDate` | Appropriation cancellation date or sentinel |
| `Weekdays` | Stored weekday count |
| `Weekends` | Stored weekend count |
| `Workdays` | Stored workday count |
| `CompensableDays` | Stored compensable-day count |
| `CompensableHours` | Stored compensable-hour count |
| `Type` | Appropriation type |
| `Availability` | Availability description |

Example schema:

```sql
CREATE TABLE BudgetFiscalYears
(
    ID INTEGER PRIMARY KEY,
    FiscalYear TEXT NOT NULL,
    BPOA TEXT NOT NULL,
    EPOA TEXT NOT NULL,
    StartDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    ExpirationDate TEXT,
    CancellationDate TEXT,
    Weekdays INTEGER NOT NULL,
    Weekends INTEGER NOT NULL,
    Workdays REAL NOT NULL,
    CompensableDays REAL NOT NULL,
    CompensableHours REAL NOT NULL,
    Type TEXT NOT NULL,
    Availability TEXT NOT NULL,
    UNIQUE (FiscalYear, BPOA, EPOA)
);
```

Example row:

```sql
INSERT INTO BudgetFiscalYears
(
    ID,
    FiscalYear,
    BPOA,
    EPOA,
    StartDate,
    EndDate,
    ExpirationDate,
    CancellationDate,
    Weekdays,
    Weekends,
    Workdays,
    CompensableDays,
    CompensableHours,
    Type,
    Availability
)
VALUES
(
    1,
    '2026',
    '2026',
    '2026',
    '2025-10-01',
    '2026-09-30',
    'NS',
    'NS',
    261,
    104,
    250,
    250,
    2000,
    'Annual',
    'One-Year'
);
```

### `FederalHolidays`

Required columns:

| Column | Value |
|---|---|
| `ID` | Database row identifier |
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

Example schema:

```sql
CREATE TABLE FederalHolidays
(
    ID INTEGER PRIMARY KEY,
    FiscalYear TEXT NOT NULL UNIQUE,
    ColumbusDay TEXT NOT NULL,
    VeteransDay TEXT NOT NULL,
    ThanksgivingDay TEXT NOT NULL,
    ChristmasDay TEXT NOT NULL,
    NewYearsDay TEXT NOT NULL,
    MartinLutherKingDay TEXT NOT NULL,
    PresidentsDay TEXT NOT NULL,
    MemorialDay TEXT NOT NULL,
    JuneteenthDay TEXT NOT NULL,
    IndependenceDay TEXT NOT NULL,
    LaborDay TEXT NOT NULL
);
```

Example row:

```sql
INSERT INTO FederalHolidays
(
    ID,
    FiscalYear,
    ColumbusDay,
    VeteransDay,
    ThanksgivingDay,
    ChristmasDay,
    NewYearsDay,
    MartinLutherKingDay,
    PresidentsDay,
    MemorialDay,
    JuneteenthDay,
    IndependenceDay,
    LaborDay
)
VALUES
(
    1,
    '2026',
    '2025-10-13',
    '2025-11-11',
    '2025-11-27',
    '2025-12-25',
    '2026-01-01',
    '2026-01-19',
    '2026-02-16',
    '2026-05-25',
    '2026-06-19',
    '2026-07-04',
    '2026-09-07'
);
```

### Supported date values

`to_date()` accepts:

```python
date(2026, 7, 4)
datetime(2026, 7, 4, 12, 30)
"2026-07-04"
"07/04/2026"
"07/04/26"
```

Database sentinels resolve to `None`:

```python
to_date(None)
to_date("")
to_date("NS")
to_date("N/A")
to_date("NA")
to_date("NONE")
to_date("NULL")
```

Example:

```python
from tempus import to_date

value = to_date("2026-07-04")

assert value == date(2026, 7, 4)
```

Invalid date text raises `ValueError`:

```python
to_date("July 4, 2026")
```

Unsupported types raise `TypeError`:

```python
to_date(20260704)
```

### Required-value validation

```python
from tempus import throw_if

throw_if("fiscal_year", "2026")
throw_if("dates", [date(2026, 1, 1)])
```

The following values raise `ValueError`:

```python
throw_if("value", None)
throw_if("value", "")
throw_if("value", "   ")
throw_if("value", [])
throw_if("value", ())
throw_if("value", {})
throw_if("value", set())
```

<a id="fiscalyear"></a>

## 📅 `FiscalYear`

### Construction

Single-year availability:

```python
from tempus import FiscalYear

fy = FiscalYear("2026")
```

Equivalent keyword construction:

```python
fy = FiscalYear(
    fy="2026",
)
```

Multi-year availability:

```python
fy = FiscalYear(
    fy="2026",
    bpoa="2024",
    epoa="2026",
)
```

When `bpoa` or `epoa` is empty, the constructor uses `fy`.

```python
fy = FiscalYear(
    fy="2026",
    bpoa="",
    epoa="",
)

assert fy.bpoa == "2026"
assert fy.epoa == "2026"
```

String representation:

```python
fy = FiscalYear("2026")

print(fy)
```

```text
2026
```

### Loaded fiscal-year values

```python
fy = FiscalYear("2026")

print(fy.id)
print(fy.fiscal_year)
print(fy.bpoa)
print(fy.epoa)
print(fy.start_date)
print(fy.end_date)
print(fy.expiration_date)
print(fy.cancellation_date)
print(fy.weekdays)
print(fy.weekends)
print(fy.workdays)
print(fy.compensable_days)
print(fy.compensable_hours)
print(fy.type)
print(fy.availability)
```

Example assertions:

```python
assert fy.fiscal_year == "2026"
assert fy.start_date == date(2025, 10, 1)
assert fy.end_date == date(2026, 9, 30)
```

### Dictionary export

```python
record = fy.to_dict()

print(record)
```

Returned keys:

```python
{
    "FiscalYear": fy.fiscal_year,
    "BPOA": fy.bpoa,
    "EPOA": fy.epoa,
    "StartDate": fy.start_date,
    "EndDate": fy.end_date,
    "ExpirationDate": fy.expiration_date,
    "CancellationDate": fy.cancellation_date,
    "Weekdays": fy.weekdays,
    "Weekends": fy.weekends,
    "Workdays": fy.workdays,
    "CompensableDays": fy.compensable_days,
    "CompensableHours": fy.compensable_hours,
    "Type": fy.type,
    "Availability": fy.availability,
}
```

### Fiscal-year holiday column values

`holidays` returns a list of one-item dictionaries using the database column names.

```python
holiday_values = fy.holidays

for holiday in holiday_values:
    print(holiday)
```

Example:

```python
[
    {"ColumbusDay": "2025-10-13"},
    {"VeteransDay": "2025-11-11"},
    {"ThanksgivingDay": "2025-11-27"},
    {"ChristmasDay": "2025-12-25"},
    {"NewYearsDay": "2026-01-01"},
    {"MartinLutherKingDay": "2026-01-19"},
    {"PresidentsDay": "2026-02-16"},
    {"MemorialDay": "2026-05-25"},
    {"JuneteenthDay": "2026-06-19"},
    {"IndependenceDay": "2026-07-04"},
    {"LaborDay": "2026-09-07"},
]
```

Convert the list to one dictionary:

```python
holiday_columns = {
    key: value
    for item in fy.holidays
    for key, value in item.items()
}
```

### Calendar-year calculations

```python
day_number = fy.calendar_day_of_year()
days_in_year = fy.calendar_days_in_year()
days_elapsed = fy.calendar_days_elapsed()
days_remaining = fy.calendar_days_remaining()
months_elapsed = fy.calendar_months_elapsed()
months_remaining = fy.calendar_months_remaining()
percent_elapsed = fy.calendar_percent_elapsed()
```

Formatted output:

```python
print(f"Calendar day: {fy.calendar_day_of_year():,}")
print(f"Calendar days elapsed: {fy.calendar_days_elapsed():,}")
print(f"Calendar days remaining: {fy.calendar_days_remaining():,}")
print(f"Calendar months elapsed: {fy.calendar_months_elapsed():,}")
print(f"Calendar months remaining: {fy.calendar_months_remaining():,}")
print(f"Calendar elapsed: {fy.calendar_percent_elapsed():.2f}%")
```

Calendar boundaries:

```python
calendar_start, calendar_end = fy.calendar_bounds()

print(calendar_start)
print(calendar_end)
```

Calendar-date checks:

```python
print(fy.is_calendar_start_year())
print(fy.is_calendar_end_date())
```

### Fiscal-year calculations

```python
fiscal_day = fy.fiscal_day_of_year()
fiscal_month = fy.fiscal_month_number()
days_in_fiscal_year = fy.fiscal_days_in_year()
days_elapsed = fy.fiscal_days_elapsed()
days_remaining = fy.fiscal_days_remaining()
months_elapsed = fy.fiscal_months_elapsed()
months_remaining = fy.fiscal_months_remaining()
percent_elapsed = fy.fiscal_percent_elapsed()
```

Formatted output:

```python
print(f"Fiscal day: {fy.fiscal_day_of_year():,}")
print(f"Fiscal month: {fy.fiscal_month_number()}")
print(f"Fiscal days elapsed: {fy.fiscal_days_elapsed():,}")
print(f"Fiscal days remaining: {fy.fiscal_days_remaining():,}")
print(f"Fiscal months elapsed: {fy.fiscal_months_elapsed():,}")
print(f"Fiscal months remaining: {fy.fiscal_months_remaining():,}")
print(f"Fiscal elapsed: {fy.fiscal_percent_elapsed():.2f}%")
```

Fiscal boundaries:

```python
fiscal_start, fiscal_end = fy.fiscal_bounds()

assert fiscal_start == fy.start_date
assert fiscal_end == fy.end_date
```

Fiscal-year checks:

```python
print(fy.is_fiscal_start_year())
print(fy.is_fiscal_end_year())
```

### Fiscal-month numbering

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

Month names:

```python
for fiscal_month in range(1, 13):
    print(
        fiscal_month,
        fy.fiscal_month_name(fiscal_month),
    )
```

Month boundaries:

```python
october_start, october_end = fy.fiscal_month_bounds(1)
september_start, september_end = fy.fiscal_month_bounds(12)

assert october_start == date(2025, 10, 1)
assert october_end == date(2025, 10, 31)
assert september_start == date(2026, 9, 1)
assert september_end == date(2026, 9, 30)
```

Days in each fiscal month:

```python
for fiscal_month in range(1, 13):
    print(
        fy.fiscal_month_name(fiscal_month),
        fy.fiscal_days_in_month(fiscal_month),
    )
```

Build a month summary:

```python
month_summary = {
    fy.fiscal_month_name(fiscal_month): {
        "Bounds": fy.fiscal_month_bounds(fiscal_month),
        "Days": fy.fiscal_days_in_month(fiscal_month),
        "Weekdays": fy.weekdays_in_month(fiscal_month),
        "Weekends": fy.weekends_in_month(fiscal_month),
    }
    for fiscal_month in range(1, 13)
}
```

### Fiscal-month week rows

Date matrix:

```python
weeks = fy.fiscal_month_calendar(1)

for week in weeks:
    print(week)
```

Each row contains seven `date` objects from Monday through Sunday. Dates from adjacent months remain in the first or final row.

Integer day matrix:

```python
weeks = fy.fiscal_month_weeks(1)

for week in weeks:
    print(week)
```

Example shape:

```python
[
    [0, 0, 1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10, 11, 12],
    [13, 14, 15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24, 25, 26],
    [27, 28, 29, 30, 31, 0, 0],
]
```

### Fiscal quarters

| Quarter | Fiscal Months | Calendar Months |
|---:|---|---|
| `1` | `1`–`3` | October–December |
| `2` | `4`–`6` | January–March |
| `3` | `7`–`9` | April–June |
| `4` | `10`–`12` | July–September |

Current fiscal quarter:

```python
quarter = fy.fiscal_quarter_number()
```

Quarter boundaries:

```python
q1_start, q1_end = fy.fiscal_quarter_bounds(1)
q4_start, q4_end = fy.fiscal_quarter_bounds(4)

assert q1_start == date(2025, 10, 1)
assert q1_end == date(2025, 12, 31)
assert q4_start == date(2026, 7, 1)
assert q4_end == date(2026, 9, 30)
```

Quarter day counts:

```python
for quarter in range(1, 5):
    start, end = fy.fiscal_quarter_bounds(quarter)
    days = fy.fiscal_days_in_quarter(quarter)

    print(
        f"Q{quarter}: {start} through {end} ({days} days)"
    )
```

Quarter summary:

```python
quarter_summary = {
    f"Q{quarter}": {
        "StartDate": fy.fiscal_quarter_bounds(quarter)[0],
        "EndDate": fy.fiscal_quarter_bounds(quarter)[1],
        "Days": fy.fiscal_days_in_quarter(quarter),
    }
    for quarter in range(1, 5)
}
```

### Weekday and weekend calculations

Count weekdays and weekends in one fiscal month:

```python
july_weekdays = fy.weekdays_in_month(10)
july_weekends = fy.weekends_in_month(10)
```

Count a specific weekday:

```python
import calendar

mondays = fy.weekday_occurrences(
    fiscal_month=1,
    weekday=calendar.MONDAY,
)

fridays = fy.weekday_occurrences(
    fiscal_month=1,
    weekday=calendar.FRIDAY,
)
```

Weekday constants:

```python
calendar.MONDAY
calendar.TUESDAY
calendar.WEDNESDAY
calendar.THURSDAY
calendar.FRIDAY
calendar.SATURDAY
calendar.SUNDAY
```

Current weekday name:

```python
print(fy.current_weekday_name())
```

Current calendar month name:

```python
print(fy.calendar_month_name())
```

### Week numbers and boundaries

ISO calendar week:

```python
iso_week = fy.calendar_week_number()
```

Fiscal week:

```python
fiscal_week = fy.fiscal_week_number()
```

Fiscal week bounds:

```python
week_start, week_end = fy.fiscal_week_bounds(1)

print(week_start)
print(week_end)
```

Final partial fiscal week:

```python
week_start, week_end = fy.fiscal_week_bounds(53)

assert week_start >= fy.start_date
assert week_end <= fy.end_date
```

### Leap-year calculations

Determine whether the represented fiscal year contains February 29:

```python
contains_leap_day = fy.contains_leap_day()
```

Count leap days across the BPOA-to-EPOA availability period:

```python
fy = FiscalYear(
    fy="2028",
    bpoa="2024",
    epoa="2028",
)

leap_days = fy.leap_days_in_availability()
```

### Inclusive range counts

```python
start = date(2026, 7, 1)
end = date(2026, 7, 31)

weekends = fy.count_weekends(start, end)
holidays = fy.count_holidays(start, end)
workdays = fy.count_workdays(start, end)
```

Observed holidays:

```python
observed_holidays = fy.count_holidays(
    start=start,
    end=end,
    use_observed=True,
)

observed_workdays = fy.count_workdays(
    start=start,
    end=end,
    use_observed=True,
)
```

Actual holidays:

```python
actual_holidays = fy.count_holidays(
    start=start,
    end=end,
    use_observed=False,
)

actual_workdays = fy.count_workdays(
    start=start,
    end=end,
    use_observed=False,
)
```

A reversed range returns zero for the count methods:

```python
assert fy.count_weekends(
    date(2026, 7, 31),
    date(2026, 7, 1),
) == 0
```

### Holiday names and dates between two dates

Observed dates:

```python
holidays = fy.holidays_between(
    start=date(2026, 1, 1),
    end=date(2026, 9, 30),
    use_observed=True,
)

for name, holiday_date in holidays.items():
    print(f"{holiday_date}: {name}")
```

Example:

```python
{
    "New Year's Day": "2026-01-01",
    "Birthday of Martin Luther King, Jr.": "2026-01-19",
    "Washington's Birthday": "2026-02-16",
    "Memorial Day": "2026-05-25",
    "Juneteenth National Independence Day": "2026-06-19",
    "Independence Day": "2026-07-03",
    "Labor Day": "2026-09-07",
}
```

Actual dates:

```python
holidays = fy.holidays_between(
    start=date(2026, 1, 1),
    end=date(2026, 9, 30),
    use_observed=False,
)
```

The range is clamped to the represented fiscal-year boundaries.

```python
holidays = fy.holidays_between(
    start=date(2020, 1, 1),
    end=date(2030, 12, 31),
)
```

A range completely outside the represented fiscal year returns an empty dictionary:

```python
holidays = fy.holidays_between(
    start=date(2024, 1, 1),
    end=date(2024, 12, 31),
)

assert holidays == {}
```

A start date later than the end date raises an error:

```python
fy.holidays_between(
    start=date(2026, 8, 1),
    end=date(2026, 7, 1),
)
```

### Remaining fiscal-year counts

```python
remaining_holidays = fy.holidays_remaining()
remaining_workdays = fy.workdays_remaining()
remaining_weekends = fy.weekends_remaining()
```

Actual-date mode:

```python
remaining_holidays = fy.holidays_remaining(
    use_observed=False,
)

remaining_workdays = fy.workdays_remaining(
    use_observed=False,
)
```

Future fiscal years begin at `start_date`. Completed fiscal years return zero.

```python
completed_fy = FiscalYear("2021")

assert completed_fy.holidays_remaining() == 0
assert completed_fy.workdays_remaining() == 0
assert completed_fy.weekends_remaining() == 0
```

### Fiscal-year date collections

All fiscal-year dates:

```python
dates = fy.fiscal_dates()

assert dates[0] == fy.start_date
assert dates[-1] == fy.end_date
assert len(dates) == fy.fiscal_days_in_year()
```

Weekdays:

```python
weekdays = fy.fiscal_weekdays()

assert all(day.weekday() < 5 for day in weekdays)
```

Weekend dates:

```python
weekends = fy.fiscal_weekends()

assert all(day.weekday() >= 5 for day in weekends)
```

Workdays using observed holidays:

```python
workdays = fy.fiscal_workdays(
    use_observed=True,
)
```

Workdays using actual holidays:

```python
workdays = fy.fiscal_workdays(
    use_observed=False,
)
```

Membership checks:

```python
target = date(2026, 7, 3)

is_workday = target in fy.fiscal_workdays()
is_weekend = target in fy.fiscal_weekends()
```

### Dates grouped by fiscal month

```python
months = fy.fiscal_calendar()

for month_name, dates in months.items():
    print(month_name, len(dates))
```

Example keys:

```python
[
    "October 2025",
    "November 2025",
    "December 2025",
    "January 2026",
    "February 2026",
    "March 2026",
    "April 2026",
    "May 2026",
    "June 2026",
    "July 2026",
    "August 2026",
    "September 2026",
]
```

### Counts grouped by fiscal month

Weekdays:

```python
weekdays = fy.weekdays_by_month()
```

Weekends:

```python
weekends = fy.weekends_by_month()
```

Workdays:

```python
workdays = fy.workdays_by_month(
    use_observed=True,
)
```

Holidays:

```python
holidays = fy.holidays_by_month(
    use_observed=True,
)
```

Combined monthly summary:

```python
weekdays = fy.weekdays_by_month()
weekends = fy.weekends_by_month()
workdays = fy.workdays_by_month()
holidays = fy.holidays_by_month()

summary = {
    month_name: {
        "Weekdays": weekdays[month_name],
        "Weekends": weekends[month_name],
        "Workdays": workdays[month_name],
        "Holidays": holidays[month_name],
    }
    for month_name in weekdays
}
```

Pandas summary:

```python
import pandas as pd

df_summary = pd.DataFrame.from_dict(
    summary,
    orient="index",
)

df_summary.index.name = "FiscalMonth"

print(df_summary)
```

<a id="federalholiday"></a>

## 🎌 `FederalHoliday`

### Construction

```python
from tempus import FederalHoliday

holiday = FederalHoliday("2026")
```

```python
print(holiday)
```

```text
2026
```

### Loaded dates

```python
print(holiday.columbus_day)
print(holiday.veterans_day)
print(holiday.thanksgiving_day)
print(holiday.christmas_day)
print(holiday.new_years_day)
print(holiday.martin_luther_king_day)
print(holiday.presidents_day)
print(holiday.memorial_day)
print(holiday.juneteenth_day)
print(holiday.independence_day)
print(holiday.labor_day)
```

### Actual and observed dates

```python
holidays = holiday.holidays()

for name, values in holidays.items():
    print(
        name,
        values["actual"],
        values["observed"],
    )
```

Returned shape:

```python
{
    "Independence Day": {
        "actual": date(2026, 7, 4),
        "observed": date(2026, 7, 3),
    }
}
```

### Observed-date calculation

Saturday holiday:

```python
actual = date(2026, 7, 4)
observed = holiday.observed_date(actual)

assert observed == date(2026, 7, 3)
```

Sunday holiday:

```python
actual = date(2027, 7, 4)
observed = holiday.observed_date(actual)

assert observed == date(2027, 7, 5)
```

Weekday holiday:

```python
actual = date(2026, 12, 25)
observed = holiday.observed_date(actual)

assert observed == actual
```

### Holiday checks

Observed-date check:

```python
is_holiday = holiday.is_holiday(
    when=date(2026, 7, 3),
    observed=True,
)

assert is_holiday is True
```

Actual-date check:

```python
is_holiday = holiday.is_holiday(
    when=date(2026, 7, 4),
    observed=False,
)

assert is_holiday is True
```

Datetime input:

```python
is_holiday = holiday.is_holiday(
    when=datetime(2026, 7, 4, 12, 0),
    observed=False,
)
```

### Weekend checks

```python
assert holiday.is_weekend(
    date(2026, 7, 4),
) is True

assert holiday.is_weekend(
    date(2026, 7, 6),
) is False
```

### Dictionary export

```python
record = holiday.to_dict()

print(record)
```

<a id="calendar-rendering"></a>

## 🗓️ Calendar Rendering

### Classified fiscal-month matrix

```python
matrix = fy.fiscal_month_matrix(
    fiscal_month=10,
    use_observed=True,
)
```

Matrix hierarchy:

```text
month
└── weeks
    └── seven day dictionaries
```

Day dictionary fields:

| Field | Type | Value |
|---|---|---|
| `Date` | `date` | Calendar date |
| `Day` | `int` | Day number |
| `Weekday` | `str` | Full weekday name |
| `FiscalMonth` | `int` | Fiscal-month number |
| `FiscalQuarter` | `int` | Fiscal-quarter number |
| `IsSelectedMonth` | `bool` | Date belongs to the selected calendar month |
| `IsFiscalYear` | `bool` | Date belongs to the represented fiscal year |
| `IsCurrentDate` | `bool` | Date equals `current_date` |
| `IsWeekend` | `bool` | Saturday or Sunday |
| `IsHoliday` | `bool` | Selected holiday date |
| `IsWorkday` | `bool` | Selected-month weekday excluding selected holidays |
| `HolidayName` | `str` | Federal holiday name |
| `HolidayType` | `str` | `actual`, `observed`, or empty |

Inspect one day:

```python
for week in matrix:
    for payload in week:
        if payload["Date"] == date(2026, 7, 3):
            print(payload)
```

Example observed-holiday payload:

```python
{
    "Date": date(2026, 7, 3),
    "Day": 3,
    "Weekday": "Friday",
    "FiscalMonth": 10,
    "FiscalQuarter": 4,
    "IsSelectedMonth": True,
    "IsFiscalYear": True,
    "IsCurrentDate": False,
    "IsWeekend": False,
    "IsHoliday": True,
    "IsWorkday": False,
    "HolidayName": "Independence Day",
    "HolidayType": "observed",
}
```

Filter workdays:

```python
workdays = [
    payload["Date"]
    for week in matrix
    for payload in week
    if payload["IsWorkday"]
]
```

Filter holidays:

```python
holiday_rows = [
    payload
    for week in matrix
    for payload in week
    if payload["IsHoliday"]
]
```

Create a DataFrame:

```python
import pandas as pd

df_month = pd.DataFrame(
    payload
    for week in matrix
    for payload in week
    if payload["IsSelectedMonth"]
)

print(df_month)
```

### Classified fiscal-year matrix

```python
year_matrix = fy.fiscal_year_matrix(
    use_observed=True,
)
```

Iterate through all months:

```python
for month_name, month_matrix in year_matrix.items():
    selected_dates = [
        payload["Date"]
        for week in month_matrix
        for payload in week
        if payload["IsSelectedMonth"]
    ]

    print(month_name, len(selected_dates))
```

Flatten the fiscal year:

```python
rows = [
    payload
    for month_matrix in year_matrix.values()
    for week in month_matrix
    for payload in week
    if payload["IsSelectedMonth"]
]
```

DataFrame:

```python
df_fiscal_calendar = pd.DataFrame(rows)

df_fiscal_calendar = df_fiscal_calendar.sort_values(
    by="Date",
)

print(df_fiscal_calendar)
```

### Text fiscal month

```python
text = fy.format_fiscal_month(
    fiscal_month=1,
)

print(text)
```

Custom day width and line spacing:

```python
text = fy.format_fiscal_month(
    fiscal_month=1,
    width=3,
    lines=1,
)

print(text)
```

### Text fiscal quarter

```python
text = fy.format_fiscal_quarter(
    quarter=1,
)

print(text)
```

Custom spacing:

```python
text = fy.format_fiscal_quarter(
    quarter=4,
    width=3,
    lines=1,
    spacing=8,
)

print(text)
```

### Text fiscal year

```python
text = fy.format_fiscal_year()

print(text)
```

Four months per row:

```python
text = fy.format_fiscal_year(
    width=3,
    lines=1,
    spacing=6,
    columns=4,
)

print(text)
```

Write text output:

```python
from pathlib import Path

Path("fiscal-year-2026.txt").write_text(
    fy.format_fiscal_year(),
    encoding="utf-8",
)
```

### HTML fiscal month

```python
html = fy.format_fiscal_month_html(
    fiscal_month=10,
    with_year=True,
    use_observed=True,
)
```

Without the calendar year in the caption:

```python
html = fy.format_fiscal_month_html(
    fiscal_month=10,
    with_year=False,
)
```

Actual-date mode:

```python
html = fy.format_fiscal_month_html(
    fiscal_month=10,
    use_observed=False,
)
```

Write one month:

```python
Path("july-2026.html").write_text(
    html,
    encoding="utf-8",
)
```

### HTML fiscal quarter

```python
html = fy.format_fiscal_quarter_html(
    quarter=4,
    use_observed=True,
)

Path("fiscal-quarter-4.html").write_text(
    html,
    encoding="utf-8",
)
```

### HTML fiscal year

```python
html = fy.format_fiscal_year_html(
    columns=3,
    use_observed=True,
)

Path("fiscal-year-2026-fragment.html").write_text(
    html,
    encoding="utf-8",
)
```

The return value is an HTML fragment containing the fiscal-year calendar tables.

### Standalone HTML page

```python
page = fy.format_fiscal_year_page(
    columns=3,
    css="calendar.css",
    encoding="utf-8",
    use_observed=True,
)

Path("fiscal-year-2026.html").write_bytes(page)
```

The return type is `bytes`.

```python
assert isinstance(page, bytes)
```

### Direct HTML export

```python
fy.save_fiscal_year_html(
    path="fiscal-year-2026.html",
    columns=3,
    use_observed=True,
)
```

### HTML classes

| Class | Meaning |
|---|---|
| `fiscal-calendar` | Calendar table |
| `outside-month` | Leading or trailing date outside the selected month |
| `fiscal-day` | Date belongs to the represented fiscal year |
| `current-date` | Date equals `current_date` |
| `weekend` | Saturday or Sunday |
| `workday` | Weekday excluding the selected holiday date |
| `holiday` | Federal holiday |
| `observed-holiday` | Weekend-adjusted holiday |
| `fiscal-year-start` | Fiscal-year start date |
| `fiscal-year-end` | Fiscal-year end date |
| `expiration-date` | Appropriation expiration date |
| `cancellation-date` | Appropriation cancellation date |
| `holiday-name` | Holiday-name element |
| `mon`–`sun` | Weekday class |

### Example stylesheet

```css
:root
{
    color-scheme: dark;
    font-family: Arial, Helvetica, sans-serif;
    background: #101418;
    color: #f2f4f7;
}

body
{
    margin: 0;
    padding: 2rem;
    background: #101418;
}

.fiscal-year-calendar,
.fiscal-quarter-calendar
{
    display: grid;
    grid-template-columns: repeat(3, minmax(18rem, 1fr));
    gap: 1.25rem;
}

.fiscal-calendar
{
    width: 100%;
    border-collapse: collapse;
    background: #182028;
    border: 1px solid #394653;
}

.fiscal-calendar caption
{
    padding: 0.75rem;
    font-size: 1.1rem;
    font-weight: 700;
    background: #202b36;
}

.fiscal-calendar th,
.fiscal-calendar td
{
    border: 1px solid #394653;
    padding: 0.5rem;
    text-align: center;
    vertical-align: top;
}

.fiscal-calendar th
{
    background: #263442;
}

.fiscal-calendar td
{
    min-width: 3rem;
    height: 3.5rem;
}

.outside-month
{
    opacity: 0.3;
}

.weekend
{
    background: #252f38;
}

.workday
{
    background: #17241d;
}

.holiday
{
    background: #4a2d2d;
    font-weight: 700;
}

.observed-holiday
{
    outline: 2px solid #d6a84b;
    outline-offset: -2px;
}

.current-date
{
    box-shadow: inset 0 0 0 3px #61dafb;
}

.fiscal-year-start,
.fiscal-year-end
{
    border: 2px solid #d6a84b !important;
}

.expiration-date
{
    background: #4a3f20;
}

.cancellation-date
{
    background: #522424;
}

.holiday-name
{
    display: block;
    margin-top: 0.25rem;
    font-size: 0.7rem;
    line-height: 1.1;
}
```

Responsive layout:

```css
@media (max-width: 1100px)
{
    .fiscal-year-calendar,
    .fiscal-quarter-calendar
    {
        grid-template-columns: repeat(2, minmax(18rem, 1fr));
    }
}

@media (max-width: 720px)
{
    .fiscal-year-calendar,
    .fiscal-quarter-calendar
    {
        grid-template-columns: 1fr;
    }

    body
    {
        padding: 0.75rem;
    }
}
```

<a id="recipes"></a>

## 🧪 Recipes

### Fiscal-year scorecard

```python
fy = FiscalYear("2026")

scorecard = {
    "FiscalYear": fy.fiscal_year,
    "StartDate": fy.start_date,
    "EndDate": fy.end_date,
    "FiscalDay": fy.fiscal_day_of_year(),
    "FiscalMonth": fy.fiscal_month_number(),
    "FiscalQuarter": fy.fiscal_quarter_number(),
    "DaysElapsed": fy.fiscal_days_elapsed(),
    "DaysRemaining": fy.fiscal_days_remaining(),
    "PercentElapsed": round(
        fy.fiscal_percent_elapsed(),
        2,
    ),
    "HolidaysRemaining": fy.holidays_remaining(),
    "WorkdaysRemaining": fy.workdays_remaining(),
    "WeekendsRemaining": fy.weekends_remaining(),
}

print(scorecard)
```

### Fiscal-year progress statement

```python
message = (
    f"FY {fy.fiscal_year} is "
    f"{fy.fiscal_percent_elapsed():.2f}% complete. "
    f"{fy.fiscal_days_remaining():,} calendar days, "
    f"{fy.workdays_remaining():,} workdays, and "
    f"{fy.holidays_remaining():,} federal holidays remain."
)

print(message)
```

### Quarter execution calendar

```python
quarter = 4
quarter_start, quarter_end = fy.fiscal_quarter_bounds(quarter)

quarter_data = {
    "Quarter": f"Q{quarter}",
    "StartDate": quarter_start,
    "EndDate": quarter_end,
    "CalendarDays": fy.fiscal_days_in_quarter(quarter),
    "Weekends": fy.count_weekends(
        quarter_start,
        quarter_end,
    ),
    "Holidays": fy.count_holidays(
        quarter_start,
        quarter_end,
    ),
    "Workdays": fy.count_workdays(
        quarter_start,
        quarter_end,
    ),
}

print(quarter_data)
```

### Monthly execution table

```python
import pandas as pd

df_months = pd.DataFrame(
    [
        {
            "FiscalMonth": fiscal_month,
            "Month": fy.fiscal_month_name(fiscal_month),
            "StartDate": fy.fiscal_month_bounds(fiscal_month)[0],
            "EndDate": fy.fiscal_month_bounds(fiscal_month)[1],
            "CalendarDays": fy.fiscal_days_in_month(fiscal_month),
            "Weekdays": fy.weekdays_in_month(fiscal_month),
            "Weekends": fy.weekends_in_month(fiscal_month),
            "Workdays": fy.workdays_by_month()[
                fy.fiscal_month_bounds(fiscal_month)[0].strftime("%B %Y")
            ],
        }
        for fiscal_month in range(1, 13)
    ]
)

print(df_months)
```

### Holiday report

```python
holidays = fy.holidays_between(
    start=fy.start_date,
    end=fy.end_date,
    use_observed=True,
)

df_holidays = pd.DataFrame(
    [
        {
            "Holiday": name,
            "Date": holiday_date,
        }
        for name, holiday_date in holidays.items()
    ]
)

print(df_holidays)
```

### Actual-versus-observed holiday comparison

```python
federal_holiday = FederalHoliday(fy.fiscal_year)

comparison = [
    {
        "Holiday": name,
        "ActualDate": payload["actual"],
        "ObservedDate": payload["observed"],
        "Adjusted": payload["actual"] != payload["observed"],
    }
    for name, payload in federal_holiday.holidays().items()
]

df_comparison = pd.DataFrame(comparison)

print(df_comparison)
```

### Validate stored annual totals

```python
calculated_days = fy.fiscal_days_in_year()
calculated_weekdays = len(fy.fiscal_weekdays())
calculated_weekends = len(fy.fiscal_weekends())
calculated_workdays = len(fy.fiscal_workdays())

validation = {
    "DaysBalanced": (
        calculated_weekdays + calculated_weekends
        == calculated_days
    ),
    "StoredWeekdaysMatch": (
        calculated_weekdays == fy.weekdays
    ),
    "StoredWeekendsMatch": (
        calculated_weekends == fy.weekends
    ),
    "StoredWorkdaysMatch": (
        calculated_workdays == int(fy.workdays)
    ),
}

print(validation)
```

### Find all Friday holidays

```python
holiday = FederalHoliday(fy.fiscal_year)

friday_holidays = {
    name: payload
    for name, payload in holiday.holidays().items()
    if payload["observed"].weekday() == 4
}

print(friday_holidays)
```

### Find the next observed holiday

```python
today = fy.current_date

future_holidays = [
    (name, payload["observed"])
    for name, payload in FederalHoliday(
        fy.fiscal_year,
    ).holidays().items()
    if payload["observed"] >= today
]

future_holidays.sort(
    key=lambda item: item[1],
)

next_holiday = (
    future_holidays[0]
    if future_holidays
    else None
)

print(next_holiday)
```

### Determine whether a date is a workday

```python
target = date(2026, 7, 3)
holiday = FederalHoliday(fy.fiscal_year)

is_workday = (
    target.weekday() < 5
    and not holiday.is_holiday(
        target,
        observed=True,
    )
)

print(is_workday)
```

Using the fiscal workday collection:

```python
is_workday = target in fy.fiscal_workdays()
```

### Get workdays in a date range

```python
start = date(2026, 7, 1)
end = date(2026, 7, 31)

workdays = [
    current
    for current in fy.fiscal_workdays()
    if start <= current <= end
]

print(workdays)
```

### Create a calendar DataFrame for one quarter

```python
quarter = 4
quarter_start, quarter_end = fy.fiscal_quarter_bounds(quarter)

rows = [
    payload
    for month_matrix in fy.fiscal_year_matrix().values()
    for week in month_matrix
    for payload in week
    if (
        payload["IsSelectedMonth"]
        and quarter_start <= payload["Date"] <= quarter_end
    )
]

df_quarter = pd.DataFrame(rows).sort_values(
    by="Date",
)

print(df_quarter)
```

### Export one fiscal quarter to CSV

```python
df_quarter.to_csv(
    "fiscal-quarter-4.csv",
    index=False,
)
```

### Export the complete fiscal calendar to CSV

```python
rows = [
    payload
    for month_matrix in fy.fiscal_year_matrix().values()
    for week in month_matrix
    for payload in week
    if payload["IsSelectedMonth"]
]

df_calendar = pd.DataFrame(rows).sort_values(
    by="Date",
)

df_calendar.to_csv(
    "fiscal-year-2026.csv",
    index=False,
)
```

### Export fiscal calendar data to JSON

```python
json_text = df_calendar.to_json(
    orient="records",
    date_format="iso",
    indent=2,
)

Path("fiscal-year-2026.json").write_text(
    json_text,
    encoding="utf-8",
)
```

### Generate text and HTML calendars together

```python
output = Path("output")
output.mkdir(
    parents=True,
    exist_ok=True,
)

(output / "fiscal-year-2026.txt").write_text(
    fy.format_fiscal_year(),
    encoding="utf-8",
)

fy.save_fiscal_year_html(
    path=str(output / "fiscal-year-2026.html"),
    columns=3,
    use_observed=True,
)
```

### Generate all monthly HTML calendars

```python
output = Path("output/months")
output.mkdir(
    parents=True,
    exist_ok=True,
)

for fiscal_month in range(1, 13):
    month_start, _ = fy.fiscal_month_bounds(
        fiscal_month,
    )

    filename = month_start.strftime(
        "%Y-%m.html",
    )

    html = fy.format_fiscal_month_html(
        fiscal_month=fiscal_month,
        with_year=True,
        use_observed=True,
    )

    (output / filename).write_text(
        html,
        encoding="utf-8",
    )
```

### Compare two fiscal years

```python
fy_2025 = FiscalYear("2025")
fy_2026 = FiscalYear("2026")

comparison = pd.DataFrame(
    [
        {
            "FiscalYear": fy_2025.fiscal_year,
            "Weekdays": fy_2025.weekdays,
            "Weekends": fy_2025.weekends,
            "Workdays": fy_2025.workdays,
            "CompensableDays": fy_2025.compensable_days,
            "CompensableHours": fy_2025.compensable_hours,
        },
        {
            "FiscalYear": fy_2026.fiscal_year,
            "Weekdays": fy_2026.weekdays,
            "Weekends": fy_2026.weekends,
            "Workdays": fy_2026.workdays,
            "CompensableDays": fy_2026.compensable_days,
            "CompensableHours": fy_2026.compensable_hours,
        },
    ]
)

print(comparison)
```

### Batch-load fiscal years

```python
fiscal_years = [
    FiscalYear(str(year))
    for year in range(2021, 2027)
]
```

Create a summary DataFrame:

```python
df_fiscal_years = pd.DataFrame(
    fy_item.to_dict()
    for fy_item in fiscal_years
)

print(df_fiscal_years)
```

### Error handling

```python
from boogr import Error

try:
    fy = FiscalYear("2099")
except Error as ex:
    print(ex.module)
    print(ex.cause)
    print(ex.method)
    raise
```

Invalid fiscal month:

```python
try:
    fy.fiscal_month_bounds(13)
except Error as ex:
    print(ex)
```

Invalid quarter:

```python
try:
    fy.fiscal_quarter_bounds(5)
except Error as ex:
    print(ex)
```

Invalid fiscal week:

```python
try:
    fy.fiscal_week_bounds(0)
except Error as ex:
    print(ex)
```

<a id="api-reference"></a>

## 📚 API Reference

### `DB`

| Member | Signature |
|---|---|
| `create_connection` | `create_connection() -> sqlite3.Connection` |
| `query_year` | `query_year(name, fy, bpoa, epoa) -> pandas.DataFrame` |
| `query_holiday` | `query_holiday(name, fy) -> pandas.DataFrame` |

### `FiscalYear`

#### Construction and export

| Member | Signature |
|---|---|
| `FiscalYear` | `FiscalYear(fy, bpoa='', epoa='')` |
| `holidays` | `holidays -> List[Dict[str, str]]` |
| `to_dict` | `to_dict() -> Dict[str, object]` |

#### Calendar calculations

| Member | Signature |
|---|---|
| `calendar_day_of_year` | `calendar_day_of_year() -> int` |
| `calendar_days_in_year` | `calendar_days_in_year() -> int` |
| `calendar_days_elapsed` | `calendar_days_elapsed() -> int` |
| `calendar_days_remaining` | `calendar_days_remaining() -> int` |
| `calendar_months_elapsed` | `calendar_months_elapsed() -> int` |
| `calendar_months_remaining` | `calendar_months_remaining() -> int` |
| `calendar_percent_elapsed` | `calendar_percent_elapsed() -> float` |
| `calendar_bounds` | `calendar_bounds() -> Tuple[date, date]` |
| `calendar_week_number` | `calendar_week_number() -> int` |
| `calendar_month_name` | `calendar_month_name() -> str` |
| `current_weekday_name` | `current_weekday_name() -> str` |
| `is_calendar_start_year` | `is_calendar_start_year() -> bool` |
| `is_calendar_end_date` | `is_calendar_end_date() -> bool` |

#### Fiscal calculations

| Member | Signature |
|---|---|
| `fiscal_day_of_year` | `fiscal_day_of_year() -> int` |
| `fiscal_days_in_year` | `fiscal_days_in_year() -> int` |
| `fiscal_days_elapsed` | `fiscal_days_elapsed() -> int` |
| `fiscal_days_remaining` | `fiscal_days_remaining() -> int` |
| `fiscal_month_number` | `fiscal_month_number() -> int` |
| `fiscal_months_elapsed` | `fiscal_months_elapsed() -> int` |
| `fiscal_months_remaining` | `fiscal_months_remaining() -> int` |
| `fiscal_percent_elapsed` | `fiscal_percent_elapsed() -> float` |
| `fiscal_bounds` | `fiscal_bounds() -> Tuple[date, date]` |
| `fiscal_quarter_number` | `fiscal_quarter_number() -> int` |
| `fiscal_week_number` | `fiscal_week_number() -> int` |
| `fiscal_week_bounds` | `fiscal_week_bounds(fiscal_week) -> Tuple[date, date]` |
| `contains_leap_day` | `contains_leap_day() -> bool` |
| `leap_days_in_availability` | `leap_days_in_availability() -> int` |
| `is_fiscal_start_year` | `is_fiscal_start_year() -> bool` |
| `is_fiscal_end_year` | `is_fiscal_end_year() -> bool` |

#### Fiscal months and quarters

| Member | Signature |
|---|---|
| `fiscal_month_bounds` | `fiscal_month_bounds(fiscal_month) -> Tuple[date, date]` |
| `fiscal_days_in_month` | `fiscal_days_in_month(fiscal_month) -> int` |
| `fiscal_month_calendar` | `fiscal_month_calendar(fiscal_month) -> List[List[date]]` |
| `fiscal_month_weeks` | `fiscal_month_weeks(fiscal_month) -> List[List[int]]` |
| `fiscal_month_name` | `fiscal_month_name(fiscal_month) -> str` |
| `fiscal_quarter_bounds` | `fiscal_quarter_bounds(quarter) -> Tuple[date, date]` |
| `fiscal_days_in_quarter` | `fiscal_days_in_quarter(quarter) -> int` |
| `weekdays_in_month` | `weekdays_in_month(fiscal_month) -> int` |
| `weekends_in_month` | `weekends_in_month(fiscal_month) -> int` |
| `weekday_occurrences` | `weekday_occurrences(fiscal_month, weekday) -> int` |

#### Ranges and remaining counts

| Member | Signature |
|---|---|
| `count_weekends` | `count_weekends(start, end) -> int` |
| `count_holidays` | `count_holidays(start, end, use_observed=True) -> int` |
| `count_workdays` | `count_workdays(start, end, use_observed=True) -> int` |
| `holidays_between` | `holidays_between(start, end, use_observed=True) -> Dict[str, str]` |
| `holidays_remaining` | `holidays_remaining(use_observed=True) -> int` |
| `workdays_remaining` | `workdays_remaining(use_observed=True) -> int` |
| `weekends_remaining` | `weekends_remaining() -> int` |

#### Fiscal-year collections

| Member | Signature |
|---|---|
| `fiscal_dates` | `fiscal_dates() -> List[date]` |
| `fiscal_weekdays` | `fiscal_weekdays() -> List[date]` |
| `fiscal_weekends` | `fiscal_weekends() -> List[date]` |
| `fiscal_workdays` | `fiscal_workdays(use_observed=True) -> List[date]` |
| `fiscal_calendar` | `fiscal_calendar() -> Dict[str, List[date]]` |
| `weekdays_by_month` | `weekdays_by_month() -> Dict[str, int]` |
| `weekends_by_month` | `weekends_by_month() -> Dict[str, int]` |
| `workdays_by_month` | `workdays_by_month(use_observed=True) -> Dict[str, int]` |
| `holidays_by_month` | `holidays_by_month(use_observed=True) -> Dict[str, List[date]]` |

#### Calendar matrices

| Member | Signature |
|---|---|
| `fiscal_month_matrix` | `fiscal_month_matrix(fiscal_month, use_observed=True) -> List[List[Dict[str, object]]]` |
| `fiscal_year_matrix` | `fiscal_year_matrix(use_observed=True) -> Dict[str, List[List[Dict[str, object]]]]` |

#### Text rendering

| Member | Signature |
|---|---|
| `format_fiscal_month` | `format_fiscal_month(fiscal_month, width=2, lines=1) -> str` |
| `format_fiscal_quarter` | `format_fiscal_quarter(quarter, width=2, lines=1, spacing=6) -> str` |
| `format_fiscal_year` | `format_fiscal_year(width=2, lines=1, spacing=6, columns=3) -> str` |

#### HTML rendering and export

| Member | Signature |
|---|---|
| `format_fiscal_month_html` | `format_fiscal_month_html(fiscal_month, with_year=True, use_observed=True) -> str` |
| `format_fiscal_quarter_html` | `format_fiscal_quarter_html(quarter, use_observed=True) -> str` |
| `format_fiscal_year_html` | `format_fiscal_year_html(columns=3, use_observed=True) -> str` |
| `format_fiscal_year_page` | `format_fiscal_year_page(columns=3, css='calendar.css', encoding='utf-8', use_observed=True) -> bytes` |
| `save_fiscal_year_html` | `save_fiscal_year_html(path, columns=3, use_observed=True) -> None` |

### `FederalHoliday`

| Member | Signature |
|---|---|
| `FederalHoliday` | `FederalHoliday(fiscal_year)` |
| `observed_date` | `observed_date(value) -> date` |
| `holidays` | `holidays() -> Dict[str, Dict[str, date]]` |
| `is_holiday` | `is_holiday(when, observed=True) -> bool` |
| `is_weekend` | `is_weekend(when) -> bool` |
| `to_dict` | `to_dict() -> Dict[str, object]` |

### Utility functions

| Member | Signature |
|---|---|
| `throw_if` | `throw_if(name, value) -> None` |
| `to_date` | `to_date(value) -> Optional[date]` |
