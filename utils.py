import os
import datetime as dt


DEFAULT_DB = ""
DB_ENVNAME = "WALKIT_DB"

def get_database_path() -> str:
    return os.getenv(key=DB_ENVNAME, default=DEFAULT_DB)


def date_from_str(datestr: str) -> dt.datetime:
    return dt.datetime.fromisoformat(datestr)