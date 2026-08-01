# tempus User Guide

`tempus` provides database-backed U.S. federal fiscal-year, calendar-year, federal-holiday, workday, and weekend calculations for Python applications and ad-hoc analysis.

The examples assume the library and its packaged fiscal data are already installed and available.

## Installation

```bash
pip install tempus
```

## Imports

```python
from datetime import date, datetime

from tempus import FederalHoliday, FiscalYear
```

For pandas analysis:

```python
import pandas as pd
```

## Quick Start

Create a fiscal-year object:

```python
from tempus import FiscalYear

fy = FiscalYear("2026")
```

Read the fiscal-year boundaries:

```python
print(fy.start_date)
print(fy.end_date)
```

```text
2025-10-01
2026-09-30
```

Inspect the current fiscal position:

```python
print(fy.fiscal_year)
print(fy.fiscal_day_of_year())
print(fy.fiscal_month_number())
print(fy.fiscal_quarter_number())
print(fy.fiscal_days_remaining())
print(fy.fiscal_percent_elapsed())
```

Count workdays in a range:

```python
workdays = fy.count_workdays(
    start=date(2026, 7, 1),
    end=date(2026, 7, 31),
)

print(workdays)
```

Return holiday names and dates:

```python
holidays = fy.holidays_between(
    start=date(2026, 1, 1),
    end=date(2026, 9, 30),
)

for name, holiday_date in holidays.items():
    print(f"{holiday_date}: {name}")
```

## Creating Fiscal-Year Objects

### Single-year availability

```python
fy = FiscalYear("2026")
```

When `bpoa` and `epoa` are omitted, each defaults to the supplied fiscal year.

```python
assert fy.bpoa == "2026"
assert fy.epoa == "2026"
```

### Multi-year availability

```python
fy = FiscalYear(
    fy="2026",
    bpoa="2024",
    epoa="2026",
)
```

### Display representation

```python
print(fy)
```

```text
2026
```

## Fiscal-Year Properties

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

Export the stored fiscal-year record:

```python
record = fy.to_dict()

for name, value in record.items():
    print(f"{name}: {value}")
```

Create a one-row DataFrame:

```python
df_fiscal_year = pd.DataFrame(
    [fy.to_dict()]
)

print(df_fiscal_year)
```

## Calendar-Year Calculations

### Calendar day and year length

```python
print(fy.calendar_day_of_year())
print(fy.calendar_days_in_year())
```

### Elapsed and remaining calendar days

```python
print(fy.calendar_days_elapsed())
print(fy.calendar_days_remaining())
```

### Elapsed and remaining calendar months

```python
print(fy.calendar_months_elapsed())
print(fy.calendar_months_remaining())
```

### Calendar-year percentage

```python
percent = fy.calendar_percent_elapsed()

print(f"{percent:.2f}%")
```

### Calendar boundaries

```python
start_date, end_date = fy.calendar_bounds()

print(start_date)
print(end_date)
```

### Current calendar labels

```python
print(fy.calendar_year)
print(fy.calendar_month_name())
print(fy.current_weekday_name())
print(fy.calendar_week_number())
```

### Calendar boundary checks

```python
print(fy.is_calendar_start_year())
print(fy.is_calendar_end_date())
```

## Fiscal-Year Calculations

### Fiscal day, month, quarter, and week

```python
print(fy.fiscal_day_of_year())
print(fy.fiscal_month_number())
print(fy.fiscal_quarter_number())
print(fy.fiscal_week_number())
```

### Fiscal-year length

```python
print(fy.fiscal_days_in_year())
```

### Elapsed and remaining fiscal days

```python
print(fy.fiscal_days_elapsed())
print(fy.fiscal_days_remaining())
```

### Elapsed and remaining fiscal months

```python
print(fy.fiscal_months_elapsed())
print(fy.fiscal_months_remaining())
```

### Fiscal-year percentage

```python
percent = fy.fiscal_percent_elapsed()

print(f"{percent:.2f}%")
```

### Fiscal boundaries

```python
start_date, end_date = fy.fiscal_bounds()

print(start_date)
print(end_date)
```

### Fiscal-year boundary checks

```python
print(fy.is_fiscal_start_year())
print(fy.is_fiscal_end_year())
```

## Fiscal Months

Federal fiscal months are numbered from October through September.

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

### Month name

```python
print(fy.fiscal_month_name(1))
print(fy.fiscal_month_name(10))
```

```text
October
July
```

### Month boundaries

