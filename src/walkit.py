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

    def get_records(self) -> List[Tuple]:
        """Returns all records from database"""
        # TODO: Print beautiful table, not list of tuples
        query = "select * from walks order by walks.date"
        items = self._database.select(sql=query)
        return items

    def delete_record(self, date: str) -> None:
        """Delete record by given date"""
        query = f"delete from walks where date = '{date}'"
        self._database.delete(sql=query)

    def total_metres(self) -> int:
        """Returns total metres traveled"""
        items = self.get_records()
        return sum(metres for _, metres in items)
