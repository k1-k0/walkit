from typing import Optional, Tuple, List
import datetime as dt

from database import Database


# TODO: add logger
class Walkit:
    """Class for working with walk records"""
    def __init__(self, database: Database):
        self._database = database

    def add_record(self, metres: int = 0, 
                   date: Optional[dt.datetime] = None) -> None:
        """Add record to database"""
        if not date:
            date = dt.datetime.now()

        # TODO: Options if date already exists in table: Rewrite, Append, Nothing
        query = "insert into walks values (?, ?)"
        self._database.insert(sql=query, values=(date.date(), metres))
        print(f'Record ({metres}m, {date.date()}) has been written!')

    def get_records(self) -> List[Tuple]:
        """Returns all records from database"""
        query = "select * from walks order by walks.date"
        items = self._database.select(sql=query)
        return items

    def delete_record(self, date: str) -> None:
        """Delete record by given date"""
        query = f"delete from walks where date = '{date}'"
        self._database.delete(sql=query)
        print(f'Record ({date}) has been removed!')

    def print_all_records(self) -> None:
        """Print table of all records contained in database"""
        records = self.get_records()
        if not records:
            print('There are no records in database.')

        col_sep, row_sep = '|', '-'
        col1_width, col2_width = 14, 20
        # TODO: Move to utils? Is it needed in the future?
        def formatted_print(first: str, second: str):
            print(f'{first:^{col1_width}}{col_sep}{second:^{col2_width}}{col_sep}')

        formatted_print("Date", "Distance")
        formatted_print(row_sep*col1_width, row_sep*col2_width)
        for date, metres in records:
            distance_info = f'{metres}m ({metres/1000}km)'
            formatted_print(date, distance_info)

    def print_total_metres(self) -> None:
        """Print total metres traveled"""
        items = self.get_records()
        total_metres = sum(metres for _, metres in items)
        print(f'Total meters traveled: {total_metres}m ({total_metres/1000}km)')
