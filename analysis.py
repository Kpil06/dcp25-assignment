"""
This file only reads from tunes.db and prints a summary for the report.
"""

import sqlite3
import pandas as pd

DB_NAME = "tunes.db"

def get_connection() -> sqlite3.Connection:
    """
    Helper function that opens a connection to the SQLite database'
    """
    return sqlite3.connect(DB_NAME)

