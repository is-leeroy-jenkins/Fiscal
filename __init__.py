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
import sqlite3
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import config as cfg
from boogr import Error

__all__: tuple[ str, ... ] = ('DB', 'FederalHoliday', 'FiscalYear', 'throw_if', 'to_date',)

def throw_if( name: str, value: object ) -> None:
	"""Validate a required argument.

	Purpose:
		Raises ``ValueError`` when a required argument is ``None``, an empty string, or an empty
		collection.

	Args:
		name (str): Name of the argument being validated.
		value (object): Argument value to validate.

	Returns:
		None: Validation does not return a value.

	Raises:
		ValueError: The supplied value is empty.
	"""
	if value is None:
		raise ValueError( f'Argument "{name}" cannot be empty!' )
	if isinstance( value, str ) and not value.strip( ):
		raise ValueError( f'Argument "{name}" cannot be empty!' )
	if isinstance( value, (list, tuple, dict, set) ) and len( value ) == 0:
		raise ValueError( f'Argument "{name}" cannot be empty!' )

def to_date( value: date | datetime | str | None ) -> Optional[ date ]:
	"""Convert a supported value to ``datetime.date``.

	Purpose:
		Converts date objects, datetime objects, ISO date text, and month/day/year text into a
		``datetime.date`` value. Database sentinel values resolve to ``None``.

	Args:
		value (date | datetime | str | None): Value to convert.

	Returns:
		date | None: Converted date or ``None`` for a database sentinel value.

	Raises:
		ValueError: The supplied text cannot be parsed as a supported date.
		TypeError: The supplied value is not a supported date type.
	"""
	if value is None:
		return None
	if isinstance( value, datetime ):
		return value.date( )
	if isinstance( value, date ):
		return value
	if isinstance( value, str ):
		text = value.strip( )
		if text.upper( ) in ('', 'NS', 'N/A', 'NA', 'NONE', 'NULL'):
			return None
		for date_format in ('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'):
			try:
				return datetime.strptime( text, date_format ).date( )
			except ValueError:
				continue
		raise ValueError( f'Unsupported date text: {text}' )
	raise TypeError( f'Unsupported date value: {type( value ).__name__}' )

