# Starter code for Data Centric Programming Assignment 2025

# Karl Ypil C24383681



# Bryan Duggan likes Star Trek
# Bryan Duggan is a great flute player
# this is a test commit!
import os 
import sqlite3
import pandas as pd

books_dir = "abc_books" # location of the ABC tune folders
DB_NAME = "tunes.db"

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tunes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_number INTEGER,
        file_name TEXT,
        tune_index INTEGER,
        title TEXT,
        tune_type TEXT,
        meter TEXT,
        tune_key TEXT,
        raw_abc TEXT
        );
    """)
    conn.commit()


def find_abc_files():
    """
    Scan abc_books folder for any numbered subfolders and collect all the files inside them.
    it returns a list of dictionaries
    """
    abc_files = []
    
    # looks inside the abc_books directory
    for item in os.listdir(books_dir):
        folder_path = os.path.join(books_dir, item)

        # must be a folder AND must be named wit digits
        if os.path.isdir(folder_path) and item.isdigit():
            book_number = int(item)

            # loop through files inside each numbered folder
            for filename in os.listdir(folder_path):
                if filename.endswith(".abc"):
                    full_path = os.path.join(folder_path, filename)

                    abc_files.append({
                        "book": book_number,
                        "file": filename,
                        "path": full_path
                    })
    return abc_files

def parse_abc_file(path, book_number, file_name):
    """
    Skeleton for the ABC parsing function.
    -Opens the file 
    -Strips whitespace
    -Prints a preview of it's contents
    """

    # reads the ABC file
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # remove trailing spaces and newline characters
    cleaned_lines = [line.strip() for line in raw_lines]

    # debug preview so we know it's working
    print(f"\n Reading ABC file: {file_name} (Book {book_number})")
    print("----")
    for line in cleaned_lines[:10]:
        print(line)
    print("----")

    return []


def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        # print(line)
        pass


# my_sql_database()
# do_databasse_stuff()

# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        print(f"Found numbered directory: {item}")
        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process_file(file_path)
                
if __name__ == "__main__":
    # 1) open the database connection
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)

    #2) Find all .abc files
    abc_files = find_abc_files()
    print(f"\nFound {len(abc_files)} ABC files total. \n")

    #3) for each ABC file call the parser skeleton
    for f in abc_files:
        parse_abc_file(
            path=f["path"],
            book_number=f["book"],
            file_name=f["file"]
        )
    conn.close()