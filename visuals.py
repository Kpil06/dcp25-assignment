"""
Visualising the dataset using matplotlib
imports the analysis functions that are already in the df and use them to make graphs.
"""

import matplotlib.pyplot as plt

# import the analysis functions
from analysis import tunes_by_key, tunes_by_type

def plot_tunes)by_key() -> None:
    """
    Bar chart showing how many tunes per tune type.
    """
    df = tunes_by_type()

    plt.figure(figsize=(10, 6))
    plt.bar(df["tune_type"].astype(str), df["tune_count"])
    plt.xticks(rotation=45)

    plt.title("Number of tunes per tune type")
    plt.xlabel("Tune type")
    plt.ylabel("Number of tunes")
    plt.tight_layout()
    plt.show()
