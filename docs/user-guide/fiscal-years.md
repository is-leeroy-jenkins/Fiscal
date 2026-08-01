# Fiscal Years

## Load a Fiscal Year

```python
from fiscal import FiscalYear

fy = FiscalYear(
    fy=2026,
)
```

Fiscal accepts integer or string fiscal-year values.

```python
fy_text = FiscalYear( "2026" )
fy_number = FiscalYear( 2026 )
```

## Load a Multi-Year Availability Record

```python
fy = FiscalYear(
    fy=2026,
    bpoa=2024,
    epoa=2026,
)
```

## Read Fiscal Metadata

```python
print( fy.start_date )
print( fy.end_date )
print( fy.expiration_date )
print( fy.cancellation_date )
print( fy.availability )
print( fy.type )
```

## Stored Counts

```python
print( fy.weekdays )
print( fy.weekends )
print( fy.workdays )
print( fy.compensable_days )
print( fy.compensable_workdays )
print( fy.compensable_hours )
```
