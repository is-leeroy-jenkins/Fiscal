'''
    ******************************************************************************************
      Assembly:                Fiscal 
      Filename:                __init__.py
      Author:                  Terry D. Eppler
      Created:                 08-26-2025

      Last Modified By:        Terry D. Eppler
      Last Modified On:        08-26-2025
    ******************************************************************************************
    <copyright file="budget_fiscal_year.py" company="Terry D. Eppler">

         Budget Fiscal Year Tools

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

    </copyright>
    <summary>
        __init__.py
    </summary>
    ******************************************************************************************
'''
from __future__ import annotations
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple, Optional
import calendar
from boogr import Error
import config as cfg
import numpy as np
import pandas as pd
import sqlite3


def throw_if( name: str, value: object ) -> None:
	"""Throw if.
    
        Purpose:
            Provides the throw if helper used by the Gipity Streamlit application. The function
            supports UI state management, provider coordination, data normalization, or display
            behavior required by the surrounding workflow.
    
        Args:
            name (str): Value supplied to the helper.
            value (object): Value supplied to the helper.
    
        Raises:
            Error: Re-raised after the exception is wrapped and written to the application logger.
    """
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be empty!' )
	if isinstance( value, str ) and (not value.strip( )):
		raise ValueError( f'Argument "{name}" cannot be empty!' )
	if isinstance( value, (list, tuple, dict, set) ) and len( value ) == 0:
		raise ValueError( f'Argument "{name}" cannot be empty!' )

def to_date( value: date ) -> date:
	"""Convert a supported value to a date.
	
	Purpose:
	    Normalizes a date-like value to ``datetime.date``. A ``None`` value resolves to the
	    current date.
	
	Args:
	    value (date): Date-like value to normalize.
	
	Returns:
	    date: Normalized calendar date.
	"""
	if value is None:
		return date.today( )
	if isinstance( value, datetime ):
		return value.date( )
	if isinstance( value, date ):
		return value

def create_connection( ) -> sqlite3.Connection:
	"""Create a connection to the configured SQLite database.

	Purpose:
	    Opens a new SQLite connection using the database path defined by the application
	    configuration.

	Returns:
	    sqlite3.Connection: Open SQLite database connection.
	"""
	return sqlite3.connect( cfg.DB_PATH )

class BFY( ):
	'''Base class for the Fiscal Year class
	
	Purpose:
	    Encapsulates fiscal-year functions. The class derives fiscal-year identifiers
	    and boundaries, calendar-year boundaries, elapsed and
	    remaining periods, completion percentages, workday counts, weekend counts, and holiday
	    checks.
	
	Attributes:
		id (int) : The Fiscal Year rowid
	    current_date (date | None): Input date used to initialize the instance.
	    calendar_year (int | None): Calendar year containing the reference date.
	    fiscal_year (str | None): Federal fiscal year containing the reference date.
	
	'''
	path: Optional[ str ]
	table: Optional[ str ]
	data: Optional[ pd.DataFrame ]
	connection: Optional[ sqlite3.Connection ]
	
	def __init__( self ) -> None:
		"""Initialize fiscal-year data.
		
		Purpose:
		    Initializes the instance of a dataframes.
		
		Args:
		    path (str): The fiscal year.
		    data (pd.DataFrame): The beginning period of availability
		    connection (sqlite3.Connection): The ending period of availability
		
		Returns:
		    None: Initialization does not return a value.
		"""
		self.path = cfg.DB_PATH
		
