import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Specify the name of the table
table_name = 'hist_lixo'

# Fetch the table schema
cursor.execute(f"PRAGMA table_info({table_name})")
rows = cursor.fetchall()

# Extract the column names
column_names = [row[1] for row in rows]

# Print the column names
for column_name in column_names:
    print(column_name)

# Close the cursor and the database connection
cursor.close()
conn.close()
