###### fiscal

![](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/images/github/project_tempus.png)

<p align="left">
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
  <a href="https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/USER_GUIDE.md">User Guide</a>
  &nbsp;&bull;&nbsp;
  <a href="https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/DEVELOPER_GUIDE.md">Developer Guide</a>
  &nbsp;&bull;&nbsp;
  <a href="#license">License</a>
</p>

___

Fiscal is a Python framework for U.S. federal fiscal-year and calendar-year calculations, including fiscal months, quarters, and weeks; workdays and weekends; and actual and observed federal holidays.

<a id="features"></a>

## 📝 Features

- SQLite-backed fiscal-year and federal-holiday records
- Fiscal-year queries by `FiscalYear`, `BPOA`, and `EPOA`
- Calendar-year and fiscal-year progress calculations
- Fiscal-month boundaries, names, day counts, and week matrices
- Fiscal-quarter identification, boundaries, and day counts
- Calendar-week and fiscal-week calculations
- Weekday, weekend, and workday date collections
- Monthly weekday, weekend, workday, and holiday aggregations
- Actual and observed federal-holiday dates
- Inclusive weekend, holiday, and workday counts
- Holiday names and dates returned for a selected range
- Remaining fiscal-year holiday, workday, and weekend counts
- Leap-day detection for fiscal years and availability periods
- Fiscal-year and holiday dictionary exports
- Required-argument validation with `throw_if()`
- Operational exception wrapping with `boogr.Error`

<a id="installation"></a>

## 🏗️ Installation

```bash
pip install fiscal
```

```toml
[tool.poetry.dependencies]
fiscal = "^1.0.0"
```

```bash
pip install pandas boogr
```

<a id="configuration"></a>

## ⚙️ Configuration

```python
DB_PATH: str
TABLES: list[str]
```

```python
TABLES = [
    "BudgetFiscalYears",
    "FederalHolidays",
]
```

<a id="quick-start"></a>

## 🎯 Quick Start

```python
from datetime import date

from fiscal import FederalHoliday, FiscalYear
```

### Fiscal-Year Record

```python
fy = FiscalYear("2026")

fy.fiscal_year
fy.bpoa
fy.epoa
fy.start_date
fy.end_date
fy.expiration_date
fy.cancellation_date
fy.weekdays
fy.weekends
fy.workdays
fy.compensable_days
fy.compensable_hours
fy.type
fy.availability
```

Multi-year availability:

```python
fy = FiscalYear(
    fy="2026",
    bpoa="2024",
    epoa="2026",
)
```

### Calendar-Year Progress

```python
fy.calendar_day_of_year()
fy.calendar_days_in_year()
fy.calendar_days_elapsed()
fy.calendar_days_remaining()
fy.calendar_months_elapsed()
fy.calendar_months_remaining()
fy.calendar_percent_elapsed()
fy.calendar_bounds()
fy.calendar_week_number()
fy.calendar_month_name()
fy.current_weekday_name()
fy.is_calendar_start_year()
fy.is_calendar_end_date()
```

### Fiscal-Year Progress

```python
fy.fiscal_day_of_year()
fy.fiscal_days_in_year()
fy.fiscal_month_number()
fy.fiscal_days_elapsed()
fy.fiscal_days_remaining()
fy.fiscal_months_elapsed()
fy.fiscal_months_remaining()
fy.fiscal_percent_elapsed()
fy.fiscal_bounds()
fy.fiscal_week_number()
fy.is_fiscal_start_year()
fy.is_fiscal_end_year()
```

### Fiscal Months

Fiscal months are numbered from October through September.

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

```python
month_start, month_end = fy.fiscal_month_bounds(10)

month_name = fy.fiscal_month_name(10)
calendar_days = fy.fiscal_days_in_month(10)
weekdays = fy.weekdays_in_month(10)
weekends = fy.weekends_in_month(10)
```

Calendar-style week matrices:

```python
date_weeks = fy.fiscal_month_calendar(10)
number_weeks = fy.fiscal_month_weeks(10)
```

Count a specific weekday:

```python
import calendar

mondays = fy.weekday_occurrences(
    fiscal_month=10,
    weekday=calendar.MONDAY,
)
```

### Fiscal Quarters

```python
current_quarter = fy.fiscal_quarter_number()

quarter_start, quarter_end = fy.fiscal_quarter_bounds(4)
quarter_days = fy.fiscal_days_in_quarter(4)
```

| Quarter | Fiscal Months | Calendar Months |
|---:|---|---|
| `1` | `1`–`3` | October–December |
| `2` | `4`–`6` | January–March |
| `3` | `7`–`9` | April–June |
| `4` | `10`–`12` | July–September |

### Fiscal Weeks

```python
current_week = fy.fiscal_week_number()

week_start, week_end = fy.fiscal_week_bounds(
    fiscal_week=1,
)
```

### Range Utilities