class DB( ):
	"""SQLite data-access base class.

	Purpose:
		Provides the configured SQLite database path, approved table names, active table selection,
		query state, database connection creation, and parameterized retrieval operations used by the
		fiscal-year domain entities.

	Attributes:
		path (str): Configured SQLite database path.
		tables (List[str]): Configured database table names.
		name (str): Active approved database table name.
		data (pd.DataFrame | None): Most recent query result.
		query_name (str): Table name assigned by the current query operation.
		query_fy (str): Fiscal-year value assigned by the current query operation.
		query_bpoa (str): Beginning period of availability assigned by a fiscal-year query.
		query_epoa (str): Ending period of availability assigned by a fiscal-year query.
		table_name (str): Candidate table name validated before query execution.
		"""

	path: Optional[ str ]
	tables: Optional[ List[ str ] ]
	name: Optional[ str ]
	data: Optional[ pd.DataFrame ]
	
	def __init__( self ) -> None:
		"""Initialize database configuration.

		Purpose:
			Loads the SQLite database path and approved table names from ``config.py`` and initializes
			the query-state members used by database operations.

		Returns:
			None: Initialization does not return a value.

		Raises:
			AttributeError: Required configuration members are not defined.
			TypeError: The configured table collection cannot be converted to a list."""
		self.path = cfg.DB_PATH
		self.tables = cfg.TABLES
	
	
	def __dir__( self ) -> List[ str ]:
		"""Return public database members.

		Purpose:
			Return public database members.

		Returns:
			List[str]: Value produced by the operation."""
		return [ 'path', 'tables', 'name', 'data', 'create_connection',
			'query_fiscal_year', 'query_federal_holiday' ]
	
	def create_connection( self ) -> sqlite3.Connection:
		"""Create a SQLite database connection.

		Purpose:
			Opens the SQLite database configured by ``cfg.DB_PATH``.

		Returns:
			sqlite3.Connection: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return sqlite3.connect( self.path )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'DB'
			ex.method = 'create_connection( self ) -> sqlite3.Connection'
			raise ex
	
	def query_year( self, name: str, fy: str, bpoa: str, epoa: str ) -> pd.DataFrame:
		"""Query one fiscal-year row.

		Purpose:
			Retrieves the ``BudgetFiscalYears`` row matching the supplied fiscal year and period
			        of availability values.

		Args:
			name (str): Value used by the operation.
			fy (str): Value used by the operation.
			bpoa (str): Value used by the operation.
			epoa (str): Value used by the operation.

		Returns:
			pd.DataFrame: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'name', name )
			throw_if( 'fy', fy )
			throw_if( 'bpoa', bpoa )
			throw_if( 'epoa', epoa )
			self.name = name
			if self.name not in self.tables:
				raise ValueError( f'Unsupported table: {self.name}' )
			sql = (f'SELECT * FROM "{self.name}" '
			       'WHERE FiscalYear = ? AND BPOA = ? AND EPOA = ?;')
			parameters = (fy, bpoa, epoa)
			with self.create_connection( ) as connection:
				self.data = pd.read_sql_query( sql, connection, params=parameters )
			if len( self.data.index ) != 1:
				raise LookupError(
					f'Expected one {self.name} row; found {len( self.data.index )}.' )
			return self.data.copy( )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'DB'
			ex.method = 'query_fiscal_year( self, **kwargs ) -> pd.DataFrame'
			raise ex
	
	def query_holiday( self, name: str, fy: str ) -> pd.DataFrame:
		"""Query one federal-holiday row.

		Purpose:
			Retrieves the ``FederalHolidays`` row matching the supplied fiscal year.

		Args:
			name (str): Value used by the operation.
			fy (str): Value used by the operation.

		Returns:
			pd.DataFrame: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'name', name )
			throw_if( 'fy', fy )
			self.name = name
			if self.name not in self.tables:
				raise ValueError( f'Unsupported table: {self.name}' )
			sql = f'SELECT * FROM "{self.name}" WHERE FiscalYear = ?;'
			parameters = (fy,)
			with self.create_connection( ) as connection:
				self.data = pd.read_sql_query( sql, connection, params=parameters )
			if len( self.data.index ) != 1:
				raise LookupError( f'Expected one {self.name} row; found {len( self.data.index )}.' )
			return self.data.copy( )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'DB'
			ex.method = 'query_federal_holiday( self, name: str, fy: str ) -> pd.DataFrame'
			raise ex

class FiscalYear( DB ):
	"""Budget fiscal-year database entity.

	Purpose:
		Maps one ``BudgetFiscalYears`` database row to typed properties and provides calendar-year,
		fiscal-year, holiday, weekend, and workday calculations derived from that row and the current
		calculation date.

	Attributes:
		holidays (List[ Dict[ str str ] ]) - List of holidays for a iven fiscal year
		range_start (date | None): Normalized start date assigned by range-counting methods.
		range_end (date | None): Normalized end date assigned by range-counting methods.
		use_observed (bool): Indicates whether observed holiday dates are used.
		id (int): Read-only database row identifier.
		fiscal_year (str): Read-only fiscal-year identifier.
		bpoa (str): Read-only beginning period of availability.
		epoa (str): Read-only ending period of availability.
		start_date (date): Read-only fiscal-year start date.
		end_date (date | None): Read-only fiscal-year end date.
		expiration_date (date | None): Read-only appropriation expiration date.
		cancellation_date (date | None): Read-only appropriation cancellation date.
		weekdays (int): Read-only number of weekdays stored in the database row.
		weekends (int): Read-only number of weekend days stored in the database row.
		workdays (float): Read-only number of workdays stored in the database row.
		compensable_days (float): Read-only number of compensable days.
		compensable_workdays (float): Legacy read-only alias for ``compensable_days``.
		compensable_hours (float): Read-only number of compensable hours.
		type (str): Read-only appropriation type.
		availability (str): Read-only appropriation availability description.
		current_date (date): Read-only date used by calendar and fiscal calculations.
		calendar_year (int): Read-only calendar year containing ``current_date``.
		cy_start_date (date): Read-only first date of ``calendar_year``.
		cy_end_date (date): Read-only final date of ``calendar_year``.
		date (date): Read-only alias for ``current_date``.
		"""
	id: Optional[ int ]
	fiscal_year: Optional[ str ]
	bpoa: Optional[ str ]
	epoa: Optional[ str ]
	start_date: Optional[ date ]
	end_date: Optional[ date ]
	expiration_date: Optional[ date ]
	cancellation_date: Optional[ date ]
	weekdays: Optional[ int ]
	weekends: Optional[ int ]
	workdays: Optional[ float ]
	compensable_days: Optional[ float ]
	compensable_workdays: Optional[ int ]
	compensable_hours: Optional[ int ]
	type: Optional[ str ]
	availability: Optional[ str ]
	current_date:  Optional[ date ]
	calendar_year: Optional[ int ]
	cy_start_date:  Optional[ date ]
	cy_end_date:  Optional[ date ]
	range_start:  Optional[ date ]
	range_end:  Optional[ date ]
	use_observed: Optional[ bool ]
	
	def __init__( self, fy: str, bpoa: str = '', epoa: str = '' ) -> None:
		"""Initialize a budget fiscal-year entity.

		Purpose:
			Validates constructor input, assigns the query members, retrieves exactly one
			``BudgetFiscalYears`` row, converts each database field, and initializes calendar state.

		Args:
			fy (str): Fiscal year used to retrieve the database row.
			bpoa (str): Beginning period of availability. An empty value defaults to ``fy``.
			epoa (str): Ending period of availability. An empty value defaults to ``fy``.

		Returns:
			None: Initialization does not return a value.

		Raises:
			ValueError: ``fy`` is empty or a retrieved value cannot be converted.
			Error: Table validation or database retrieval fails.
			IndexError: The configured fiscal-year table is unavailable.
			KeyError: A required database column is missing.
			TypeError: A retrieved value has an unsupported type."""
		super( ).__init__( )
		self.fiscal_year = fy
		self.bpoa = bpoa if bpoa else fy
		self.epoa = epoa if epoa else fy
		self.name = self.tables[ 0 ]
		df = self.query_year( self.name, self.fiscal_year, self.bpoa, self.epoa, )
		row = df.iloc[ 0 ]
		self.id = int( row[ 'ID' ] )
		self.fiscal_year = str( row[ 'FiscalYear' ] )
		self.bpoa = str( row[ 'BPOA' ] )
		self.epoa = str( row[ 'EPOA' ] )
		self.start_date = to_date( row[ 'StartDate' ] )
		self.end_date = to_date( row[ 'EndDate' ] )
		self.expiration_date = to_date( row[ 'ExpirationDate' ] )
		self.cancellation_date = to_date( row[ 'CancellationDate' ] )
		self.weekdays = int( row[ 'Weekdays' ] )
		self.weekends = int( row[ 'Weekends' ] )
		self.workdays = float( row[ 'Workdays' ] )
		self.compensable_days = float( row[ 'CompensableDays' ] )
		self.compensable_hours = float( row[ 'CompensableHours' ] )
		self.type = str( row[ 'Type' ] )
		self.availability = str( row[ 'Availability' ] )
		self.current_date = datetime.today( ).date( )
		self.calendar_year = self.current_date.year
		self.cy_start_date = date( self.calendar_year, 1, 1 )
		self.cy_end_date = date( self.calendar_year, 12, 31 )
	
	
	def __repr__( self ) -> str:
		"""Return the fiscal-year identifier.

		Purpose:
			Return the fiscal-year identifier.

		Returns:
			str: Value produced by the operation."""
		return self.fiscal_year
	
	def __dir__( self ) -> List[ str ]:
		"""Return public fiscal-year members.

		Purpose:
			Return public fiscal-year members.

		Returns:
			List[str]: Value produced by the operation."""
		return [ 'id', 'fiscal_year', 'bpoa', 'epoa', 'start_date', 'end_date', 'expiration_date',
			'cancellation_date', 'weekdays', 'weekends', 'workdays', 'compensable_days',
			'compensable_workdays', 'compensable_hours', 'type', 'availability', 'current_date',
			'calendar_year', 'cy_start_date', 'cy_end_date', 'calendar_day_of_year',
			'calendar_days_elapsed', 'calendar_days_remaining',
			'calendar_elapsed_months', 'calendar_remaining_months', 'calendar_percent_elapsed',
			'fiscal_day_of_year', 'fiscal_month_number', 'fiscal_days_elapsed',
			'fiscal_days_remaining', 'fiscal_months_elapsed', 'calendar_days_in_year',
			'fiscal_months_remaining', 'fiscal_percent_elapsed', 'count_weekends',
			'count_holidays', 'count_workdays', 'calendar_bounds', 'fiscal_bounds', 'is_fiscal_start_year',
			'is_fiscal_end_year', 'is_calendar_start_year', 'is_calendar_end_date', 'to_dict' ]
	
	@property
	def holidays( self ) -> List[ Dict[ str, str ] ]:
		"""Return the FederalHolidays row as column-and-value mappings.
	
		Purpose:
			Queries the ``FederalHolidays`` table for the fiscal year represented by this instance
			and converts the matching row into a list of dictionaries. Each dictionary contains one
			holiday name and its corresponding value.
	
		Returns:
			List[Dict[str, str]]: Federal holiday column names and values for the current fiscal
			year.
				Each item contains ``ColumnName`` and ``ColumnValue`` keys.
	
		Raises:
			Error: The FederalHolidays row cannot be queried or converted.
		"""
		try:
			self.holiday_table_name = self.tables[ 1 ]
			self.holiday_data = self.query_holiday( name=self.holiday_table_name, fy=self.fiscal_year )
			self.holiday_row = self.holiday_data.iloc[ 0 ]
			self.holiday_columns = [ column for column in self.holiday_data.columns if
				column not in ('ID', 'FiscalYear') ]
			
			return [ { str( column ): ('' if pd.isna( self.holiday_row[ column ] ) else str(
				self.holiday_row[ column ] )) } for column in self.holiday_columns ]
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'holidays( self ) -> List[ Dict[ str, str ] ]'
			raise ex
	
	def calendar_day_of_year( self ) -> int:
		"""Return the one-based calendar day-of-year index.

		Purpose:
			Return the one-based calendar day-of-year index.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return (self.current_date - self.cy_start_date).days + 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_day_of_year( self ) -> int'
			raise ex
	
	def calendar_days_elapsed( self ) -> int:
		"""Return elapsed calendar-year days.

		Purpose:
			Return elapsed calendar-year days.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return max( 0, (self.current_date - self.cy_start_date).days )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_days_elapsed( self ) -> int'
			raise ex
	
	def calendar_days_remaining( self ) -> int:
		"""Return remaining calendar-year days.

		Purpose:
			Return remaining calendar-year days.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return max( 0, (self.cy_end_date - self.current_date).days )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_days_remaining( self ) -> int'
			raise ex
	
	def calendar_months_elapsed( self ) -> int:
		"""Return elapsed calendar-year months.

		Purpose:
			Return elapsed calendar-year months.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.current_date.month - 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_elapsed_months( self ) -> int'
			raise ex
	
	def calendar_months_remaining( self ) -> int:
		"""Return remaining calendar-year months.

		Purpose:
			Return remaining calendar-year months.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return 12 - self.current_date.month
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_remaining_months( self ) -> int'
			raise ex
	
	def calendar_percent_elapsed( self ) -> float:
		"""Return the elapsed calendar-year percentage.

		Purpose:
			Return the elapsed calendar-year percentage.

		Returns:
			float: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return (self.calendar_days_elapsed( ) / self.calendar_days_in_year( )) * 100.0
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_percent_elapsed( self ) -> float'
			raise ex
	
	def fiscal_day_of_year( self ) -> int:
		"""Return the one-based fiscal day-of-year index.

		Purpose:
			Return the one-based fiscal day-of-year index.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return (self.current_date - self.start_date).days + 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_day_of_year( self ) -> int'
			raise ex
	
	def fiscal_month_number( self ) -> int:
		"""Return the federal fiscal-month number.

		Purpose:
			Return the federal fiscal-month number.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return ((self.current_date.month - 10) % 12) + 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_month_number( self ) -> int'
			raise ex
	
	def fiscal_days_elapsed( self ) -> int:
		"""Return elapsed fiscal-year days.

		Purpose:
			Return elapsed fiscal-year days.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return max( 0, (self.current_date - self.start_date).days )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_days_elapsed( self ) -> int'
			raise ex
	
	def fiscal_days_remaining( self ) -> int:
		"""Return remaining fiscal-year days.

		Purpose:
			Return remaining fiscal-year days.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'end_date', self.end_date )
			return max( 0, (self.end_date - self.current_date).days )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_days_remaining( self ) -> int'
			raise ex
	
	def fiscal_months_elapsed( self ) -> int:
		"""Return elapsed fiscal-year months.

		Purpose:
			Return elapsed fiscal-year months.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.fiscal_month_number( ) - 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_months_elapsed( self ) -> int'
			raise ex
	
	def fiscal_months_remaining( self ) -> int:
		"""Return remaining fiscal-year months.

		Purpose:
			Return remaining fiscal-year months.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return 12 - self.fiscal_month_number( )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_months_remaining( self ) -> int'
			raise ex
	
	def fiscal_percent_elapsed( self ) -> float:
		"""Return the elapsed fiscal-year percentage.

		Purpose:
			Return the elapsed fiscal-year percentage.

		Returns:
			float: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return (self.fiscal_days_elapsed( ) / self.fiscal_days_in_year( )) * 100.0
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_percent_elapsed( self ) -> float'
			raise ex
	
	def count_weekends( self, start: date | datetime, end: date | datetime ) -> int:
		"""Count weekend days in an inclusive range.

		Purpose:
			Count weekend days in an inclusive range.

		Args:
			start (date | datetime): Value used by the operation.
			end (date | datetime): Value used by the operation.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'start', start )
			throw_if( 'end', end )
			self.range_start = to_date( start )
			self.range_end = to_date( end )
			if self.range_start > self.range_end:
				return 0
			count = 0
			current = self.range_start
			while current <= self.range_end:
				if current.weekday( ) >= 5:
					count += 1
				current += timedelta( days=1 )
			return count
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = ('count_weekends( self, start: date | datetime, end: date | datetime ) -> '
			             'int')
			raise ex
	
	def calendar_days_in_year( self ) -> int:
		try:
			return ( self.cy_end_date - self.cy_start_date ).days + 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_days_in_year( self ) -> int'
			raise ex
	
	def fiscal_days_in_year( self ) -> int:
		try:
			return ( self.end_date - self.start_date ).days + 1
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_days_in_year( self ) -> int'
			raise ex
	
	def count_holidays( self, start: date | datetime, end: date | datetime,
		use_observed: bool=True ) -> int:
		"""Count federal holidays in an inclusive range.

		Purpose:
			Count federal holidays in an inclusive range.

		Args:
			start (date | datetime): Value used by the operation.
			end (date | datetime): Value used by the operation.
			use_observed (bool): Value used by the operation.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'start', start )
			throw_if( 'end', end )
			self.range_start = to_date( start )
			self.range_end = to_date( end )
			self.use_observed = use_observed
			if self.range_start > self.range_end:
				return 0
			federal_holiday = FederalHoliday( self.fiscal_year )
			key = 'observed' if self.use_observed else 'actual'
			return sum( 1 for payload in federal_holiday.holidays( ).values( ) if
			self.range_start <= payload[ key ] <= self.range_end )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'count_holidays( self, **kwargs ) -> int'
			raise ex
	
	def count_workdays( self, start: date | datetime, end: date | datetime,
		use_observed: bool=True ) -> int:
		"""Count workdays in an inclusive range.

		Purpose:
			Count workdays in an inclusive range.

		Args:
			start (date | datetime): Value used by the operation.
			end (date | datetime): Value used by the operation.
			use_observed (bool): Value used by the operation.

		Returns:
			int: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'start', start )
			throw_if( 'end', end )
			self.range_start = to_date( start )
			self.range_end = to_date( end )
			self.use_observed = use_observed
			if self.range_start > self.range_end:
				return 0
			federal_holiday = FederalHoliday( self.fiscal_year )
			key = 'observed' if self.use_observed else 'actual'
			holiday_dates = { payload[ key ] for payload in federal_holiday.holidays( ).values( ) }
			count = 0
			current = self.range_start
			while current <= self.range_end:
				if current.weekday( ) < 5 and current not in holiday_dates:
					count += 1
				current += timedelta( days=1 )
			return count
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'count_workdays( self, **kwargs ) -> int'
			raise ex
	
	def calendar_bounds( self ) -> Tuple[ date, date ]:
		"""Return calendar-year boundaries.

		Purpose:
			Return calendar-year boundaries.

		Returns:
			Tuple[date, date]: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.cy_start_date, self.cy_end_date
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'calendar_bounds( self ) -> Tuple[ date, date ]'
			raise ex
	
	def fiscal_bounds( self ) -> Tuple[ date, date ]:
		"""Return fiscal-year boundaries.

		Purpose:
			Return fiscal-year boundaries.

		Returns:
			Tuple[date, date]: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'end_date', self.end_date )
			return self.start_date, self.end_date
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'fiscal_bounds( self ) -> Tuple[ date, date ]'
			raise ex
	
	def is_fiscal_start_year( self ) -> bool:
		"""Determine whether the current date starts the fiscal year.

		Purpose:
			Determine whether the current date starts the fiscal year.

		Returns:
			bool: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.current_date.year == self.start_date.year
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'is_fiscal_start_year( self ) -> bool'
			raise ex
	
	def is_fiscal_end_year( self ) -> bool:
		"""Determine whether the current date ends the fiscal year.

		Purpose:
			Determine whether the current date ends the fiscal year.

		Returns:
			bool: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.current_date.year == self.end_date.year
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'is_fiscal_end_year( self ) -> bool'
			raise ex
	
	def is_calendar_start_year( self ) -> bool:
		"""Determine whether the current date starts the calendar year.

		Purpose:
			Determine whether the current date starts the calendar year.

		Returns:
			bool: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.current_date.year == self.cy_start_date.year
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'is_calendar_start_year( self ) -> bool'
			raise ex
	
	def is_calendar_end_date( self ) -> bool:
		"""Determine whether the current date ends the calendar year.

		Purpose:
			Determine whether the current date ends the calendar year.

		Returns:
			bool: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return self.current_date == self.cy_end_date
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'is_calendar_end_date( self ) -> bool'
			raise ex
	
	def to_dict( self ) -> Dict[ str, object ]:
		"""Return the mapped fiscal-year row as a dictionary.

		Purpose:
			Return the mapped fiscal-year row as a dictionary.

		Returns:
			Dict[str, object]: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return \
			{
				'FiscalYear': self.fiscal_year, 'BPOA': self.bpoa,
				'EPOA': self.epoa, 'StartDate': self.start_date, 'EndDate': self.end_date,
				'ExpirationDate': self.expiration_date, 'CancellationDate': self.cancellation_date,
				'Weekdays': self.weekdays, 'Weekends': self.weekends, 'Workdays': self.workdays,
				'CompensableDays': self.compensable_days, 'CompensableHours': self.compensable_hours,
				'Type': self.type, 'Availability': self.availability,
			}
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FiscalYear'
			ex.method = 'to_dict( self ) -> Dict[ str, object ]'
			raise ex

