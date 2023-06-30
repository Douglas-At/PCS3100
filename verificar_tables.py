import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute the query to fetch table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Fetch all the table names
table_names = cursor.fetchall()

# Print the table names
for name in table_names:
    print(name[0])

# Close the connection
conn.close()
