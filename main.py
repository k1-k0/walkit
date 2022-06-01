
import argparse
from ctypes import Union
from typing import Optional, Tuple
from utils import get_database_path

from database import Database
from walkit import Walkit
# TODO: Argparse
# TODO: get env 


def main():
    database_path = get_database_path()
    database = Database(path=database_path)
    walkit = Walkit(database=database)

    parser = argparse.ArgumentParser()
    parser.add_argument('--total', '-t', action='store_true',
                        help='Returns the total number of meters traveled')
    parser.add_argument('--add', '-a', action='store', nargs='*',
                        help='Returns the total number of meters traveled')
    args = parser.parse_args()

    if args.total:
        print(walkit.total_metres())
    elif args.add:
        values = parse_add_values(*args.add)
        walkit.add_record(values)
        print("Record has been written!")


def parse_add_values(metres: str, date: Optional[str]) -> Union[str, Tuple[str, str]]:
    pass


if __name__ == '__main__':
    main()