```python
start_date, end_date = fy.fiscal_month_bounds(10)

print(start_date)
print(end_date)
```

```text
2026-07-01
2026-07-31
```

### Days in a fiscal month

```python
print(fy.fiscal_days_in_month(5))
```

### Iterate through all fiscal months

```python
for fiscal_month in range(1, 13):
    start_date, end_date = fy.fiscal_month_bounds(
        fiscal_month,
    )

    print(
        fiscal_month,
        fy.fiscal_month_name(fiscal_month),
        start_date,
        end_date,
        fy.fiscal_days_in_month(fiscal_month),
    )
```

### Week-oriented date matrix

```python
weeks = fy.fiscal_month_calendar(1)

for week in weeks:
    print(week)
```

Each row contains seven `date` values.

### Week-oriented integer matrix

```python
weeks = fy.fiscal_month_weeks(1)

for week in weeks:
    print(week)
```

Days outside the selected month are represented by `0`.

### Weekdays and weekends in a month

```python
print(fy.weekdays_in_month(1))
print(fy.weekends_in_month(1))
```

### Count a weekday in a month

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

print(mondays)
print(fridays)
```

## Fiscal Quarters

| Quarter | Fiscal Months | Calendar Months |
|---:|---|---|
| `1` | `1`–`3` | October–December |
| `2` | `4`–`6` | January–March |
| `3` | `7`–`9` | April–June |
| `4` | `10`–`12` | July–September |

### Current fiscal quarter

```python
print(fy.fiscal_quarter_number())
```

### Quarter boundaries

```python
start_date, end_date = fy.fiscal_quarter_bounds(4)

print(start_date)
print(end_date)
```

```text
2026-07-01
2026-09-30
```

### Days in a quarter

```python
print(fy.fiscal_days_in_quarter(4))
```

### Quarter summary

```python
quarter = 4
start_date, end_date = fy.fiscal_quarter_bounds(
    quarter,
)

summary = {
    "Quarter": f"Q{quarter}",
    "StartDate": start_date,
    "EndDate": end_date,
    "CalendarDays": fy.fiscal_days_in_quarter(
        quarter,
    ),
    "Weekends": fy.count_weekends(
        start_date,
        end_date,
    ),
    "Holidays": fy.count_holidays(
        start_date,
        end_date,
    ),
    "Workdays": fy.count_workdays(
        start_date,
        end_date,
    ),
}

print(summary)
```

## Fiscal Weeks

### Current fiscal week

```python
print(fy.fiscal_week_number())
```

### Fiscal-week boundaries

```python
start_date, end_date = fy.fiscal_week_bounds(1)

print(start_date)
print(end_date)
```

### Generate a fiscal-week table

```python
rows = []

for fiscal_week in range(
    1,
    fy.fiscal_week_number() + 1,
):
    start_date, end_date = fy.fiscal_week_bounds(
        fiscal_week,
    )

    rows.append(
        {
            "FiscalWeek": fiscal_week,
            "StartDate": start_date,
            "EndDate": end_date,
        }
    )

df_weeks = pd.DataFrame(rows)

print(df_weeks)
```

## Federal Holidays

### Create a holiday object

```python
holiday = FederalHoliday("2026")
```

### Read stored holiday dates

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

### Actual and observed holiday dates

```python
holidays = holiday.holidays()

for name, values in holidays.items():
    print(
        name,
        values["actual"],
        values["observed"],
    )
```

Example payload:

```python
{
    "Independence Day": {
        "actual": date(2026, 7, 4),
        "observed": date(2026, 7, 3),
    },
}
```

### Calculate an observed date

Saturday holiday:

```python
observed_date = holiday.observed_date(
    date(2026, 7, 4),
)

print(observed_date)
```

```text
2026-07-03
```

Sunday holiday:

```python
observed_date = holiday.observed_date(
    date(2027, 7, 4),
)

print(observed_date)
```

```text
2027-07-05
```

### Determine whether a date is a holiday

Observed date:

```python
result = holiday.is_holiday(
    when=date(2026, 7, 3),
    observed=True,
)

print(result)
```

Actual date:

```python
result = holiday.is_holiday(
    when=date(2026, 7, 4),
    observed=False,
)

print(result)
```

Datetime values are accepted:

```python
result = holiday.is_holiday(
    when=datetime(2026, 7, 4, 12, 0),
    observed=False,
)
```

### Determine whether a date is a weekend

```python
print(
    holiday.is_weekend(
        date(2026, 7, 4),
    )
)

