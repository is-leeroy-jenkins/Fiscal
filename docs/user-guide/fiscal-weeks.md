# Fiscal Weeks

Fiscal weeks are consecutive seven-day periods beginning on the fiscal-year start date. The final week is truncated at the fiscal-year end date.

## Current Fiscal Week

```python
week_number = fy.fiscal_week_number( )
```

## Week Boundaries

```python
week_start, week_end = fy.fiscal_week_bounds(
    fiscal_week=1,
)
```

The ISO calendar week is separate:

```python
iso_week = fy.calendar_week_number( )
```