class FederalHoliday( DB ):
	"""Federal-holiday database entity.

	Purpose:
		Maps one ``FederalHolidays`` database row to typed properties and provides actual-date,
		observed-date, holiday-membership, weekend, and dictionary-export operations.

	Attributes:
		input_fiscal_year (str): Fiscal year supplied to the constructor.
		actual_date (date): Holiday date assigned by ``observed_date``.
		when (date | None): Normalized date assigned by holiday and weekend tests.
		use_observed (bool): Indicates whether holiday tests use observed dates.
		id (int): Read-only database row identifier.
		fiscal_year (str): Read-only fiscal-year identifier.
		columbus_day (date): Read-only Columbus Day date.
		veterans_day (date): Read-only Veterans Day date.
		thanksgiving_day (date): Read-only Thanksgiving Day date.
		christmas_day (date): Read-only Christmas Day date.
		new_years_day (date): Read-only New Year's Day date.
		martin_luther_king_day (date): Read-only Martin Luther King Jr. Day date.
		presidents_day (date): Read-only Presidents Day date.
		memorial_day (date): Read-only Memorial Day date.
		juneteenth_day (date): Read-only Juneteenth National Independence Day date.
		independence_day (date): Read-only Independence Day date.
		labor_day (date): Read-only Labor Day date.
		"""

	id: int
	fiscal_year: str
	columbus_day: date
	veterans_day: date
	thanksgiving_day: date
	christmas_day: date
	new_years_day: date
	martin_luther_king_day: date
	presidents_day: date
	memorial_day: date
	juneteenth_day: date
	independence_day: date
	labor_day: date
	input_fiscal_year: str
	actual_date: date
	when: date
	use_observed: bool
	
	def __init__( self, fiscal_year: str ) -> None:
		"""Initialize a federal-holiday entity.

		Purpose:
			Validates the fiscal year, assigns query state, retrieves exactly one ``FederalHolidays`` row,
			and maps each database column to its typed storage member.

		Args:
			fiscal_year (str): Fiscal year whose federal-holiday row is loaded.

		Returns:
			None: Initialization does not return a value.

		Raises:
			ValueError: ``fiscal_year`` is empty or a retrieved value cannot be converted.
			Error: Table validation or database retrieval fails.
			IndexError: The configured federal-holiday table is unavailable.
			KeyError: A required database column is missing.
			TypeError: A retrieved value has an unsupported type."""
		super( ).__init__( )
		throw_if( 'fiscal_year', fiscal_year )
		self.input_fiscal_year = fiscal_year
		self.name = self.tables[ 1 ]
		df = self.query_holiday( self.name, self.input_fiscal_year )
		row = df.iloc[ 0 ]
		self.id = int( row[ 'ID' ] )
		self.fiscal_year = str( row[ 'FiscalYear' ] )
		self.columbus_day = to_date( row[ 'ColumbusDay' ] )
		self.veterans_day = to_date( row[ 'VeteransDay' ] )
		self.thanksgiving_day = to_date( row[ 'ThanksgivingDay' ] )
		self.christmas_day = to_date( row[ 'ChristmasDay' ] )
		self.new_years_day = to_date( row[ 'NewYearsDay' ] )
		self.martin_luther_king_day = to_date( row[ 'MartinLutherKingDay' ] )
		self.presidents_day = to_date( row[ 'PresidentsDay' ] )
		self.memorial_day = to_date( row[ 'MemorialDay' ] )
		self.juneteenth_day = to_date( row[ 'JuneteenthDay' ] )
		self.independence_day = to_date( row[ 'IndependenceDay' ] )
		self.labor_day = to_date( row[ 'LaborDay' ] )
	
	
	def __repr__( self ) -> str:
		"""Return the fiscal-year identifier.

		Purpose:
			Return the fiscal-year identifier.

		Returns:
			str: Value produced by the operation."""
		return self.fiscal_year
	
	def __dir__( self ) -> List[ str ]:
		"""Return public federal-holiday members.

		Purpose:
			Return public federal-holiday members.

		Returns:
			List[str]: Value produced by the operation."""
		return [ 'id', 'fiscal_year', 'columbus_day', 'veterans_day', 'thanksgiving_day',
			'christmas_day', 'new_years_day', 'martin_luther_king_day', 'presidents_day',
			'memorial_day', 'juneteenth_day', 'independence_day', 'labor_day', 'observed_date',
			'holidays', 'is_holiday', 'is_weekend', 'to_dict' ]
	
	def observed_date( self, value: date ) -> date:
		"""Return the observed date for a holiday.

		Purpose:
			Return the observed date for a holiday.

		Args:
			value (date): Value used by the operation.

		Returns:
			date: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'value', value )
			self.actual_date = value
			if self.actual_date.weekday( ) == 5:
				return self.actual_date - timedelta( days=1 )
			if self.actual_date.weekday( ) == 6:
				return self.actual_date + timedelta( days=1 )
			return self.actual_date
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FederalHoliday'
			ex.method = 'observed_date( self, value: date ) -> date'
			raise ex
	
	def holidays( self ) -> Dict[ str, Dict[ str, date ] ]:
		"""Return actual and observed federal-holiday dates.

		Purpose:
			Return actual and observed federal-holiday dates.

		Returns:
			Dict[str, Dict[str, date]]: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			actual_dates = { 'Columbus Day': self.columbus_day, 'Veterans Day': self.veterans_day,
				'Thanksgiving Day': self.thanksgiving_day, 'Christmas Day': self.christmas_day,
				"New Year's Day": self.new_years_day,
				'Birthday of Martin Luther King, Jr.': self.martin_luther_king_day,
				"Washington's Birthday": self.presidents_day, 'Memorial Day': self.memorial_day,
				'Juneteenth National Independence Day': self.juneteenth_day,
				'Independence Day': self.independence_day, 'Labor Day': self.labor_day, }
			return { name: { 'actual': actual, 'observed': self.observed_date( actual ) } for
				name, actual in actual_dates.items( ) }
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FederalHoliday'
			ex.method = 'holidays( self ) -> Dict[ str, Dict[ str, date ] ]'
			raise ex
	
	def is_holiday( self, when: date | datetime, observed: bool = True ) -> bool:
		"""Determine whether a date is a federal holiday.

		Purpose:
			Determine whether a date is a federal holiday.

		Args:
			when (date | datetime): Value used by the operation.
			observed (bool): Value used by the operation.

		Returns:
			bool: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'when', when )
			self.when = to_date( when )
			self.use_observed = observed
			key = 'observed' if self.use_observed else 'actual'
			return any( self.when == payload[ key ] for payload in self.holidays( ).values( ) )
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FederalHoliday'
			ex.method = 'is_holiday( self, when: date | datetime, observed: bool = True ) -> bool'
			raise ex
	
	def is_weekend( self, when: date | datetime ) -> bool:
		"""Determine whether a date falls on a weekend.

		Purpose:
			Determine whether a date falls on a weekend.

		Args:
			when (date | datetime): Value used by the operation.

		Returns:
			bool: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			throw_if( 'when', when )
			self.when = to_date( when )
			return self.when.weekday( ) >= 5
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FederalHoliday'
			ex.method = 'is_weekend( self, when: date | datetime ) -> bool'
			raise ex
	
	def to_dict( self ) -> Dict[ str, object ]:
		"""Return the mapped federal-holiday row as a dictionary.

		Purpose:
			Return the mapped federal-holiday row as a dictionary.

		Returns:
			Dict[str, object]: Value produced by the operation.

		Raises:
			Error: The operation fails and the underlying exception is wrapped."""
		try:
			return { 'ID': self.id, 'FiscalYear': self.fiscal_year,
				'ColumbusDay': self.columbus_day, 'VeteransDay': self.veterans_day,
				'ThanksgivingDay': self.thanksgiving_day, 'ChristmasDay': self.christmas_day,
				'NewYearsDay': self.new_years_day,
				'MartinLutherKingDay': self.martin_luther_king_day,
				'PresidentsDay': self.presidents_day, 'MemorialDay': self.memorial_day,
				'JuneteenthDay': self.juneteenth_day, 'IndependenceDay': self.independence_day,
				'LaborDay': self.labor_day, }
		except Exception as e:
			ex = Error( e )
			ex.module = 'fiscal'
			ex.cause = 'FederalHoliday'
			ex.method = 'to_dict( self ) -> Dict[ str, object ]'
			raise ex
