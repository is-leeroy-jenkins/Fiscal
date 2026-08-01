# Fiscal User Guide

Fiscal provides U.S. federal fiscal-year, calendar-year, federal-holiday, workday, and weekend calculations for Python applications and ad-hoc analysis.

## Installation

```bash
pip install fiscal
```

## Import the Library

```python
from datetime import date

from fiscal import FederalHoliday, FiscalYear
```

## Determine the Status of a Fiscal Year

```python
fy = FiscalYear( '2026' )

status = \
{
    'FiscalYear': fy.fiscal_year,
    'StartDate': fy.start_date,
    'EndDate': fy.end_date,
    'FiscalDay': fy.fiscal_day_of_year( ),
    'FiscalWeek': fy.fiscal_week_number( ),
    'FiscalMonth': fy.fiscal_month_number( ),
    'FiscalQuarter': fy.fiscal_quarter_number( ),
    'DaysElapsed': fy.fiscal_days_elapsed( ),
    'DaysRemaining': fy.fiscal_days_remaining( ),
    'PercentElapsed': round( fy.fiscal_percent_elapsed( ), 2 ),
}

for name, value in status.items( ):
    print( f'{name}: {value}' )
```

Use `to_dict( )` when the stored fiscal-year record is needed by another application:

```python
record = fy.to_dict( )

print( record[ 'FiscalYear' ] )
print( record[ 'Availability' ] )
print( record[ 'Type' ] )
```

## Analyze a Date Range

```python
start_date = date( 2026, 7, 1 )
end_date = date( 2026, 7, 31 )

summary = \
{
    'StartDate': start_date,
    'EndDate': end_date,
    'WeekendDays': fy.count_weekends( start_date, end_date ),
    'FederalHolidays': fy.count_holidays( start_date, end_date ),
    'Workdays': fy.count_workdays( start_date, end_date ),
}

print( summary )
```

Observed federal holidays are used by default. Use actual holiday dates when required:

```python
actual_holidays = fy.count_holidays(
    start=start_date,
    end=end_date,
    use_observed=False,
)

actual_workdays = fy.count_workdays(
    start=start_date,
    end=end_date,
    use_observed=False,
)
```

Return holiday names and dates for the range:

```python
holidays = fy.holidays_between(
    start=start_date,
    end=end_date,
    use_observed=True,
)

for name, holiday_date in holidays.items( ):
    print( f'{holiday_date}: {name}' )
```

## Determine Remaining Fiscal-Year Time

```python
remaining = \
{
    'CalendarDays': fy.fiscal_days_remaining( ),
    'Workdays': fy.workdays_remaining( ),
    'WeekendDays': fy.weekends_remaining( ),
    'FederalHolidays': fy.holidays_remaining( ),
}

print( remaining )
```

## Build a Monthly Fiscal Summary

Federal fiscal months are numbered from October through September.

| Fiscal Month | Calendar Month |
|---:|---|
| 1 | October |
| 2 | November |
| 3 | December |
| 4 | January |
| 5 | February |
| 6 | March |
| 7 | April |
| 8 | May |
| 9 | June |
| 10 | July |
| 11 | August |
| 12 | September |

```python
rows = [ ]

for fiscal_month in range( 1, 13 ):
    month_start, month_end = fy.fiscal_month_bounds( fiscal_month )

    rows.append(
        {
            'FiscalMonth': fiscal_month,
            'Month': fy.fiscal_month_name( fiscal_month ),
            'StartDate': month_start,
            'EndDate': month_end,
            'CalendarDays': fy.fiscal_days_in_month( fiscal_month ),
            'Weekdays': fy.weekdays_in_month( fiscal_month ),
            'WeekendDays': fy.weekends_in_month( fiscal_month ),
        }
    )

for row in rows:
    print( row )
```

Monthly workday and holiday summaries are available directly:

```python
workdays = fy.workdays_by_month( )
holidays = fy.holidays_by_month( )

for month_name in workdays:
    print(
        month_name,
        workdays[ month_name ],
        holidays[ month_name ],
    )
```

## Build a Quarterly Fiscal Summary

```python
quarters = [ ]

for quarter in range( 1, 5 ):
    quarter_start, quarter_end = fy.fiscal_quarter_bounds( quarter )

    quarters.append(
        {
            'Quarter': f'Q{quarter}',
            'StartDate': quarter_start,
            'EndDate': quarter_end,
            'CalendarDays': fy.fiscal_days_in_quarter( quarter ),
            'WeekendDays': fy.count_weekends( quarter_start, quarter_end ),
            'FederalHolidays': fy.count_holidays( quarter_start, quarter_end ),
            'Workdays': fy.count_workdays( quarter_start, quarter_end ),
        }
    )

for quarter in quarters:
    print( quarter )
```

