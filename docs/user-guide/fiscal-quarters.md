# Fiscal Quarters

| Quarter | Fiscal Months | Calendar Months |
|---:|---|---|
| 1 | 1–3 | October–December |
| 2 | 4–6 | January–March |
| 3 | 7–9 | April–June |
| 4 | 10–12 | July–September |

## Current Quarter

```python
quarter = fy.fiscal_quarter_number( )
```

## Quarter Boundaries

```python
quarter_start, quarter_end = fy.fiscal_quarter_bounds( 4 )
quarter_days = fy.fiscal_days_in_quarter( 4 )
```

## Quarter Summary

```python
summary = {
    "StartDate": quarter_start,
    "EndDate": quarter_end,
    "CalendarDays": quarter_days,
    "WeekendDays": fy.count_weekends( quarter_start, quarter_end ),
    "Holidays": fy.count_holidays( quarter_start, quarter_end ),
    "Workdays": fy.count_workdays( quarter_start, quarter_end ),
}
```
