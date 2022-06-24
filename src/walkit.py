from typing import Optional, Tuple, List
import datetime as dt

from database import Database


# TODO: add logger
class Walkit:
    """Class for working with walk records"""
    def __init__(self, database: Database):
        self._database = database

    def add_or_update_record(self, metres: int = 0, 
                             date: Optional[dt.datetime] = None) -> None:
        """Add record to database or update if it already exists"""
        if not date:
            date = dt.datetime.now()

        record = self.get_record(str(date.date()))
        if record:
            db_date, db_metres = record[0], record[1]
            self.update_record(db_date, metres)
            print(f'Record ({db_metres}m, {db_date}) has been updated '\
                  f'with new value {metres}m.')
            return 

        query = "insert into walks values (?, ?)"
        self._database.insert(sql=query, values=(date.date(), metres))
        print(f'Record ({metres}m, {date.date()}) has been written.')

    def update_record(self, date: str, metres: int) -> None:
        """Update record from database with specified date by given metres"""
        query = f"update walks set metres = ? where date = ?"
        record = self._database.update(sql=query, values=(metres,date))
        return record

    def get_records(self) -> List[Tuple]:
        """Returns all records from database"""
        query = "select * from walks order by walks.date"
        records = self._database.select(sql=query)
        return records

    def get_record(self, date: str) -> Tuple[str, int]:
        """Return record from database with specified date"""
        query = f"select * from walks where date = ?"
        record = self._database.select_one(sql=query, values=(date,))
        return record

    def delete_record(self, date: str) -> None:
        """Delete record by given date"""
        query = f"delete from walks where date = '{date}'"
        self._database.delete(sql=query)
        print(f'Record ({date}) has been removed.')

    def print_all_records(self) -> None:
        """Print table of all records contained in database"""
        records = self.get_records()
        if not records:
            print('There are no records in database.')

        col_sep, row_sep = '|', '-'
        col1_width, col2_width = 14, 24
        # TODO: Move to utils? Is it needed in the future?
        def formatted_print(first: str, second: str):
            print(f'{first:^{col1_width}}{col_sep}{second:^{col2_width}}{col_sep}')

        formatted_print("Date", "Distance(m)")
        formatted_print(row_sep*col1_width, row_sep*col2_width)
        for date, metres in records:
            metres_info, km_info = f'{metres}m', f'{metres/1000}km'
            distance_info = f'{metres_info:>10} == {km_info:<10}'
            formatted_print(date, distance_info)

    def print_total_metres(self) -> None:
        """Print total metres traveled"""
        items = self.get_records()
        total_metres = sum(metres for _, metres in items)
        print(f'Total meters traveled: {total_metres}m ({total_metres/1000}km)')