## Check Federal Holidays

```python
holiday = FederalHoliday( '2026' )
```

Return actual and observed dates:

```python
for name, values in holiday.holidays( ).items( ):
    print(
        name,
        values[ 'actual' ],
        values[ 'observed' ],
    )
```

Check a specific date:

```python
observed = holiday.is_holiday(
    when=date( 2026, 7, 3 ),
    observed=True,
)

actual = holiday.is_holiday(
    when=date( 2026, 7, 4 ),
    observed=False,
)

weekend = holiday.is_weekend(
    date( 2026, 7, 4 ),
)

print( observed )
print( actual )
print( weekend )
```

## Work with Fiscal-Year Date Collections

```python
all_dates = fy.fiscal_dates( )
weekdays = fy.fiscal_weekdays( )
weekends = fy.fiscal_weekends( )
workdays = fy.fiscal_workdays( )

print( len( all_dates ) )
print( len( weekdays ) )
print( len( weekends ) )
print( len( workdays ) )
```

Check whether a date is a workday:

```python
target_date = date( 2026, 7, 3 )
is_workday = target_date in fy.fiscal_workdays( )

print( is_workday )
```

Filter workdays to a reporting period:

```python
start_date = date( 2026, 7, 1 )
end_date = date( 2026, 7, 31 )

period_workdays = \
[
    current_date
    for current_date in fy.fiscal_workdays( )
    if start_date <= current_date <= end_date
]

print( period_workdays )
```

## Use Fiscal with pandas

```python
import pandas as pd
```

Create a fiscal-year DataFrame:

```python
df_fiscal_year = pd.DataFrame(
    [ fy.to_dict( ) ]
)

print( df_fiscal_year )
```

Create a holiday DataFrame:

```python
holiday_rows = \
[
    {
        'Holiday': name,
        'ActualDate': values[ 'actual' ],
        'ObservedDate': values[ 'observed' ],
        'Adjusted': values[ 'actual' ] != values[ 'observed' ],
    }
    for name, values in FederalHoliday( fy.fiscal_year ).holidays( ).items( )
]

df_holidays = pd.DataFrame( holiday_rows )

print( df_holidays )
```

Create a monthly operating calendar:

```python
weekdays = fy.weekdays_by_month( )
weekends = fy.weekends_by_month( )
workdays = fy.workdays_by_month( )
holidays = fy.holidays_by_month( )

monthly_rows = \
[
    {
        'Month': month_name,
        'Weekdays': weekdays[ month_name ],
        'WeekendDays': weekends[ month_name ],
        'Workdays': workdays[ month_name ],
        'FederalHolidays': len( holidays[ month_name ] ),
    }
    for month_name in weekdays
]

df_monthly = pd.DataFrame( monthly_rows )

print( df_monthly )
```

Export the analysis:

```python
df_monthly.to_csv(
    'fiscal-month-summary.csv',
    index=False,
)

df_holidays.to_excel(
    'federal-holidays.xlsx',
    index=False,
)
```

## Validate Fiscal-Year Totals

```python
calculated_weekdays = len( fy.fiscal_weekdays( ) )
calculated_weekends = len( fy.fiscal_weekends( ) )
calculated_workdays = len( fy.fiscal_workdays( ) )

validation = \
{
    'CalendarDaysBalance': (
        calculated_weekdays
        + calculated_weekends
        == fy.fiscal_days_in_year( )
    ),
    'StoredWeekdaysMatch': calculated_weekdays == fy.weekdays,
    'StoredWeekendsMatch': calculated_weekends == fy.weekends,
    'StoredWorkdaysMatch': calculated_workdays == int( fy.workdays ),
}

print( validation )
```

## Application Integration Example

```python
from datetime import date

from fiscal import FiscalYear


def build_fiscal_summary(
    fiscal_year: str,
    start_date: date,
    end_date: date,
) -> dict[ str, object ]:
    fy = FiscalYear( fiscal_year )

    return \
    {
        'FiscalYear': fy.fiscal_year,
        'StartDate': start_date,
        'EndDate': end_date,
        'CalendarDays': ( end_date - start_date ).days + 1,
        'WeekendDays': fy.count_weekends( start_date, end_date ),
        'FederalHolidays': fy.holidays_between( start_date, end_date ),
        'Workdays': fy.count_workdays( start_date, end_date ),
    }


summary = build_fiscal_summary(
    fiscal_year='2026',
    start_date=date( 2026, 7, 1 ),
    end_date=date( 2026, 9, 30 ),
)

print( summary )
```
