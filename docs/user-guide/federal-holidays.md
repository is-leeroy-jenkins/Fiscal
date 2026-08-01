# Federal Holidays

## Load Holiday Records

```python
from datetime import date
from fiscal import FederalHoliday

holidays = FederalHoliday( 2026 )
```

## Actual and Observed Dates

```python
holiday_map = holidays.holidays( )
independence_day = holiday_map[ "Independence Day" ]

print( independence_day[ "actual" ] )
print( independence_day[ "observed" ] )
```

## Check a Date

```python
print(
    holidays.is_holiday(
        when=date( 2026, 7, 3 ),
        observed=True,
    )
)
```

## Observed-Date Rules

- Saturday: preceding Friday
- Sunday: following Monday
- Monday through Friday: unchanged

```python
observed = holidays.observed_date(
    date( 2026, 7, 4 ),
)
```
