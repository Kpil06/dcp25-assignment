# Starter code for Data Centric Programming Assignment 2025

# Karl Ypil C24383681



# Bryan Duggan likes Star Trek
# Bryan Duggan is a great flute player
import os 
import sqlite3

books_dir = "abc_books" # location of the ABC tune folders
DB_NAME = "tunes.db"

def get_connection():
    """
    Helper function to open connection to SQLite.
    """
    return sqlite3.connect(DB_NAME)

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

def insert_tunes(conn, tunes):
    """
    Insert a list of tune dictionaries into the tunes table.

    Each tune dict should have keys:
      - book_number
      - file_name
      - tune_index
      - title
      - tune_type
      - meter
      - tune_key
      - raw_abc
    """
    cursor = conn.cursor()

    # Build a list of tuples (one per tune) with values in the same order
    rows_to_insert = [
        (
            tune["book_number"],  # book folder number, e.g. 1 or 2
            tune["file_name"],    # abc file name, e.g. "hnbuchimish0.abc"
            tune["tune_index"],   # X: number in the ABC
            tune["title"],        # T: line
            tune["tune_type"],    # R: line
            tune["meter"],        # M: line
            tune["tune_key"],     # K: line
            tune["raw_abc"],      # full raw ABC text for that tune
        )
        for tune in tunes
    ]

    # Use executemany with (SQL, list_of_tuples)
    cursor.executemany("""
        INSERT INTO tunes (
            book_number,
            file_name,
            tune_index,
            title,
            tune_type,
            meter,
            tune_key,
            raw_abc
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows_to_insert)

    # Save the changes to the DB
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

def build_tune_from_lines(lines, book_number, file_name):
    """
    We are given all the lines for a single tune, so we extract the header fields and return a dictionary ready to insert into the database.
    """

    tune_index = None   # X:
    title = None        #first T:
    tune_type = None    # R:
    meter = None        # M:
    tune_key = None     #K:

    for line in lines:
        # remove leading/trailing spaces
        stripped = line.strip()

        # tune index
        if stripped.startswith("X:"):
            # everything after x is the number
            try:
                tune_index = int(stripped[2:].strip())
            except ValueError:
                tune_index = None

        # Title, only use the first T: line
        elif stripped.startswith("T:") and title is None:
            title = stripped[2:].strip()
        
        # Rythmn / tune_type
        elif stripped.startswith("R:") and tune_type is None:
            tune_type = stripped[2:].strip()

        # Meter
        elif stripped.startswith("M:") and meter is None:
            meter = stripped[2:].strip()

        # Key
        elif stripped.startswith("K:") and tune_key is None:
            tune_key = stripped[2:].strip()
    
    # Join all teh lines together as one block of ABC text
    raw_abc = "\n".join(lines)

    return {
        "book_number": book_number,
        "file_name": file_name,
        "tune_index": tune_index,
        "title": title,
        "tune_type": tune_type,
        "meter": meter,
        "tune_key": tune_key,
        "raw_abc": raw_abc
    }


def parse_abc_file(path, book_number, file_name):
    """
    Parse an .abc file and return a list of tune dictionaries.

    The function:
    - Reads all lines from the file
    - Skips intro text till it finds a line starting with 'X:' or end of the file
    - Extracts the basic metadata form the header lines
    """
    print(f"Reading ABC file: {file_name} (Book {book_number})")
    print("----")

    tunes = [] # list to hold all the tunes in this file
    current_lines = [] # lines for teh tune we are currently building

    # Opens and reads all lines, stripping newline characters
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.rstrip("\n") for line in f]

    for line in lines:
        # when we see a new 'X:' line that means:
        # If we were already ina. tune, we should finish it first
        # Then after start a new tune
        if line.startswith("X:"):
            # If we have lines from a pervious tune, we finish it
            if current_lines:
                tune = build_tune_from_lines(
                    current_lines,
                    book_number,
                    file_name
                )
                tunes.append(tune)

            # start a new tune with X:
            current_lines = [line]
        else:
            # if X not reached we are in the intro, so skip
            if current_lines: # only collect lines after hitting the first X:
                current_lines.append(line)

    # after the loop ends, a tune might still be in progress
    if current_lines:
        tune = build_tune_from_lines(
            current_lines,
            book_number,
            file_name
        )
        tunes.append(tune)
        print(f"    Parsed tune X:{tune['tune_index']} - {tune['title']}")
        print("----")
    
    print(f"Finished {file_name}: {len(tunes)} tunes found\n")
    
    return tunes

def import_all_abc():
    """
    Walk through the abc_books directory, parse every .abc file
    from all numbered subfolders, and insert all tunes into the SQLite DB.
    """

    # 1) Open ONE connection for the entire import
    conn = sqlite3.connect(DB_NAME)

    # 2) Ensure tables exist
    create_tables(conn)

    total_tunes = 0

    # 3) Walk through the parent directory containing book folders
    for item in os.listdir(books_dir):
        item_path = os.path.join(books_dir, item)

        # Check if it's a directory with a numeric name
        if os.path.isdir(item_path) and item.isdigit():
            book_number = int(item)
            print(f"Found numbered directory (book): {book_number}")

            # 4) Loop through every .abc file 
            for file_name in os.listdir(item_path):
                if file_name.endswith(".abc"):
                    file_path = os.path.join(item_path, file_name)

                    print(f"Reading ABC file: {file_name} (Book {book_number})")

                    # 5) Parse tunes from this file
                    tunes = parse_abc_file(
                        path=file_path,
                        book_number=book_number,
                        file_name=file_name
                    )

                    print("----")
                    if tunes:
                        # Debug summary
                        first_tune = tunes[0]
                        print(f"    Parsed tune X:{first_tune['tune_index']} - {first_tune['title']}")
                        print(f"Finished {file_name}: {len(tunes)} tunes found\n")

                        # 6) Insert into DB using the SAME conn
                        insert_tunes(conn, tunes)
                        total_tunes += len(tunes)
                    else:
                        print(f"    No tunes found in {file_name}\n")

    print(f"Inserted {total_tunes} tunes into the database in total.")

    # 7) Only close AFTER all books/files are processed
    conn.close()

# runs the import if the script is executed directly
if __name__ == "__main__":
    import_all_abc()


if __name__ == "__main__":
    # 1) open the database connection
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)

    #2) Find all .abc files
    abc_files = find_abc_files()
    print(f"\nFound {len(abc_files)} ABC files total. \n")
