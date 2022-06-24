import os
import argparse
import datetime as dt
from typing import Optional, Tuple


DEFAULT_DB = ""     # TODO: Figure with default path of DB
DB_ENVNAME = "WALKIT_DB"

def get_database_path() -> str:
    """Read DB file path from env, if not exists use default"""
    return os.getenv(key=DB_ENVNAME, default=DEFAULT_DB)

def parse_args() -> argparse.Namespace:
    """Parse arguments of command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--total', '-t', action='store_true',
                        help='Returns the total number of meters traveled')
    parser.add_argument('--add', '-a', action='store', nargs='*',
                        help='Add new record to database')
    parser.add_argument('--print', '-p', action='store_true',
                        help='Returns all records in database')
    parser.add_argument('--delete', '-d', action='store',
                        help='Delete record by specified date')
    return parser.parse_args()

def parse_add_values(metres: str,
                     date: Optional[str] = None) -> Tuple[ int, Optional[dt.datetime]]:
    """Transform walks data(metres and date) from string to correct types"""
    parsed_metres = int(metres)
    parsed_date = date_from_str(date) if date else None  
    return (parsed_metres, parsed_date)

def date_from_str(datestr: str) -> dt.datetime:
    """Build datetime object from string with date"""
    return dt.datetime.fromisoformat(datestr)

