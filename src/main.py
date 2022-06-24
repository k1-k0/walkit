from pprint import pprint
from utils import get_database_path, parse_args, parse_add_values

from database import Database
from walkit import Walkit


def main():
    database_path = get_database_path()
    database = Database(path=database_path)
    walkit = Walkit(database=database)
    args = parse_args()

    if args.total:
        walkit.print_total_metres()
    elif args.add:
        metres, date = parse_add_values(*args.add)
        walkit.add_record(metres, date) if date else walkit.add_record(metres)
    elif args.print:
        # TODO: Also must traveled metres for specified date
        walkit.print_all_records()
    elif args.delete:
        # TODO: Delete_record should pass datetime, not string
        date = args.delete
        walkit.delete_record(date)


if __name__ == '__main__':
    main()
