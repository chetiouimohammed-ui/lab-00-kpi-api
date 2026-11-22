import pyodbc

from config import settings


def get_connection() -> pyodbc.Connection:
    return pyodbc.connect(settings.connection_string, timeout=5)
