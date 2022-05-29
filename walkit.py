from contextlib import contextmanager
import sqlite3
from typing import Optional, Tuple, List
import datetime as dt

from utils import get_database_path


# TODO: add logger
class Database:
    def __init__(self):
        self.path = get_database_path() 
        self.connection = sqlite3.Connection(self.path)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def insert(self, sql: str, values: Optional[Tuple] = None):
        with self._get_cursor() as cur:
            cur.execute(sql) if not values else cur.execute(sql, values)
        self.connection.commit()

    def select(self, sql: str, values: Optional[Tuple] = None) -> List:
        with self._get_cursor() as cur:
            cur.execute(sql) if not values else cur.execute(sql, values)
            items = cur.fetchall()
        return items

    def delete(self, sql: str) -> None:
        with self._get_cursor() as cur:
            cur.execute(sql)
        self.connection.commit()

    @contextmanager
    def _get_cursor(self):
        cur = self.connection.cursor()
        yield cur
        cur.close()

    def _prepare_table(self):
        # TODO add check for table existence 
        with self._get_cursor() as cur:
            cur.execute("create table walks (date TIMESTAMP, metres INTEGER)")
        self.connection.commit()


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
