'''
  ******************************************************************************************
      Assembly:                fiscal
      Filename:                config.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file="config.py" company="Terry D. Eppler">

	     config.py
	     Copyright ©  2020  Terry Eppler

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
    config.py
  </summary>
  ******************************************************************************************
'''
import os
import re
from typing import Optional, List, Dict
from pathlib import Path

# -------------- APP-LEVEL UTILITIES -------------

def throw_if( name: str, value: object ) -> None:
	"""Raise ``ValueError`` when a required value is empty.

	Purpose:
		Provide a small, consistent guard for required arguments and configuration values. The
		function treats falsy values as invalid and raises a ``ValueError`` containing the
		caller-supplied argument or setting name.

	Args:
		name (str): Name of the argument or configuration value being validated.
		value (object): Value to validate.

	Returns:
		None.

	Raises:
		ValueError: Raised when ``value`` is falsy.
	"""
	if not value:
		raise ValueError( f'Argument "{name}" cannot be empty!' )

def get_bool( name: str, default: bool = False ) -> bool:
	"""Read a Boolean environment variable using Fiddy's true-value convention.

	Purpose:
		Convert environment-variable text into a deterministic Boolean value. Missing variables
		return the caller-provided default. Values of ``1``, ``true``, ``yes``, ``y``, and
		``on`` are treated as ``True``; all other defined values are treated as ``False``.

	Args:
		name (str): Environment variable name.
		default (bool): Default value used when the environment variable is not defined.

	Returns:
		bool: Parsed Boolean value. If parsing fails, the original ``default`` value is returned.
	"""
	try:
		throw_if( 'name', name )
		value = os.getenv( name )
		return default if value is None else value.strip( ).lower( ) in (
				'1',
				'true',
				'yes',
				'y',
				'on'
		)
	except Exception:
		return default

def get_int( name: str, default: int ) -> int:
	"""Read an integer environment variable with a deterministic fallback.

	Purpose:
		Parse an optional environment variable as an integer while preserving a safe default when
		the variable is missing, empty, or invalid.

	Args:
		name (str): Environment variable name.
		default (int): Default integer value used when parsing is not possible.

	Returns:
		int: Parsed integer value or the supplied default value.
	"""
	try:
		throw_if( 'name', name )
		value = os.getenv( name )
		return default if value in (None, '') else int( str( value ).strip( ) )
	except Exception:
		return default

def get_float( name: str, default: float ) -> float:
	"""Read a floating-point environment variable with a deterministic fallback.

	Purpose:
		Parse an optional environment variable as a float while preserving a safe default when the
		variable is missing, empty, or invalid.

	Args:
		name (str): Environment variable name.
		default (float): Default floating-point value used when parsing is not possible.

	Returns:
		float: Parsed floating-point value or the supplied default value.
	"""
	try:
		throw_if( 'name', name )
		value = os.getenv( name )
		return default if value in (None, '') else float( str( value ).strip( ) )
	except Exception:
		return default

def get_path( name: str, default: Path ) -> Path:
	"""Read a path environment variable and return a resolved ``Path``.

	Purpose:
		Resolve optional filesystem configuration from the environment. Missing variables return
		the resolved default path. Invalid values return the resolved default path rather than
		interrupting module import.

	Args:
		name (str): Environment variable name.
		default (Path): Default path used when the environment variable is not defined.

	Returns:
		Path: Resolved path value or resolved default path.
	"""
	try:
		throw_if( 'name', name )
		throw_if( 'default', default )
		value = os.getenv( name )
		return Path( value ).resolve( ) if value else default.resolve( )
	except Exception:
		return default.resolve( )

def get_text( name: str, default: str ) -> str:
	"""Read a text environment variable with a deterministic fallback.

	Purpose:
		Return an environment variable as text while preserving the supplied default when the
		variable is missing or empty.

	Args:
		name (str): Environment variable name.
		default (str): Default text value.

	Returns:
		str: Environment value or supplied default.
	"""
	try:
		throw_if( 'name', name )
		value = os.getenv( name )
		return default if value in (None, '') else str( value )
	except Exception:
		return default
	
# ----------------- CONSTANTS -------------------

TABLES = [ 'BudgetFiscalYears', 'FederalHolidays' ]
ROOT_DIR = Path( __file__ ).resolve( ).parent
DB_DIR: Path = get_path( 'DB_DIR', ROOT_DIR / 'sqlite' )
DB_PATH: str = get_text( 'DB_PATH', str( DB_DIR / 'data.db' ) )