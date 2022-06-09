import datetime as dt
import argparse
from pprint import pprint
from typing import Optional, Tuple
from utils import get_database_path, date_from_str

from database import Database
from walkit import Walkit


def main():
    database_path = get_database_path()
    database = Database(path=database_path)
    walkit = Walkit(database=database)

    parser = argparse.ArgumentParser()
    parser.add_argument('--total', '-t', action='store_true',
                        help='Returns the total number of meters traveled')
    parser.add_argument('--add', '-a', action='store', nargs='*',
                        help='Add new record to database')
    parser.add_argument('--print', '-p', action='store_true',
                        help='Returns all records in database')
    parser.add_argument('--delete', '-d', action='store',
                        help='Delete record by specified date')
    args = parser.parse_args()

    # TODO: All arguments handlers to separate functions
    if args.total:
        print(walkit.total_metres())
    elif args.add:
        metres, date = parse_add_values(*args.add)
        if date:
            walkit.add_record(metres, date)
        else:
            walkit.add_record(metres)
        print("Record has been written!")
    elif args.print:
        # TODO: Also must traveled metres for specified date
        records = walkit.get_records()
        if records:
            pprint(records)
        else:
            print('There are no records in database.')
    elif args.delete:
        # TODO: Delete_record should pass datetime, not string
        date = args.delete
        walkit.delete_record(date)
        print('Record has been removed!')


# TODO: Move to utils and add docstring
def parse_add_values(metres: str,
                     date: Optional[str] = None) -> Tuple[
                         int, Optional[dt.datetime]]:
    parsed_metres = int(metres)
    if date:
        parsed_date = date_from_str(date)
        return (parsed_metres, parsed_date)
    return (parsed_metres, None)


if __name__ == '__main__':
    main()
