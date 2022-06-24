from typing import Optional, Tuple, List
from contextlib import contextmanager
import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path
        self.connection = sqlite3.Connection(self.path)
        self.check_tables()

    def check_tables(self):
        # TODO: Move table name to env name
        check_query = \
                "SELECT name FROM sqlite_master WHERE type='table' and name='walks';"
        result = self.connection.execute(check_query).fetchone()
        if not result:
            self._prepare_table()
            print(f"Table 'walks' has been successfully created!")

    def close(self) -> None:
        self.connection.commit()
        self.connection.close()

    def insert(self, sql: str, values: Optional[Tuple] = None) -> None:
        with self._get_cursor() as cur:
            cur.execute(sql) if not values else cur.execute(sql, values)
        self.connection.commit()

    def select(self, sql: str, values: Optional[Tuple] = None) -> List:
        with self._get_cursor() as cur:
            cur.execute(sql)
            items = cur.fetchall() 
        return items

    def select_one(self, sql: str, values: Tuple) -> Tuple:
        with self._get_cursor() as cur:
            cur.execute(sql, values)
            items = cur.fetchone()
        return items

    def update(self, sql: str, values: Tuple) -> None:
        with self._get_cursor() as cur:
            cur.execute(sql, values)
        self.connection.commit()

    def delete(self, sql: str) -> None:
        with self._get_cursor() as cur:
            cur.execute(sql)
        self.connection.commit()

    @contextmanager
    def _get_cursor(self):
        cur = self.connection.cursor()
        yield cur
        cur.close()

    def _prepare_table(self) -> None:
        with self._get_cursor() as cur:
            cur.execute("create table if not exists walks (date TIMESTAMP, metres INTEGER)")
        self.connection.commit()