class FiscalYear( ):
	"""United States federal fiscal-year calculations.
	
	Purpose:
	    Encapsulates fiscal-year functions. The class derives fiscal-year identifiers
	    and boundaries, calendar-year boundaries, elapsed and
	    remaining periods, completion percentages, workday counts, weekend counts, and holiday
	    checks.
	
	Attributes:
		id (int) : The Fiscal Year rowid
	    current_date (date | None): Input date used to initialize the instance.
	    calendar_year (int | None): Calendar year containing the reference date.
	    fiscal_year (str | None): Federal fiscal year containing the reference date.
	    bpoa (str | None): Beginning period of availability.
	    epoa (str | None): Ending period of avialability.
	    start_date (datetime | None): First day of the fiscal year.
	    end_date (datetime | None): Last day of the fiscal year.
	    expiration_date (datetime | None): First day of the federal fiscal year.
	    cancellation_date (datetime | None): Last day of the federal fiscal year.
	    weekends (int): The number of weekends in the fiscal year.
	    weekdays (int): The number of days that are not weekends.
	    workdays (int): The number of days that are not weekends or holidays.
	    compensable_workdays (float): The maximum number of days worked.
	    compensable_hours (float): The maximum number of hours worked.
	"""
	id: Optional[ int ]
	current_date: Optional[ datetime ]
	calendar_year: Optional[ int ]
	fiscal_year: Optional[ str ]
	bpoa: Optional[ str ]
	epoa: Optional[ str ]
	start_date: Optional[ datetime ]
	end_date: Optional[ datetime ]
	expiration_date: Optional[ datetime ]
	cancellation_date: Optional[ datetime ]
	weekends: Optional[ int ]
	weekdays: Optional[ int ]
	workdays: Optional[ float ]
	compensable_workdays: Optional[ float ]
	compensable_hours: Optional[ float ]
	
	def __init__( self, year: str, bpoa: str=None, epoa: str=None ) -> None:
		"""Initialize fiscal-year state.
		
		Purpose:
		    Initializes the instance from a reference datetime and derives its calendar-year and
		    fiscal-year fields.
		
		Args:
		    year (str): The fiscal year.
		    bpoa (str): The beginning period of availability
		    epoa (str): The ending period of availability
		
		Returns:
		    None: Initialization does not return a value.
		"""
		self.current_date = datetime( ).date( )
		self.fiscal_year = year
		self.calendar_year = datetime( ).year
		self.bpoa = bpoa
		self.epoa = epoa
		self.start_date = None
		self.end_date = None
		self.expiration_date = None
		self.cancellation_date = None
		self.weekdays = 0
		self.weekends = 0
		self.workdays = 0.0
		self.compensable_workdays = 0.0
		self.compensable_hours = 0.0
		
	def __repr__( self ) -> str:
		"""Return a diagnostic representation.
		
		Purpose:
		    Produces a concise representation containing the reference date, calendar year, fiscal
		    year, beginning fiscal year, and ending fiscal year.
		
		Returns:
		    str: Human-readable fiscal-year summary.
		"""
		return self.fiscal_year
	
	def calendar_days_elapsed( self ) -> int:
		"""Return elapsed calendar-year days.
		
		Purpose:
		    Calculates the number of completed days since the start of the calendar year.
		
		Returns:
		    int: Number of elapsed calendar-year days.
		
		Raises:
		    Error: The elapsed-day count cannot be calculated.
		"""
		try:
			return max( 0, ( self.current_date - datetime( self.calendar_year, 1, 1 ) ).days )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'calendar_days_elapsed( self ) -> int'
			raise exception
	
	def calendar_days_remaining( self ) -> int:
		"""Return remaining calendar-year days.
		
		Purpose:
		    Calculates the number of days after the reference date through the end of the calendar
		    year.
		
		Returns:
		    int: Number of remaining calendar-year days.
		
		Raises:
		    Error: The remaining-day count cannot be calculated.
		"""
		try:
			return max( 0, ( datetime( self.calendar_year, 1, 1 ) - self.current_date ).days )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'calendar_days_remaining( self ) -> int'
			raise exception
	
	def calendar_elapsed_months( self ) -> int:
		"""Return elapsed calendar-year months.
		
		Purpose:
		    Calculates the number of completed months preceding the reference month in the calendar
		    year.
		
		Returns:
		    int: Number of elapsed calendar-year months from 0 through 11.
		
		Raises:
		    Error: The elapsed-month count cannot be calculated.
		"""
		try:
			return max( 0, self.date.month - 1 )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'calendar_elapsed_months( self ) -> int'
			raise exception
	
	def calendar_remaining_months( self ) -> int:
		"""Return remaining calendar-year months.
		
		Purpose:
		    Calculates the number of months following the reference month in the calendar year.
		
		Returns:
		    int: Number of remaining calendar-year months from 0 through 11.
		
		Raises:
		    Error: The remaining-month count cannot be calculated.
		"""
		try:
			return 12 - self.date.month
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'calendar_remaining_months( self ) -> int'
			raise exception
	
	def calendar_percent_elapsed( self ) -> float:
		"""Return the elapsed calendar-year percentage.
		
		Purpose:
		    Calculates the percentage of the calendar year completed before the reference date.
		
		Returns:
		    float: Elapsed calendar-year percentage from 0.0 through 100.0.
		
		Raises:
		    Error: The elapsed percentage cannot be calculated.
		"""
		try:
			completed = self.calendar_days_elapsed( )
			total = self.calendar_days_in_year( )
			return (completed / total) * 100.0
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'calendar_percent_elapsed( self ) -> float'
			raise exception
	
	def fiscal_day_of_year( self ) -> int:
		"""Return the fiscal day-of-year index.
		
		Purpose:
		    Calculates the one-based day number within the federal fiscal year.
		
		Returns:
		    int: Fiscal day-of-year value from 1 through 366.
		
		Raises:
		    Error: The fiscal day-of-year value cannot be calculated.
		"""
		try:
			return (self.current_date - self.start_date) + 1
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_day_of_year( self ) -> int'
			raise exception
	
	def fiscal_days_in_year( self ) -> int:
		"""Return the number of days in the fiscal year.
		
		Purpose:
		    Calculates the total length of the federal fiscal year containing the reference date.
		
		Returns:
		    int: Total fiscal-year days, either 365 or 366.
		
		Raises:
		    Error: The fiscal-year length cannot be calculated.
		"""
		try:
			return (self.end_date - self.start_date).days + 1
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_days_in_year( self ) -> int'
			raise exception
	
	def fiscal_month_number( self ) -> int:
		"""Return the fiscal month number.
		
		Purpose:
		    Converts the calendar month to its federal fiscal-month position, where October is
		    month
		    1 and September is month 12.
		
		Returns:
		    int: Fiscal month number from 1 through 12.
		
		Raises:
		    Error: The fiscal month number cannot be calculated.
		"""
		try:
			m = self.date.month
			return ((m - 10) % 12) + 1
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_month_number( self ) -> int'
			raise exception
	
	def fiscal_days_elapsed( self ) -> int:
		"""Return elapsed fiscal-year days.
		
		Purpose:
		    Calculates the number of completed days since the start of the federal fiscal year.
		
		Returns:
		    int: Number of elapsed fiscal-year days.
		
		Raises:
		    Error: The elapsed fiscal-day count cannot be calculated.
		"""
		try:
			return max( 0, (self.date - self.start_date) )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_days_elapsed( self ) -> int'
			raise exception
	
	def fiscal_days_remaining( self ) -> int:
		"""Return remaining fiscal-year days.
		
		Purpose:
		    Calculates the number of days after the reference date through the end of the federal
		    fiscal year.
		
		Returns:
		    int: Number of remaining fiscal-year days.
		
		Raises:
		    Error: The remaining fiscal-day count cannot be calculated.
		"""
		try:
			return max( 0, (self.end_date - self.date).days )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_days_remaining( self ) -> int'
			raise exception
	
	def fiscal_months_elapsed( self ) -> int:
		"""Return elapsed fiscal-year months.
		
		Purpose:
		    Calculates the number of completed months preceding the reference fiscal month.
		
		Returns:
		    int: Number of elapsed fiscal-year months from 0 through 11.
		
		Raises:
		    Error: The elapsed fiscal-month count cannot be calculated.
		"""
		try:
			return self.fiscal_month_number( ) - 1
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_months_elapsed( self ) -> int'
			raise exception
	
	def fiscal_months_remaining( self ) -> int:
		"""Return remaining fiscal-year months.
		
		Purpose:
		    Calculates the number of months following the reference fiscal month.
		
		Returns:
		    int: Number of remaining fiscal-year months from 0 through 11.
		
		Raises:
		    Error: The remaining fiscal-month count cannot be calculated.
		"""
		try:
			return 12 - self.fiscal_month_number( )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_months_remaining( self ) -> int'
			raise exception
	
	def fiscal_percent_elapsed( self ) -> float:
		"""Return the elapsed fiscal-year percentage.
		
		Purpose:
		    Calculates the percentage of the federal fiscal year completed before the reference
		    date.
		
		Returns:
		    float: Elapsed fiscal-year percentage from 0.0 through 100.0.
		
		Raises:
		    Error: The elapsed fiscal-year percentage cannot be calculated.
		"""
		try:
			completed = self.fiscal_days_elapsed( )
			total = self.fiscal_days_in_year( )
			return (completed / total) * 100.0
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_percent_elapsed( self ) -> float'
			raise exception
	
	def count_weekends( self, start: datetime, end: datetime ) -> int:
		"""Count weekend days in an inclusive range.
		
		Purpose:
		    Counts Saturdays and Sundays between the supplied start and end dates, including both
		    endpoints.
		
		Args:
		    start (datetime): First date in the range.
		    end (datetime): Last date in the range.
		
		Returns:
		    int: Number of weekend days in the range, or 0 when ``start`` follows ``end``.
		
		Raises:
		    Error: The weekend count cannot be calculated.
		"""
		try:
			s, e = to_date( start ), to_date( end )
			if s > e:
				return 0
			count = 0
			cur = s
			while cur <= e:
				if cur.weekday( ) >= 5:
					count += 1
				cur += timedelta( days=1 )
			return count
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'count_weekends(self, start, end)'
			raise exception
	
	def count_holidays( self, start: datetime, end: datetime, use_observed: bool = True ) -> int:
		"""Count federal holidays in an inclusive range.
		
		Purpose:
		    Counts actual or observed federal holidays between the supplied start and end dates for
		    the instance fiscal year.
		
		Args:
		    start (datetime): First date in the range.
		    end (datetime): Last date in the range.
		    use_observed (bool): Whether to count observed dates instead of actual dates.
		
		Returns:
		    int: Number of qualifying federal holidays, or 0 when ``start`` follows ``end``.
		
		Raises:
		    Error: The holiday count cannot be calculated.
		"""
		try:
			s, e = to_date( start ), to_date( end )
			if s > e:
				return 0
			fh = FederalHoliday( self.fiscal_year )
			hols = fh.holidays( )
			key = 'observed' if use_observed else 'actual'
			return sum( 1 for payload in hols.values( ) if s <= payload[ key ] <= e )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'count_holidays(self, start, end)'
			raise exception
	
	def count_workdays( self, start: datetime, end: datetime, use_observed: bool = True ) -> int:
		"""Count workdays in an inclusive range.
		
		Purpose:
		    Counts Monday-through-Friday dates that are not federal holidays between the supplied
		    start and end dates.
		
		Args:
		    start (datetime): First date in the range.
		    end (datetime): Last date in the range.
		    use_observed (bool): Whether observed holiday dates are excluded instead of actual
		    dates.
		
		Returns:
		    int: Number of workdays in the range, or 0 when ``start`` follows ``end``.
		
		Raises:
		    Error: The workday count cannot be calculated.
		"""
		try:
			s, e = to_date( start ), to_date( end )
			if s > e:
				return 0
			fh = FederalHoliday( self.fiscal_year )
			hols = fh.holidays( )
			hset = { payload[ 'observed' if use_observed else 'actual' ] for payload in
				hols.values( ) }
			count, cur = 0, s
			while cur <= e:
				if cur.weekday( ) < 5 and cur not in hset:
					count += 1
				cur += timedelta( days=1 )
			return count
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'count_workdays(self, start, end)'
			raise exception
	
	def calendar_bounds( self ) -> Tuple[ date, date ]:
		"""Return calendar-year boundaries.
		
		Purpose:
		    Provides the first and last dates of the calendar year containing the reference date.
		
		Returns:
		    Tuple[date, date]: Calendar-year start and end dates.
		
		Raises:
		    Error: The calendar-year boundaries cannot be returned.
		"""
		try:
			return (self.cy_start_date, self.cy_end_date)
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = ''
			raise exception
	
	def fiscal_bounds( self ) -> Tuple[ date, date ]:
		"""Return fiscal-year boundaries.
		
		Purpose:
		    Provides the first and last dates of the federal fiscal year containing the reference
		    date.
		
		Returns:
		    Tuple[date, date]: Fiscal-year start and end dates.
		
		Raises:
		    Error: The fiscal-year boundaries cannot be returned.
		"""
		try:
			return self.start_date, self.end_date
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'fiscal_bounds( self ) -> Tuple[ date, date ]'
			raise exception
	
	def is_fiscal_start_year( self ) -> bool:
		"""Determine whether the date starts the fiscal year.
		
		Purpose:
		    Tests whether the reference date is October 1, the first day of the federal fiscal
		    year.
		
		Returns:
		    bool: ``True`` when the reference date is the fiscal-year start; otherwise ``False``.
		
		Raises:
		    Error: The fiscal-year boundary test cannot be completed.
		"""
		try:
			return self.date == self.start_date
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = 'is_fiscal_start_year( self ) -> bool'
			raise exception
	
	def is_fiscal_end_year( self ) -> bool:
		"""Determine whether the date ends the fiscal year.
		
		Purpose:
		    Tests whether the reference date is September 30, the final day of the federal fiscal
		    year.
		
		Returns:
		    bool: ``True`` when the reference date is the fiscal-year end; otherwise ``False``.
		
		Raises:
		    Error: The fiscal-year boundary test cannot be completed.
		"""
		try:
			return self.date == self.end_date
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = ''
			raise exception
	
	def is_calendar_start_year( self ) -> bool:
		"""Determine whether the date starts the calendar year.
		
		Purpose:
		    Tests whether the reference date is January 1.
		
		Returns:
		    bool: ``True`` when the reference date is the calendar-year start; otherwise ``False``.
		
		Raises:
		    Error: The calendar-year boundary test cannot be completed.
		"""
		try:
			return self.date == self.cy_start_date
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = ''
			raise exception
	
	def is_calendar_end_date( self ) -> bool:
		"""Determine whether the date ends the calendar year.
		
		Purpose:
		    Tests whether the reference date is December 31.
		
		Returns:
		    bool: ``True`` when the reference date is the calendar-year end; otherwise ``False``.
		
		Raises:
		    Error: The calendar-year boundary test cannot be completed.
		"""
		try:
			return self.date == self.cy_end_date
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FiscalYear'
			exception.method = ''
			raise exception
	
	def to_dict( self ) -> Dict[ str, object ]:
		"""Return the fiscal-year state as a dictionary.
		
		Purpose:
		    Exports the reference date, fiscal-year identifiers, and calendar and fiscal
		    boundaries as
		    a structured mapping.
		
		Returns:
		    Dict[str, object]: Mapping containing the current fiscal-year and calendar-year state.
		"""
		return { 'date': self.date, 'calendar_year': self.calendar_year,
			'fiscal_year': self.fiscal_year, 'beginning_fiscal_year': self.bpoa,
			'ending_fiscal_year': self.epoa, 'cy_start_date': self.cy_start_date,
			'cy_end_date': self.cy_end_date, 'fy_start_date': self.start_date,
			'fy_end_date': self.end_date, }

