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

def tunes_by_type() -> pd.DataFrame:
    """
    Returns a df showing how many tunes belong to each type.
    """
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT tune_type, COUNT(*) AS tune_count
        FROM tunes
        GROUP BY tune_type
        ORDER BY tune_count DESC;
        """,
        conn,
    )

    conn.close()
    return df

def tunes_per_book() -> pd.DataFrame:
    """
    df that shows how many tunes cam from each book directory.
    """
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT book_number, COUNT(*) AS tune_count
        FROM tunes
        GROUP BY book_number
        ORDER BY book_number;
        """,
        conn,
    )

    conn.close()
    return df

if __name__ == "__main__":

    print("\n---Tunes by key---\n")
    print(tunes_by_key())

    print("\n---Tunes by type---\n")
    print(tunes_by_type())

    print("\n---Tunes by book---\n")
    print(tunes_by_book())