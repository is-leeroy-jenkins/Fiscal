###### fiscal

![](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/images/github/project_fiscal.png)

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
  <a href="#license">License</a>
</p>

___

<a id="features"></a>

## 📝 Features

- SQLite-backed fiscal-year and federal-holiday records
- Fiscal-year queries by `FiscalYear`, `BPOA`, and `EPOA`
- Calendar-year and fiscal-year progress calculations
- Actual and observed federal-holiday dates
- Inclusive weekend, holiday, and workday counts
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

### Fiscal Year Usage

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

```python
fy = FiscalYear(
    fy="2026",
    bpoa="2024",
    epoa="2026",
)
```

### Calendar Year Calculations

```python
fy.calendar_day_of_year()
fy.calendar_days_in_year()
fy.calendar_days_elapsed()
fy.calendar_days_remaining()
fy.calendar_months_elapsed()
fy.calendar_months_remaining()
fy.calendar_percent_elapsed()
fy.calendar_bounds()
fy.is_calendar_start_year()
fy.is_calendar_end_date()
```

### Fiscal Year Calculations

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
fy.is_fiscal_start_year()
fy.is_fiscal_end_year()
```

### Range Utilities

```python

start = date(2026, 7, 1)
end = date(2026, 7, 31)

weekend_count = fy.count_weekends(start, end)
holiday_count = fy.count_holidays(start, end)
workday_count = fy.count_workdays(start, end)
```

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

| Member                                                                                                                                  | Signature                                              |
|-----------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| [holidays](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L401)                  | `holidays -> list[dict[str, str]]`                     |
| [calendar_day_of_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L434)      | `calendar_day_of_year() -> int`                        |
| [calendar_days_in_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L732)     | `calendar_days_in_year() -> int`                       |
| [calendar_days_elapsed](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L454)     | `calendar_days_elapsed() -> int`                       |
| [calendar_days_remaining](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L474)   | `calendar_days_remaining() -> int`                     |
| [calendar_months_elapsed](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L494)   | `calendar_months_elapsed() -> int`                     |
| [calendar_months_remaining](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L514) | `calendar_months_remaining() -> int`                   |
| [calendar_percent_elapsed](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L534)  | `calendar_percent_elapsed() -> float`                  |
| [fiscal_day_of_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L554)        | `fiscal_day_of_year() -> int`                          |
| [fiscal_days_in_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L742)       | `fiscal_days_in_year() -> int`                         |
| [fiscal_month_number](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L574)       | `fiscal_month_number() -> int`                         |
| [fiscal_days_elapsed](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L594)       | `fiscal_days_elapsed() -> int`                         |
| [fiscal_days_remaining](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L614)     | `fiscal_days_remaining() -> int`                       |
| [fiscal_months_elapsed](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L635)     | `fiscal_months_elapsed() -> int`                       |
| [fiscal_months_remaining](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L655)   | `fiscal_months_remaining() -> int`                     |
| [fiscal_percent_elapsed](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L675)    | `fiscal_percent_elapsed() -> float`                    |
| [count_weekends](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L695)            | `count_weekends(start, end) -> int`                    |
| [count_holidays](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L752)            | `count_holidays(start, end, use_observed=True) -> int` |
| [count_workdays](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L788)            | `count_workdays(start, end, use_observed=True) -> int` |
| [calendar_bounds](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L830)           | `calendar_bounds() -> tuple[date, date]`               |
| [fiscal_bounds](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L850)             | `fiscal_bounds() -> tuple[date, date]`                 |
| [is_fiscal_start_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L871)      | `is_fiscal_start_year() -> bool`                       |
| [is_fiscal_end_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L891)        | `is_fiscal_end_year() -> bool`                         |
| [is_calendar_start_year](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L911)    | `is_calendar_start_year() -> bool`                     |
| [is_calendar_end_date](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L931)      | `is_calendar_end_date() -> bool`                       |
| [to_dict](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L951)                   | `to_dict() -> dict[str, object]`                       |

### `FederalHoliday`

| Member                                                                                                                       | Signature                                  |
|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| [observed_date](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L1087) | `observed_date(value) -> date`             |
| [holidays](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L1116)      | `holidays() -> dict[str, dict[str, date]]` |
| [is_holiday](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L1144)    | `is_holiday(when, observed=True) -> bool`  |
| [is_weekend](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L1172)    | `is_weekend(when) -> bool`                 |
| [to_dict](https://github.com/is-leeroy-jenkins/Fiscal/blob/26dc5083256db526c41d50954b09660df776ad14/__init__.py#L1197)       | `to_dict() -> dict[str, object]`           |

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
