import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import yfinance as yf
from datetime import datetime, timedelta


today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
ticker = 'MARA'
data = yf.download(ticker, start="2024-01-01", end=today_str)

# se quiser ver os valores recenstes apague esse comentario e deixe apenas esse codigo a frente: print(data.head())

data = data[['Close']]
data.dropna(inplace=True)

n_days = 30

X = []
y = []

for i in range(n_days, len(data)):
    X.append(data['Close'].iloc[i-n_days:i].values)
    y.append(data['Close'].iloc[i])

X = np.array(X)
y = np.array(y)

X = X.reshape(X.shape[0], -1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

modelo = LinearRegression()

modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# parte do grafico

plt.figure(figsize=(10,6))
plt.plot(data.index[-len(y_test):], y_test, label="Preço Real", color="blue")
plt.plot(data.index[-len(y_test):], y_pred, label="Preço Previsto", color="red")
plt.title(f'Previsão de Preços - {ticker}')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.legend()
plt.show()

# cotações 

EXCHANGE_RATE_API_KEY = 'dc27d5434e168b4c4d0dfc45'

def obter_cotacoes():
        url_usd = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD'
        url_eur = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/EUR'
        
        resposta_usd = requests.get(url_usd)
        resposta_usd.raise_for_status()
        cotacao_usd = resposta_usd.json()['conversion_rates']['BRL']

        resposta_eur = requests.get(url_eur)
        resposta_eur.raise_for_status()
        cotacao_eur = resposta_eur.json()['conversion_rates']['BRL']
        
        return cotacao_usd, cotacao_eur

recent_days = 30
average_recent_values = data['Close'].iloc[-recent_days:].mean()

prediction_date = datetime.now() + timedelta(days=1)
past_prices = data['Close'].iloc[-n_days:].values.reshape(1, -1)
predicted_price = modelo.predict(past_prices)
prediction_date_str = prediction_date.strftime('%Y-%m-%d')

# Calculando cotações

cotacao_usd, cotacao_eur = obter_cotacoes()
cotacao_usd = round(cotacao_usd, 2)
cotacao_eur = round(cotacao_eur, 2)

cotacao_usd_brl = round(predicted_price[0][0] / cotacao_usd, 2)
cotacao_eur_brl = round(predicted_price[0][0] / cotacao_eur, 2)

print(cotacao_eur_brl)
print(cotacao_usd_brl)

# Mensagens

print(f"A media do valor no periodo de ({recent_days} dias): BRL {float(average_recent_values.iloc[0]):.2f}")
print(f"RMSE (Erro Quadrático Médio): {rmse:.2f}")
print(f"Previsão para o dia {prediction_date_str}: BRL {predicted_price[0][0]:.2f}")
print(f"")
if predicted_price[0][0] > average_recent_values.iloc[0]:
  print("A previsão é positiva, aconselho a vender em relaçao a media dos ultimos 30 dias")
else:
  print("A previsão é negativa, aconselho a compra em relação a media dos ultimos 30")
