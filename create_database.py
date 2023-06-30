import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

'''cursor.execute("DROP TABLE acompanhamento")
conn.commit()
conn.close()
quit()'''


# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS hist_lixo (
        id INTEGER PRIMARY KEY,
        data DATETIME,
        valor INTEGER,
        chao INTEGER,
        otimizado INTEGER,
        padrao INTEGER,
        lixeira_real INTEGER
        )''')

# Commit the changes and close the connection
conn.commit()
conn.close()
