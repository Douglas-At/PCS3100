import pandas as pd
from pathlib import Path
import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Specify the name of the Excel sheet to be added to the table


# Identify the Excel file to be imported
filename = [i for i in os.listdir() if i.startswith('df_base')]
filename.sort(key=os.path.getctime, reverse=True)
filename = filename[0]

try:
    df = pd.read_excel(filename)
    df.rename(columns={'Unnamed: 0':"id", "Data":"data","Valor":"valor","Chão":"chao","Otimizada":"otimizado","Padrão":"padrao","Lixeira_Real":"lixeira_real"}, inplace=True)
    df.set_index("id", inplace=True)
    df.to_sql('hist_lixo', conn, if_exists='append', index=True)
    conn.commit()
    conn.close()

except Exception as e:
    print(e)
