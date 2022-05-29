from typing import Optional, Tuple, List
import datetime as dt

from database import Database


# TODO: add logger
class Walkit:
    def __init__(self, database: Database):
        self._database = database

    def add_record(self, metres: int = 0, 
                   date: Optional[dt.datetime] = None) -> None:
        if not date:
            date = dt.datetime.now().date()

        # TODO: Options if date already exists in table: Rewrite, Append, Nothing
        query = "insert into walks values (?, ?)"
        self._database.insert(sql=query, values=(date, metres))

    def get_records(self) -> List[Tuple]:
        query = "select * from walks"
        items = self._database.select(sql=query)
        return items
    
    def delete_record(self, date: str) -> None:
        query = f"delete from walks where date = '{date}'"
        self._database.delete(sql=query)
    
    def total_metres(self) -> int:
        items = self.get_records()
        return sum(metres for _, metres in items)
