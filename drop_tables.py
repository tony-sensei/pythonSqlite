import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/testDatabase.db')

# Get a cursor object
cur = conn.cursor()

# Disable foreign key constraints for SQLite
cur.execute("PRAGMA foreign_keys = OFF")

# Get a list of all tables in the database
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
table_names = [row[0] for row in cur.fetchall()]

# Drop all tables in the database
for table_name in table_names:
    cur.execute(f"DROP TABLE {table_name}")

# Commit the changes to the database
conn.commit()

# Close the cursor and connection objects
cur.close()
conn.close()