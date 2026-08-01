# Data Exports

## Fiscal-Year Dictionary

```python
record = fy.to_dict( )
```

## Federal-Holiday Dictionary

```python
from fiscal import FederalHoliday

holidays = FederalHoliday( 2026 )
record = holidays.to_dict( )
```

## pandas DataFrames

```python
import pandas as pd

df_fiscal_year = pd.DataFrame(
    [ fy.to_dict( ) ]
)

df_months = pd.DataFrame(
    [
        {
            "Month": month,
            "Weekdays": fy.weekdays_by_month( )[ month ],
            "WeekendDays": fy.weekends_by_month( )[ month ],
            "Workdays": fy.workdays_by_month( )[ month ],
            "FederalHolidays": len( fy.holidays_by_month( )[ month ] ),
        }
        for month in fy.dates_by_month( )
    ]
)
```

## CSV Export

```python
df_months.to_csv(
    "fiscal-month-summary.csv",
    index=False,
)
```
