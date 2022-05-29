from typing import Optional, Tuple, List
from contextlib import contextmanager
import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path
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
