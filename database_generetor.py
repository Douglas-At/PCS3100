"""
2 - Calculos em cima da database criar 
    2.1 - Tempo até encher
    2.2 - Tempo que irá ficar cheia no metodo antigo e qnt irá ficar cheia no metodo novo
    2.3 - Gráfico histórico de coleta de lixo para plotar gráfico entre os 2 metodos 

3 - Gerar uma conclusão em número de horas e constancia de lixo que foi jogada no chão pq a lixeira estava cheia 

4 - botão de envio de gari

5 - botão de exportas csv com a database que tenho salva
"""
import pandas as pd
import os 
import sqlite3
import numpy as np
import xlwings as xw
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
'''
#crinado para intervalo de 15 segundos 

inicio = pd.Timestamp('2023-05-28 00:00:00')
fim = pd.Timestamp('2023-06-28 23:59:59')

index = pd.date_range(start=inicio, end=fim, freq='15S')
valores = []
for _ in range(len(index)):
    valor = np.random.choice([0,np.random.randint(15, 25)], p=[0.9,0.1])
    valores.append(valor)


df = pd.DataFrame({'Data':index,'Valor': valores})
otimizada = []
padrao = []
chao = []
soma_o = df.iloc[0,1]
soma_p = df.iloc[0,1]
lixo = 0
acumulado = 0
#pegar intervalo de 1 dia
dias = 30
x = 5760*dias

df = df.iloc[0:x,:]

for i,row in df.iterrows():
    valor = row.Valor
    
    #fazendo dentro do loop o modo otimizado 
    if i != 0:
        if soma_o + valor > 3000:
            soma_o = valor
            otimizada.append(soma_o)
        else:
            soma_o += valor
            otimizada.append(soma_o)
    else:
        otimizada.append(valor)
    #metodo tradicional de limpeza a cada 8h
    if i != 0:
        if soma_p > 3000 :
            lixo = soma_p - 3000
            chao.append(lixo)
        else:
            chao.append(0)

        if i%1920 == 0:
            acumulado += lixo
            soma_p = valor
            padrao.append(soma_p)
        else:
            soma_p += valor
            padrao.append(soma_p)
    else:
        padrao.append(valor)
        chao.append(0)



df['Chão'] = chao
df['Otimizada'] = otimizada
df['Padrão'] = padrao
df['Lixeira_Real'] = np.where(df['Padrão'] < 3000, df['Padrão'], 3000)
'''
df = pd.read_excel("df_base.xlsx")
df = df.iloc[5760*15:5760*16,:]
def sum_values_before_zeros(lst):
    
    current_sum = 0

    for value in lst:
        if value == 0:
            current_sum += z
        z = value
    return current_sum
print(df)
plt.plot(df['Data'], df['Chão'], label='Lixo chao')
plt.plot(df['Data'], df['Lixeira_Real'], label='Lixeira Normal')
plt.plot(df['Data'], df['Otimizada'], label='Lixeira Otimizada')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)


plt.xlabel('Tempo')
plt.ylabel('KG')
acumulado = sum_values_before_zeros(df['Chão'])
acumulado  =  format(acumulado, ",.0f").replace(",", ".")
dias = format(len(df)/5760, ",.0f").replace(",","")
plt.title('Total de lixo evitado {} G em {} dias'.format(acumulado, dias))
plt.legend()
plt.show()