print(
    holiday.is_weekend(
        date(2026, 7, 6),
    )
)
```

### Export holiday data

```python
record = holiday.to_dict()

print(record)
```

## Holiday Analysis by Date Range

### Return holiday names and observed dates

```python
holidays = fy.holidays_between(
    start=date(2026, 1, 1),
    end=date(2026, 9, 30),
    use_observed=True,
)

for name, holiday_date in holidays.items():
    print(f"{holiday_date}: {name}")
```

### Return actual holiday dates

```python
holidays = fy.holidays_between(
    start=date(2026, 1, 1),
    end=date(2026, 9, 30),
    use_observed=False,
)
```

### Count holidays in a range

```python
count = fy.count_holidays(
    start=date(2026, 7, 1),
    end=date(2026, 9, 30),
)

print(count)
```

### Count remaining holidays

```python
print(fy.holidays_remaining())
```

Use actual dates instead of observed dates:

```python
print(
    fy.holidays_remaining(
        use_observed=False,
    )
)
```

### Group holidays by month

```python
holidays_by_month = fy.holidays_by_month()

for month_name, dates in holidays_by_month.items():
    print(month_name, dates)
```

## Workday and Weekend Analysis

### Count weekends in a range

```python
count = fy.count_weekends(
    start=date(2026, 7, 1),
    end=date(2026, 7, 31),
)

print(count)
```

### Count workdays in a range

Observed-holiday mode:

```python
count = fy.count_workdays(
    start=date(2026, 7, 1),
    end=date(2026, 7, 31),
    use_observed=True,
)

print(count)
```

Actual-holiday mode:

```python
count = fy.count_workdays(
    start=date(2026, 7, 1),
    end=date(2026, 7, 31),
    use_observed=False,
)
```

### Remaining workdays and weekend days

```python
print(fy.workdays_remaining())
print(fy.weekends_remaining())
```

### Complete fiscal-year date lists

All dates:

```python
dates = fy.fiscal_dates()

print(dates[0])
print(dates[-1])
print(len(dates))
```

Weekdays:

```python
weekdays = fy.fiscal_weekdays()

print(len(weekdays))
```

Weekend dates:

```python
weekends = fy.fiscal_weekends()

print(len(weekends))
```

Workdays:

```python
workdays = fy.fiscal_workdays()

print(len(workdays))
```

### Check whether a date is a fiscal-year workday

```python
target_date = date(2026, 7, 3)

is_workday = target_date in fy.fiscal_workdays()

print(is_workday)
```

### Filter a workday range

```python
start_date = date(2026, 7, 1)
end_date = date(2026, 7, 31)

workdays = [
    current_date
    for current_date in fy.fiscal_workdays()
    if start_date <= current_date <= end_date
]

print(workdays)
```

## Monthly Fiscal Analysis

### Dates grouped by month

```python
calendar_by_month = fy.fiscal_calendar()

for month_name, dates in calendar_by_month.items():
    print(month_name, len(dates))
```

### Counts grouped by month

```python
weekdays = fy.weekdays_by_month()
weekends = fy.weekends_by_month()
workdays = fy.workdays_by_month()
holidays = fy.holidays_by_month()
```

Create a combined dictionary:

```python
monthly_summary = {
    month_name: {
        "Weekdays": weekdays[month_name],
        "Weekends": weekends[month_name],
        "Workdays": workdays[month_name],
        "Holidays": len(holidays[month_name]),
    }
    for month_name in weekdays
}

print(monthly_summary)
```

Create a DataFrame:

```python
df_monthly = pd.DataFrame(
    [
        {
            "Month": month_name,
            "Weekdays": weekdays[month_name],
            "Weekends": weekends[month_name],
            "Workdays": workdays[month_name],
            "Holidays": len(holidays[month_name]),
        }
        for month_name in weekdays
    ]
)

