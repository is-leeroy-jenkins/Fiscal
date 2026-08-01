# Workdays and Weekends

## Fiscal-Year Collections

```python
all_dates = fy.fiscal_dates( )
weekday_dates = fy.fiscal_weekdays( )
weekend_dates = fy.fiscal_weekends( )
workday_dates = fy.fiscal_workdays( )
```

Observed holidays are excluded from workdays by default.

```python
actual_date_workdays = fy.fiscal_workdays(
    use_observed=False,
)
```

## Monthly Counts

```python
weekdays = fy.weekdays_by_month( )
weekends = fy.weekends_by_month( )
workdays = fy.workdays_by_month( )
holidays = fy.holidays_by_month( )
```

## Remaining Counts

```python
remaining = {
    "Holidays": fy.holidays_remaining( ),
    "Workdays": fy.workdays_remaining( ),
    "WeekendDays": fy.weekends_remaining( ),
}
```
