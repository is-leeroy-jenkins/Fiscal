# Calendar Rendering

Calendar rendering is integrated directly into `FiscalYear`. No additional classes are required.

## Fiscal-Month Text Calendar

```python
text = fy.fiscal_month_text_calendar(
    fiscal_month=10,
)

print( text )
```

## Fiscal-Year Text Calendar

```python
text = fy.fiscal_year_text_calendar( )
```

The output follows fiscal order from October through September.

## Fiscal-Month HTML Calendar

```python
html = fy.fiscal_month_html_calendar(
    fiscal_month=10,
    with_year=True,
)
```

## Fiscal-Year HTML Calendar

```python
html = fy.fiscal_year_html_calendar(
    width=3,
)
```

## Date-Range Text Calendar

```python
from datetime import date

text = fy.date_range_text_calendar(
    start=date( 2026, 7, 1 ),
    end=date( 2026, 9, 30 ),
)
```

## Date-Range HTML Calendar

```python
html = fy.date_range_html_calendar(
    start=date( 2026, 7, 1 ),
    end=date( 2026, 9, 30 ),
    width=3,
    with_year=True,
)
```

Range renderers include each calendar month that intersects the inclusive range. The first and final month are rendered as complete month calendars.
