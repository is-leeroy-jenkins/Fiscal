###### tempus
![](https://github.com/is-leeroy-jenkins/Fiscal/blob/master/resources/images/github/project_tempus.png)

> Modern Federal Fiscal Year & Calendar Utilities for Python  
> Precise, production-ready tools to unify U.S. fiscal year (FY) and calendar year (CY) calculations, 
> including workdays, weekends, and official U.S. federal holidays — all with a clean, well-documented API.



## 📝 Features

- **Federal Fiscal Year Engine**  
  Compute CY, FY, Beginning/Ending FY (BBFY/EBFY), and both calendar/fiscal boundaries.

- **Elapsed & Remaining Counters**  
  Days, months, day-of-year indices, and percent elapsed for both CY and FY.

- **Federal Holiday Logic**  
  Actual and observed U.S. federal holidays, filtered to the active fiscal window.

- **Range Utilities**  
  Count workdays, weekends, and holidays between any two dates.

- **Production-Hardened**  
  Guard clauses, consistent error handling, rich docstrings, and deterministic calculations.



## 🏗️ Installation

- Use pip:

```python 

    pip install tempus
  
```

- Or add via Poetry (pyproject.toml):

```python 

    [tool.poetry.dependencies]
    tempus = "^1.0.0"
  
```



## 🎯 Quick Start

```python 

    from datetime import date
    from tempus import FiscalYear, FederalHoliday
    
```

## 📊 Bind a date to FiscalYear

```python     

    bfy = FiscalYear(date(2025, 8, 27))

    bfy.fiscal_year                     # 2024
    bfy.beginning_fiscal_year, bfy.ending_fiscal_year)  # 2024 2025
    round(bfy.fiscal_percent_elapsed(), 2)             # e.g., 91.23
    
```

## 🚀 Range utilities

```python    

    bfy.count_workdays(date(2025, 8, 1), date(2025, 8, 31))
    bfy.count_weekends(date(2025, 8, 1), date(2025, 8, 31))
    bfy.count_holidays(date(2025, 1, 1), date(2025, 9, 30))
    
```

## ⚡ Holiday checks

```python     

    holiday = FederalHoliday(bfy.fiscal_year)
    holiday.is_holiday(date(2025, 7, 4))    # True (Independence Day)
    holiday.is_weekend(date(2025, 7, 5))    # True (Saturday)
    
```



## 🧠 API Overview

#### Defninitions

##### Fiscal Year 

The fiscal year is the accounting period of the federal government. It begins on October 1 and ends 
on September 30 of the next calendar year. Each fiscal year is identified by the calendar year in 
which it ends and commonly is referred to as "FY." For example, FY2011 began October 1, 2010, and 
ends September 30, 2011.

###### Spending

The key terms of federal spending are budget authority, obligations, outlays, and spendout rate. 
Congress and the President enact budget authority in law. Budget authority allows federal agencies 
to incur obligations, such as entering into contracts, employing personnel, and submitting purchase 
orders. Outlays represent the actual payment of these obligations, usually in the form of electronic 
transfers or checks issued by the Treasury Department. The rate at which budget authority becomes 
outlays in a fiscal year is called the spendout rate, or the outlay rate. The spendout rate varies 
among agencies' accounts depending on the timing of activity in each account.

Budget authority may be made available for obligation for a one-year, multiyear, or no-year period. 
One-year, or annual, budget authority is available for obligation only during a specific fiscal year, 
and any unobligated authority expires at the end of that fiscal year; multiyear budget authority is 
available for a specified period longer than one fiscal year; and no-year budget authority is 
available for an indefinite period (i.e., until expended).

Typically, new budget authority is provided in the form of permanent appropriations or annual 
appropriations. Permanent appropriations provide new budget authority each year without any annual 
legislative action. Usually, this type of new budget authority is provided in legislation 
authorizing the program, such as in the case of most entitlement programs (e.g., Social Security benefits). 
Annual appropriations, on the other hand, generally provide new budget authority for the particular 
fiscal year for which they were enacted. In some cases, new budget authority in annual appropriations 
acts is made available for more than one year, or for a future fiscal year. Annual appropriations 
are provided in the regular appropriations bills enacted by Congress and the President each year. 
Annual appropriations also may be provided in supplemental appropriations acts and continuing 
appropriations acts (often referred to as continuing resolutions).

New budget authority also may be made available to agencies in the form of borrowing authority, 
contract authority, and the authority to spend offsetting collections. Borrowing authority and 
contract authority allow agencies to borrow funds and enter into contracts prior to enactment of 
appropriations. Spending authority from offsetting collections may be provided to allow agencies to 
obligate and spend funds, such as fees, collected from the public for certain market-oriented activities. 
Offsetting collections are deducted from gross budget authority and outlays at the account or higher level.

- calendar: `calendar_day_of_year()`, `calendar_days_in_year()`, `calendar_elapsed_days()`, `calendar_remaining_days()`, `calendar_elapsed_months()`, `calendar_remaining_months()`, `calendar_percent_elapsed()`
- fiscal: `fiscal_day_of_year()`, `fiscal_days_in_year()`, `fiscal_month_number()`, `fiscal_elapsed_days()`, `fiscal_remaining_days()`, `fiscal_elapsed_months()`, `fiscal_remaining_months()`, `fiscal_percent_elapsed()`
- ranges: `count_weekends(start, end)`, `count_holidays(start, end)`, `count_workdays(start, end)`
- bounds & checks: `calendar_bounds()`, `fiscal_bounds()`, `is_calendar_year_start()`, `is_calendar_year_end()`, `is_fiscal_year_start()`, `is_fiscal_year_end()`

#### Federal Holiday

- `holidays() -> dict` — holiday map with `actual` and `observed` dates within the FY window  
- `is_holiday(date, use_observed=True) -> bool`  
- `is_weekend(date) -> bool`



## 📝 Design Notes

- **FY Naming**: FY is named for its ending year. For example, FY 2026 runs 2025-10-01 through 2026-09-30.  
- **Observed Dates**: Saturday holidays observe on Friday; Sunday on Monday.  
- **Juneteenth**: Included from FY 2021 forward.  
- **Determinism**: All calculations are pure functions of the input date(s); no I/O or timezone side-effects.



## 🏁 Roadmap

- ISO week numbers and fiscal week helpers  
- Optional state/local holiday overlays  
- CLI (`tempus`) for shell-friendly queries  
- Pandas integration for DataFrame fiscal transformations



## 📜 [License](https://github.com/is-leeroy-jenkins/Tempus/blob/master/LICENSE.txt)

- MIT © 2022 Terry D. Eppler