```python
start = date(2026, 7, 1)
end = date(2026, 7, 31)

weekend_count = fy.count_weekends(start, end)
holiday_count = fy.count_holidays(start, end)
workday_count = fy.count_workdays(start, end)
```

Use actual holiday dates rather than observed dates:

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

Return holiday names and dates:

```python
holidays = fy.holidays_between(
    start=start,
    end=end,
    use_observed=True,
)

for name, holiday_date in holidays.items():
    print(f"{holiday_date}: {name}")
```

### Fiscal-Year Date Collections

```python
dates = fy.fiscal_dates()
weekdays = fy.fiscal_weekdays()
weekends = fy.fiscal_weekends()
workdays = fy.fiscal_workdays()
```

Use actual holidays when constructing workdays:

```python
workdays = fy.fiscal_workdays(
    use_observed=False,
)
```

### Monthly Aggregations

```python
calendar_by_month = fy.fiscal_calendar()

weekdays_by_month = fy.weekdays_by_month()
weekends_by_month = fy.weekends_by_month()
workdays_by_month = fy.workdays_by_month()
holidays_by_month = fy.holidays_by_month()
```

Actual-holiday mode:

```python
workdays_by_month = fy.workdays_by_month(
    use_observed=False,
)

holidays_by_month = fy.holidays_by_month(
    use_observed=False,
)
```

### Remaining Fiscal-Year Counts

```python
remaining_holidays = fy.holidays_remaining()
remaining_workdays = fy.workdays_remaining()
remaining_weekends = fy.weekends_remaining()
```

Actual-holiday mode:

```python
remaining_holidays = fy.holidays_remaining(
    use_observed=False,
)

remaining_workdays = fy.workdays_remaining(
    use_observed=False,
)
```

### Leap-Day Utilities

```python
contains_leap_day = fy.contains_leap_day()
availability_leap_days = fy.leap_days_in_availability()
```

### Fiscal-Year Holiday Values

```python
holiday_values = fy.holidays
```

```python
[
    {"ColumbusDay": "10/13/2025"},
    {"VeteransDay": "11/11/2025"},
    {"ThanksgivingDay": "11/27/2025"},
]
```

`ID` and `FiscalYear` are excluded. Null values are returned as empty strings.

### Federal Holiday Usage

```python
holidays = FederalHoliday("2026")

holidays.fiscal_year
holidays.columbus_day
holidays.veterans_day
holidays.thanksgiving_day
holidays.christmas_day
holidays.new_years_day
holidays.martin_luther_king_day
holidays.presidents_day
holidays.memorial_day
holidays.juneteenth_day
holidays.independence_day
holidays.labor_day
```

```python
holiday_map = holidays.holidays()

independence_day = holiday_map["Independence Day"]

independence_day["actual"]
independence_day["observed"]
```

```python
holidays.is_holiday(date(2026, 7, 4))
holidays.is_holiday(date(2026, 7, 3), observed=True)
holidays.is_holiday(date(2026, 7, 4), observed=False)
holidays.is_weekend(date(2026, 7, 4))
holidays.observed_date(date(2026, 7, 4))
```

- Saturday holiday: preceding Friday
- Sunday holiday: following Monday
- Weekday holiday: unchanged

### Dictionary Exports

```python
fiscal_record = fy.to_dict()
holiday_record = holidays.to_dict()
```

<a id="api-overview"></a>

## 🧠 API Overview

