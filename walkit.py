import sqlite3
from typing import Optional
import datetime as dt

from utils import get_database_path


class Database:
    def __init__(self):
        self.path = get_database_path() 
        self.connection = sqlite3.Connection(self.path)

    def close(self):
        self.connection.commit()
        self.connection.close()

    def prepare_table(self):
        cur = self.connection.cursor()
        cur.execute("create table walks (date TIMESTAMP, metres INTEGER)")
        cur.close()
        self.connection.commit()

    def add_record(self, metres: int = 0, date: Optional[dt.datetime] = None):
        cur = self.connection.cursor()

        if not date:
            date = dt.datetime.now()

        cur.execute("insert into walks values (?, ?)", (date, metres))
        cur.close()
        self.connection.commit()

    def get_records(self):
        cur = self.connection.cursor()
        cur.execute("select * from walks")
        print(cur.fetchall())