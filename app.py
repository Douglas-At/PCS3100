from flask import Flask, render_template, request,redirect, make_response, jsonify, render_template_string
import sqlite3
import socket
import csv
from io import StringIO
from datetime import datetime
import random
import matplotlib.pyplot as plt
import pandas as pd
import base64
import json

esp32_ip = '192.168.15.74'
esp32_port = "COM3"

def send_command(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((esp32_ip, esp32_port))
    sock.send(command.encode())
    response = sock.recv(1024).decode().strip()
    sock.close()
    return response

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT lugar FROM ruas")
    data = cursor.fetchall()
    conn.close()
    #value = send_command('get_value')
    #tirat o value par anãp dar pau 
    #   value=value

    return render_template('index.html', data=data)

#add lugar ao databsase
@app.route('/add_lugar', methods=['POST'])
def add_lugar():
    # Retrieve the submitted "lugar" value from the request
    data = request.json
    lugar = data.get('lugar')

    # Insert the "lugar" value into the "ruas" table
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ruas (lugar) VALUES (?)", (lugar,))
    conn.commit()
    conn.close()

    # Retrieve the updated list of "lugar" values
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT lugar FROM ruas")
    data = cursor.fetchall()
    conn.close()

    return jsonify(data)



@app.route('/download_csv', methods=['POST'])
def download_csv():
    # Retrieve the filter values from the request
    filter1 = request.form.get('filter1')
    filter2 = request.form.get('filter2')
    print(f"filter3: {filter1}","AQUIIII")
    print(f"filter4: {filter2}")
    #teste com datas já inputadas
    #filter1 = "05/06/2023"
    #filter2 = "15/06/2023"  
    filter1_date = datetime.strptime(filter1, '%d/%m/%Y').strftime('%Y-%m-%d')
    filter2_date = datetime.strptime(filter2, '%d/%m/%Y').strftime('%Y-%m-%d')

    # Retrieve data from the database based on the filters
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hist_lixo WHERE data BETWEEN ? AND ?", (filter1_date, filter2_date))
    data = cursor.fetchall()
    conn.close()

    # Create a CSV file
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'data', 'valor', 'chao', 'otimizado','lixeira_real'])
    writer.writerows(data)

    # Prepare response headers
    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename=dados_lixeira_1.csv',
        'Content-type': 'text/csv'
    }

    return output.getvalue(), headers


def sum_values_before_zeros(lst):
    
    current_sum = 0

    for value in lst:
        if value == 0:
            current_sum += z
        z = value
    return current_sum


@app.route('/generate_plot', methods=['POST'])
def filter_plot():
    # Retrieve the filter values from the request
    filter3 = request.form.get('filter3')
    filter4 = request.form.get('filter4')
    print(f"filter3: {filter3}","AQUIIII")
    print(f"filter4: {filter4}")
    #teste com datas já inputadas
    #filter3 = "05/06/2023"
    #filter4 = "06/06/2023"  
    filter3_date = datetime.strptime(filter3, '%d/%m/%Y').strftime('%Y-%m-%d')
    filter4_date = datetime.strptime(filter4, '%d/%m/%Y').strftime('%Y-%m-%d')
    # Retrieve data from the database based on the filters
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hist_lixo WHERE data BETWEEN ? AND ?", (filter3_date, filter4_date))
    data = cursor.fetchall()
    conn.close()

    json_data = json.dumps(data)
    filtered_df = pd.read_json(json_data)
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS hist_lixo (
        id INTEGER PRIMARY KEY,
        data DATETIME,1
        valor INTEGER,2
        chao INTEGER,3
        otimizado INTEGER,4
        padrao INTEGER,5
        lixeira_real INTEGER6
        )''')"""
    # Plot the graph using matplotlib
    filtered_df.columns = ['id','data','valor','chao','otimizado','padrao','lixeira_real']
    plt.plot(filtered_df['data'], filtered_df['chao'], label='Lixo chao')
    plt.plot(filtered_df['data'], filtered_df['lixeira_real'], label='Lixeira Normal')
    plt.plot(filtered_df['data'], filtered_df['otimizado'], label='Lixeira Otimizada')

    # Customize the graph labels, title, etc.
    plt.xlabel('Tempo')
    plt.ylabel('KG')

    acumulado = sum_values_before_zeros(filtered_df['chao'])
    print(acumulado)
    acumulado  =  format(acumulado, ",.0f").replace(",", ".")
    dias = format(len(filtered_df)/5760, ",.0f").replace(",","")
    plt.title('Total de lixo evitado {} G em {} dias'.format(acumulado, dias))
    
    plt.legend()

    # Save the graph image to a file
    image_path = 'image.png'
    plt.savefig(image_path)
    
    plt.close()

    # Convert the image to base64-encoded data
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    return render_template_string('<img src="data:image/png;base64,{{ image_data }}" />', image_data=image_data)
    

@app.route('/generate_numbers')
def generate_numbers():
    # Generate random numbers
    number1 = random.randint(1, 10)
    number2 = random.randint(1, 10)
    number3 = random.randint(1, 10)

    # Return the numbers as JSON response
    return {
        'number1': number1,
        'number2': number2,
        'number3': number3
    }



if __name__ == '__main__':
    app.run()