import sqlite3
from typing import Optional, Tuple, List
import datetime as dt

from utils import get_database_path


class Database:
    def __init__(self):
        self.path = get_database_path() 
        self.connection = sqlite3.Connection(self.path)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def _prepare_table(self):
        # TODO add check for table existence 
        cur = self.connection.cursor()
        cur.execute("create table walks (date TIMESTAMP, metres INTEGER)")

        cur.close()
        self.connection.commit()

    def insert(self, sql: str, values: Optional[Tuple] = None):
        cur = self.connection.cursor()

        cur.execute(sql) if not values else cur.execute(sql, values)
        
        cur.close()
        self.connection.commit()

    def select(self, sql: str, values: Optional[Tuple] = None) -> List:
        cur = self.connection.cursor()

        cur.execute(sql) if not values else cur.execute(sql, values)

        items = cur.fetchall()
        cur.close()

        return items

    def delete(self, sql: str) -> None:
        cur = self.connection.cursor()
        
        cur.execute(sql)
        
        cur.close()
        self.connection.commit()


    # TODO: this and below method get out to separate class,
    # which will work with business logic (add/remove/list records)

    def add_record(self, metres: int = 0, 
                   date: Optional[dt.datetime] = None) -> None:
        cur = self.connection.cursor()

        if not date:
            date = dt.datetime.now().date()

        # TODO: Options if date already exists in table: Rewrite, Append, Nothing
        query = "insert into walks values (?, ?)"
        self.insert(sql=query, values=(date, metres))

    def get_records(self) -> None:
        query = "select * from walks"
        items = self.select(sql=query)
        return items
    
    def delete_record(self, date: str) -> None:
        query = f"delete from walks where date = '{date}'"
        self.delete(sql=query)