class FederalHoliday( ):
	"""United States federal holidays for a fiscal year.
	
	Purpose:
	    Calculates actual and observed federal holiday dates whose observed dates fall within a
	    specified federal fiscal year.
	
	Attributes:
	    fiscal_year (int): Fiscal year identified by its ending calendar year.
	    fy_start_date (date): First day of the fiscal year.
	    fy_end_date (date): Last day of the fiscal year.
	    holidays (Dict[str, Dict[str, date]]): Holiday names mapped to actual and observed dates.
	"""
	fiscal_year: int
	fy_start_date: date
	fy_end_date: date
	holidays: Dict[ str, Dict[ str, date ] ]
	
	def __init__( self, fiscal_year: int ) -> None:
		"""Initialize federal-holiday calculations.
		
		Purpose:
		    Initializes the fiscal-year boundaries used to calculate federal holidays.
		
		Args:
		    fiscal_year (int): Fiscal year identified by its ending calendar year.
		
		Returns:
		    None: Initialization does not return a value.
		"""
		self.fiscal_year = int( fiscal_year )
		self.fy_start_date = date( self.fiscal_year - 1, 10, 1 )
		self.fy_end_date = date( self.fiscal_year, 9, 30 )
	
	def _observed_date( self, d: date ) -> date | None:
		"""Return the observed holiday date.
		
		Purpose:
		    Moves a Saturday holiday to the preceding Friday and a Sunday holiday to the following
		    Monday. Weekday holidays retain their actual date.
		
		Args:
		    d (date): Actual holiday date.
		
		Returns:
		    date | None: Observed holiday date.
		
		Raises:
		    Error: The observed date cannot be calculated.
		"""
		try:
			if d.weekday( ) == 5:
				return d - timedelta( days=1 )
			if d.weekday( ) == 6:
				return d + timedelta( days=1 )
			return d
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = ''
			raise exception
	
	def _nth_weekday_of_month( self, year: int, month: int, weekday: int, n: int ) -> date | None:
		"""Return the nth weekday of a month.
		
		Purpose:
		    Calculates a specified occurrence of a weekday within a calendar month.
		
		Args:
		    year (int): Calendar year.
		    month (int): Calendar month from 1 through 12.
		    weekday (int): Weekday index from 0 for Monday through 6 for Sunday.
		    n (int): One-based weekday occurrence within the month.
		
		Returns:
		    date | None: Date of the requested weekday occurrence.
		
		Raises:
		    Error: The requested weekday occurrence cannot be calculated.
		"""
		try:
			cal = calendar.Calendar( )
			matches = [ d for d in cal.itermonthdates( year, month ) if
				d.month == month and d.weekday( ) == weekday ]
			return matches[ n - 1 ]
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = ''
			raise exception
	
	def _last_weekday_of_month( self, year: int, month: int, weekday: int ) -> date | None:
		"""Return the final weekday of a month.
		
		Purpose:
		    Calculates the last occurrence of a specified weekday within a calendar month.
		
		Args:
		    year (int): Calendar year.
		    month (int): Calendar month from 1 through 12.
		    weekday (int): Weekday index from 0 for Monday through 6 for Sunday.
		
		Returns:
		    date | None: Date of the final requested weekday.
		
		Raises:
		    Error: The final weekday occurrence cannot be calculated.
		"""
		try:
			cal = calendar.Calendar( )
			matches = [ d for d in cal.itermonthdates( year, month ) if
				d.month == month and d.weekday( ) == weekday ]
			return matches[ -1 ]
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = ''
			raise exception
	
	def _add_holiday( self, hols: Dict[ str, Dict[ str, date ] ], name: str, actual: date ) -> \
			None:
		"""Add a holiday to a holiday mapping.
		
		Purpose:
		    Adds the holiday when its observed date falls within the configured fiscal-year
		    boundaries.
		
		Args:
		    hols (Dict[str, Dict[str, date]]): Holiday mapping being constructed.
		    name (str): Holiday name.
		    actual (date): Actual holiday date.
		
		Returns:
		    None: The method updates the supplied mapping and does not return a value.
		
		Raises:
		    Error: The holiday cannot be added to the mapping.
		"""
		try:
			obs = self._observed_date( actual )
			if self.fy_start_date <= obs <= self.fy_end_date:
				hols[ name ] = { 'actual': actual, 'observed': obs }
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = ''
			raise exception
	
	def holidays( self ) -> Dict[ str, Dict[ str, date ] ] | None:
		"""Return federal holidays for the fiscal year.
		
		Purpose:
		    Calculates actual and observed dates for United States federal holidays whose observed
		    dates fall between October 1 of the preceding calendar year and September 30 of the
		    fiscal
		    year.
		
		Returns:
		    Dict[str, Dict[str, date]] | None: Holiday names mapped to ``actual`` and ``observed``
		        dates.
		
		Raises:
		    Error: The federal-holiday mapping cannot be calculated.
		"""
		try:
			hols: Dict[ str, Dict[ str, date ] ] = { }
			start = self.fy_start_date.year
			end = self.fiscal_year
			self._add_holiday( hols, r'Columbus Day',
				self._nth_weekday_of_month( start, 10, calendar.MONDAY, 2 ) )
			self._add_holiday( hols, r'Veterans Day', date( start, 11, 11 ) )
			self._add_holiday( hols, r'Thanksgiving Day',
				self._nth_weekday_of_month( start, 11, calendar.THURSDAY, 4 ) )
			self._add_holiday( hols, r'Christmas Day', date( start, 12, 25 ) )
			self._add_holiday( hols, r"New Year's Day", date( end, 1, 1 ) )
			self._add_holiday( hols, r'Birthday of Martin Luther King, Jr.',
				self._nth_weekday_of_month( end, 1, calendar.MONDAY, 3 ) )
			self._add_holiday( hols, r"Washington's Birthday",
				self._nth_weekday_of_month( end, 2, calendar.MONDAY, 3 ) )
			self._add_holiday( hols, r'Memorial Day',
				self._last_weekday_of_month( end, 5, calendar.MONDAY ) )
			self._add_holiday( hols, r'Juneteenth National Independence Day', date( end, 6, 19 ) )
			self._add_holiday( hols, r'Independence Day', date( end, 7, 4 ) )
			self._add_holiday( hols, r'Labor Day',
				self._nth_weekday_of_month( end, 9, calendar.MONDAY, 1 ) )
			return hols
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = 'holidays( self ) -> Dict[ str, Dict[ str, date ] ]'
			raise exception
	
	def is_holiday( self, when: datetime, observed: bool = True ) -> bool | None:
		"""Determine whether a date is a federal holiday.
		
		Purpose:
		    Tests the supplied date against the actual or observed federal holiday dates for the
		    configured fiscal year.
		
		Args:
		    when (datetime): Date to evaluate.
		    observed (bool): Whether to compare against observed dates instead of actual dates.
		
		Returns:
		    bool | None: ``True`` when the date is a holiday; otherwise ``False``.
		
		Raises:
		    Error: The holiday test cannot be completed.
		"""
		try:
			d = to_date( when )
			hols = self.holidays( )
			if observed:
				return any( d == payload[ 'observed' ] for payload in hols.values( ) )
			return any( d == payload[ 'actual' ] for payload in hols.values( ) )
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = ('is_holiday( self, when: datetime, use_observed: bool=True ) -> '
			                    'bool')
			raise exception
	
	def is_weekend( self, when: datetime ) -> bool | None:
		"""Determine whether a date falls on a weekend.
		
		Purpose:
		    Tests whether the supplied date is Saturday or Sunday.
		
		Args:
		    when (datetime): Date to evaluate.
		
		Returns:
		    bool | None: ``True`` for Saturday or Sunday; otherwise ``False``.
		
		Raises:
		    Error: The weekend test cannot be completed.
		"""
		try:
			throw_if( 'when', when )
			d = to_date( when )
			return d.weekday( ) >= 5
		except Exception as e:
			exception = Error( e )
			exception.module = 'fiscal'
			exception.cause = 'FederalHoliday'
			exception.method = 'is_weekend( self, when: datetime ) -> bool '
			raise exception
