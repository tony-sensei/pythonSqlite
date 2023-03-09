import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/testDatabase.db')

# Get a cursor object
cur = conn.cursor()

# Get a list of tables in the database
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

if len(tables) == 0:
    print("No tables inside the DB")
else:
    # Print the list of tables
    print("Tables in the database:")
    for table in tables:
        print(table[0])

    # View the schema of a specific table
    table_name = 'transitions'
    cur.execute(f"PRAGMA table_info({table_name});")
    schema = cur.fetchall()

    print(f"\nSchema for table '{table_name}':")
    for column in schema:
        print(f"{column[1]}: {column[2]}")

    # Execute a SELECT statement to retrieve all the entries in the questions table
    cur.execute(f"SELECT * FROM {table_name};")
    entries = cur.fetchall()

    # Print the entries
    print("\nprinting entries: ")
    for entry in entries:
        print(entry)