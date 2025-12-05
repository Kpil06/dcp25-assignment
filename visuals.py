"""
Visualising the dataset using matplotlib
imports the analysis functions that are already in the df and use them to make graphs.
"""

import matplotlib.pyplot as plt

# import the analysis functions
from analysis import tunes_by_key, tunes_per_book

def plot_tunes_per_book() -> None:
    """
    Bar chart showing how many tunes per tune book.
    """
    df = tunes_per_Book()

    plt.figure(figsize=(8, 5))
    plt.bar(df["book_number"].astype(str), df["tune_count"])
    plt.xticks(rotation=45)

    plt.title("Number of tunes per book")
    plt.xlabel("Book number")
    plt.ylabel("Number of tunes")
    plt.tight_layout()
    plt.show()

def plot_tunes_by_key() -> None:
    """
    Bar chart showing how many tunes per key.
    """
    df = tunes_by_key()

    plt.figure(figsize=(12, 6))
    plt.bar(df["tune_type"].astype(str), df["tune_count"])
    plt.xticks(rotation=90)

    plt.title("Number of tunes per key")
    plt.xlabel("Key")
    plt.ylabel("Number of tunes")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Showing tunes per type..")
    plot_tunes_by_type()

    print("Showing tunes per key...")
    plot_tunes_by_key()