- [Key Definitions](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/Definitions.md#%EF%B8%8F-defninitions)

```python
from fiscal import DB, FederalHoliday, FiscalYear, throw_if, to_date
```

### `FiscalYear`

#### Fiscal and Calendar Progress

| Member | Signature |
|---|---|
| `holidays` | `holidays -> list[dict[str, str]]` |
| `calendar_day_of_year` | `calendar_day_of_year() -> int` |
| `calendar_days_in_year` | `calendar_days_in_year() -> int` |
| `calendar_days_elapsed` | `calendar_days_elapsed() -> int` |
| `calendar_days_remaining` | `calendar_days_remaining() -> int` |
| `calendar_months_elapsed` | `calendar_months_elapsed() -> int` |
| `calendar_months_remaining` | `calendar_months_remaining() -> int` |
| `calendar_percent_elapsed` | `calendar_percent_elapsed() -> float` |
| `calendar_bounds` | `calendar_bounds() -> tuple[date, date]` |
| `calendar_week_number` | `calendar_week_number() -> int` |
| `calendar_month_name` | `calendar_month_name() -> str` |
| `current_weekday_name` | `current_weekday_name() -> str` |
| `fiscal_day_of_year` | `fiscal_day_of_year() -> int` |
| `fiscal_days_in_year` | `fiscal_days_in_year() -> int` |
| `fiscal_month_number` | `fiscal_month_number() -> int` |
| `fiscal_days_elapsed` | `fiscal_days_elapsed() -> int` |
| `fiscal_days_remaining` | `fiscal_days_remaining() -> int` |
| `fiscal_months_elapsed` | `fiscal_months_elapsed() -> int` |
| `fiscal_months_remaining` | `fiscal_months_remaining() -> int` |
| `fiscal_percent_elapsed` | `fiscal_percent_elapsed() -> float` |
| `fiscal_bounds` | `fiscal_bounds() -> tuple[date, date]` |
| `is_fiscal_start_year` | `is_fiscal_start_year() -> bool` |
| `is_fiscal_end_year` | `is_fiscal_end_year() -> bool` |
| `is_calendar_start_year` | `is_calendar_start_year() -> bool` |
| `is_calendar_end_date` | `is_calendar_end_date() -> bool` |

#### Months, Quarters, and Weeks

| Member | Signature |
|---|---|
| `fiscal_month_bounds` | `fiscal_month_bounds(fiscal_month) -> tuple[date, date]` |
| `fiscal_days_in_month` | `fiscal_days_in_month(fiscal_month) -> int` |
| `fiscal_month_calendar` | `fiscal_month_calendar(fiscal_month) -> list[list[date]]` |
| `fiscal_month_weeks` | `fiscal_month_weeks(fiscal_month) -> list[list[int]]` |
| `fiscal_month_name` | `fiscal_month_name(fiscal_month) -> str` |
| `fiscal_quarter_number` | `fiscal_quarter_number() -> int` |
| `fiscal_quarter_bounds` | `fiscal_quarter_bounds(quarter) -> tuple[date, date]` |
| `fiscal_days_in_quarter` | `fiscal_days_in_quarter(quarter) -> int` |
| `fiscal_week_number` | `fiscal_week_number() -> int` |
| `fiscal_week_bounds` | `fiscal_week_bounds(fiscal_week) -> tuple[date, date]` |
| `weekdays_in_month` | `weekdays_in_month(fiscal_month) -> int` |
| `weekends_in_month` | `weekends_in_month(fiscal_month) -> int` |
| `weekday_occurrences` | `weekday_occurrences(fiscal_month, weekday) -> int` |

#### Date Collections and Monthly Aggregations

| Member | Signature |
|---|---|
| `fiscal_dates` | `fiscal_dates() -> list[date]` |
| `fiscal_weekdays` | `fiscal_weekdays() -> list[date]` |
| `fiscal_weekends` | `fiscal_weekends() -> list[date]` |
| `fiscal_workdays` | `fiscal_workdays(use_observed=True) -> list[date]` |
| `fiscal_calendar` | `fiscal_calendar() -> dict[str, list[date]]` |
| `weekdays_by_month` | `weekdays_by_month() -> dict[str, int]` |
| `weekends_by_month` | `weekends_by_month() -> dict[str, int]` |
| `workdays_by_month` | `workdays_by_month(use_observed=True) -> dict[str, int]` |
| `holidays_by_month` | `holidays_by_month(use_observed=True) -> dict[str, list[date]]` |

#### Range, Remaining-Time, and Leap-Day Utilities

| Member | Signature |
|---|---|
| `count_weekends` | `count_weekends(start, end) -> int` |
| `count_holidays` | `count_holidays(start, end, use_observed=True) -> int` |
| `count_workdays` | `count_workdays(start, end, use_observed=True) -> int` |
| `holidays_between` | `holidays_between(start, end, use_observed=True) -> dict[str, str]` |
| `holidays_remaining` | `holidays_remaining(use_observed=True) -> int` |
| `workdays_remaining` | `workdays_remaining(use_observed=True) -> int` |
| `weekends_remaining` | `weekends_remaining() -> int` |
| `contains_leap_day` | `contains_leap_day() -> bool` |
| `leap_days_in_availability` | `leap_days_in_availability() -> int` |
| `to_dict` | `to_dict() -> dict[str, object]` |

### `FederalHoliday`

| Member | Signature |
|---|---|
| `observed_date` | `observed_date(value) -> date` |
| `holidays` | `holidays() -> dict[str, dict[str, date]]` |
| `is_holiday` | `is_holiday(when, observed=True) -> bool` |
| `is_weekend` | `is_weekend(when) -> bool` |
| `to_dict` | `to_dict() -> dict[str, object]` |

### Utilities

- `throw_if(name, value) -> None`
- `to_date(value) -> date | None`

`to_date()` accepts:

- `date`
- `datetime`
- `YYYY-MM-DD`
- `MM/DD/YYYY`
- `MM/DD/YY`
- `NS`
- `N/A`
- `NA`
- `NONE`
- `NULL`

## 📚 References

- [Fiscal Year](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/Definitions.md#fiscal-year)
- [Federal Holiday](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/)

<a id="license"></a>

## 📜 [License](https://github.com/is-leeroy-jenkins/fiscal/blob/master/LICENSE.txt)

MIT © 2022 Terry D. Eppler
