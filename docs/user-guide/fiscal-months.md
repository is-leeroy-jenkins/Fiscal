# Fiscal Months

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

## Boundaries and Counts

```python
month_start, month_end = fy.fiscal_month_bounds( 10 )
month_name = fy.fiscal_month_name( 10 )
month_days = fy.fiscal_days_in_month( 10 )
weekdays = fy.weekdays_in_month( 10 )
weekends = fy.weekends_in_month( 10 )
```

## Weekday Occurrences

```python
mondays = fy.weekday_occurrences(
    fiscal_month=10,
    weekday="Monday",
)
```

Full weekday names are accepted case-insensitively. Legacy integers from `0` through `6` remain supported.

## Calendar Matrices

```python
date_rows = fy.fiscal_month_dates( 10 )
day_rows = fy.fiscal_month_day_numbers( 10 )
```

The original compatibility methods remain available:

```python
date_rows = fy.fiscal_month_calendar( 10 )
day_rows = fy.fiscal_month_weeks( 10 )
```