print(df_monthly)
```

Export the monthly summary:

```python
df_monthly.to_csv(
    "fiscal-month-summary.csv",
    index=False,
)
```

## Ad-Hoc pandas Analysis

### Fiscal-year record

```python
df_fiscal_year = pd.DataFrame(
    [fy.to_dict()]
)
```

### Holiday table

```python
holidays = fy.holidays_between(
    start=fy.start_date,
    end=fy.end_date,
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

### Actual-versus-observed comparison

```python
holiday = FederalHoliday(
    fy.fiscal_year,
)

df_holiday_comparison = pd.DataFrame(
    [
        {
            "Holiday": name,
            "ActualDate": values["actual"],
            "ObservedDate": values["observed"],
            "Adjusted": (
                values["actual"]
                != values["observed"]
            ),
        }
        for name, values in holiday.holidays().items()
    ]
)

print(df_holiday_comparison)
```

### Complete fiscal-year date table

```python
holiday_dates = holiday.holidays()

observed_lookup = {
    values["observed"]: name
    for name, values in holiday_dates.items()
}

rows = []

for current_date in fy.fiscal_dates():
    holiday_name = observed_lookup.get(
        current_date,
        "",
    )

    rows.append(
        {
            "Date": current_date,
            "FiscalYear": fy.fiscal_year,
            "FiscalMonth": (
                ((current_date.month - 10) % 12)
                + 1
            ),
            "Weekday": current_date.strftime("%A"),
            "IsWeekend": (
                current_date.weekday() >= 5
            ),
            "IsHoliday": bool(holiday_name),
            "HolidayName": holiday_name,
            "IsWorkday": (
                current_date.weekday() < 5
                and not holiday_name
            ),
        }
    )

df_calendar = pd.DataFrame(rows)

print(df_calendar.head())
```

Filter workdays:

```python
df_workdays = df_calendar.loc[
    df_calendar["IsWorkday"]
]
```

Filter holidays:

```python
df_holidays = df_calendar.loc[
    df_calendar["IsHoliday"]
]
```

Filter one fiscal month:

```python
df_july = df_calendar.loc[
    df_calendar["FiscalMonth"] == 10
]
```

Export:

```python
df_calendar.to_csv(
    "fiscal-year-2026.csv",
    index=False,
)

df_calendar.to_json(
    "fiscal-year-2026.json",
    orient="records",
    date_format="iso",
    indent=2,
)
```

## Common Recipes

### Fiscal-year dashboard values

```python
dashboard = {
    "FiscalYear": fy.fiscal_year,
    "StartDate": fy.start_date,
    "EndDate": fy.end_date,
    "FiscalDay": fy.fiscal_day_of_year(),
    "FiscalMonth": fy.fiscal_month_number(),
    "FiscalQuarter": fy.fiscal_quarter_number(),
    "PercentElapsed": round(
        fy.fiscal_percent_elapsed(),
        2,
    ),
    "CalendarDaysRemaining": (
        fy.fiscal_days_remaining()
    ),
    "WorkdaysRemaining": (
        fy.workdays_remaining()
    ),
    "WeekendDaysRemaining": (
        fy.weekends_remaining()
    ),
    "HolidaysRemaining": (
        fy.holidays_remaining()
    ),
}

print(dashboard)
```

### Fiscal-year progress statement

```python
message = (
    f"FY {fy.fiscal_year} is "
    f"{fy.fiscal_percent_elapsed():.2f}% complete. "
    f"{fy.fiscal_days_remaining():,} calendar days, "
    f"{fy.workdays_remaining():,} workdays, "
    f"{fy.weekends_remaining():,} weekend days, and "
    f"{fy.holidays_remaining():,} federal holidays remain."
)

print(message)
```

### Find the next observed holiday

```python
today = fy.current_date

future_holidays = [
    (name, values["observed"])
    for name, values in FederalHoliday(
        fy.fiscal_year,
    ).holidays().items()
    if values["observed"] >= today
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

### Find adjusted holidays

```python
adjusted_holidays = {
    name: values
    for name, values in FederalHoliday(
        fy.fiscal_year,
    ).holidays().items()
    if values["actual"] != values["observed"]
}

print(adjusted_holidays)
```

### Determine whether today is a workday

```python
today = fy.current_date

is_workday = today in fy.fiscal_workdays()

print(is_workday)
```

### Compare multiple fiscal years

```python
fiscal_years = [
    FiscalYear("2024"),
    FiscalYear("2025"),
    FiscalYear("2026"),
]

df_comparison = pd.DataFrame(
    [
        {
            "FiscalYear": item.fiscal_year,
            "StartDate": item.start_date,
            "EndDate": item.end_date,
            "Weekdays": item.weekdays,
            "Weekends": item.weekends,
            "Workdays": item.workdays,
            "CompensableDays": (
                item.compensable_days
            ),
            "CompensableHours": (
                item.compensable_hours
            ),
        }
        for item in fiscal_years
    ]
)

print(df_comparison)
```

### Validate fiscal-year totals

```python
calculated_days = fy.fiscal_days_in_year()
calculated_weekdays = len(
    fy.fiscal_weekdays()
)
calculated_weekends = len(
    fy.fiscal_weekends()
)
calculated_workdays = len(
    fy.fiscal_workdays()
)

validation = {
    "CalendarDaysBalance": (
        calculated_weekdays
        + calculated_weekends
        == calculated_days
    ),
    "WeekdaysMatch": (
        calculated_weekdays
        == fy.weekdays
    ),
    "WeekendsMatch": (
        calculated_weekends
        == fy.weekends
    ),
    "WorkdaysMatch": (
        calculated_workdays
        == int(fy.workdays)
    ),
}

print(validation)
```

## Error Handling

Invalid fiscal-year records, unsupported table values, invalid month or quarter numbers, and malformed date values are surfaced through the library's `Error` wrapper.

```python
from boogr import Error

try:
    fy = FiscalYear("2099")
except Error as ex:
    print(ex.module)
    print(ex.cause)
    print(ex.method)
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

## API Summary

### `FiscalYear`

| Member | Signature |
|---|---|
| Constructor | `FiscalYear(fy, bpoa='', epoa='')` |
| Fiscal record | `to_dict() -> Dict[str, object]` |
| Holiday columns | `holidays -> List[Dict[str, str]]` |
| Calendar day | `calendar_day_of_year() -> int` |
| Calendar days | `calendar_days_in_year() -> int` |
| Calendar elapsed | `calendar_days_elapsed() -> int` |
| Calendar remaining | `calendar_days_remaining() -> int` |
| Calendar months elapsed | `calendar_months_elapsed() -> int` |
| Calendar months remaining | `calendar_months_remaining() -> int` |
| Calendar percentage | `calendar_percent_elapsed() -> float` |
| Calendar bounds | `calendar_bounds() -> Tuple[date, date]` |
| Calendar week | `calendar_week_number() -> int` |
| Fiscal day | `fiscal_day_of_year() -> int` |
| Fiscal month | `fiscal_month_number() -> int` |
| Fiscal quarter | `fiscal_quarter_number() -> int` |
| Fiscal week | `fiscal_week_number() -> int` |
| Fiscal elapsed | `fiscal_days_elapsed() -> int` |
| Fiscal remaining | `fiscal_days_remaining() -> int` |
| Fiscal percentage | `fiscal_percent_elapsed() -> float` |
| Fiscal bounds | `fiscal_bounds() -> Tuple[date, date]` |
| Month bounds | `fiscal_month_bounds(fiscal_month) -> Tuple[date, date]` |
| Quarter bounds | `fiscal_quarter_bounds(quarter) -> Tuple[date, date]` |
| Week bounds | `fiscal_week_bounds(fiscal_week) -> Tuple[date, date]` |
| Range weekends | `count_weekends(start, end) -> int` |
| Range holidays | `count_holidays(start, end, use_observed=True) -> int` |
| Range workdays | `count_workdays(start, end, use_observed=True) -> int` |
| Holiday mapping | `holidays_between(start, end, use_observed=True) -> Dict[str, str]` |
| Remaining holidays | `holidays_remaining(use_observed=True) -> int` |
| Remaining workdays | `workdays_remaining(use_observed=True) -> int` |
| Remaining weekends | `weekends_remaining() -> int` |
| Fiscal dates | `fiscal_dates() -> List[date]` |
| Fiscal weekdays | `fiscal_weekdays() -> List[date]` |
| Fiscal weekends | `fiscal_weekends() -> List[date]` |
| Fiscal workdays | `fiscal_workdays(use_observed=True) -> List[date]` |
| Monthly weekdays | `weekdays_by_month() -> Dict[str, int]` |
| Monthly weekends | `weekends_by_month() -> Dict[str, int]` |
| Monthly workdays | `workdays_by_month(use_observed=True) -> Dict[str, int]` |
| Monthly holidays | `holidays_by_month(use_observed=True) -> Dict[str, List[date]]` |

### `FederalHoliday`

| Member | Signature |
|---|---|
| Constructor | `FederalHoliday(fiscal_year)` |
| Observed date | `observed_date(value) -> date` |
| Holiday mapping | `holidays() -> Dict[str, Dict[str, date]]` |
| Holiday test | `is_holiday(when, observed=True) -> bool` |
| Weekend test | `is_weekend(when) -> bool` |
| Record export | `to_dict() -> Dict[str, object]` |
