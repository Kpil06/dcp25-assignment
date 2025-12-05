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

def tunes_by_key() -> pd.DataFrame:
    """
    Returns a dataframe showing how many tunes are in each key.
    """
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT tune_key, COUNT(*) AS tune_count
        FROM tunes
        GROUP BY tune_key
        ORDER BY tune_count DESC;
        """,
        conn,
    )

    conn.close()
    return df