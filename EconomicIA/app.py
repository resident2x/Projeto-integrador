import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import yfinance as yf
from datetime import datetime, timedelta

today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
ticker = 'PL=F'
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

plt.figure(figsize=(10,6))
plt.plot(data.index[-len(y_test):], y_test, label="Preço Real", color="blue")
plt.plot(data.index[-len(y_test):], y_pred, label="Preço Previsto", color="red")
plt.title(f'Previsão de Preços - {ticker}')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.legend()
plt.show()

recent_days = 30
average_recent_values = data['Close'].iloc[-recent_days:].mean()

def media():
  return print(f"A media do valor no periodo de ({recent_days} dias): R$ {float(average_recent_values.iloc[0]):.2f}")

prediction_date = datetime.now() + timedelta(days=1)
past_prices = data['Close'].iloc[-n_days:].values.reshape(1, -1)
predicted_price = modelo.predict(past_prices)

prediction_date_str = prediction_date.strftime('%Y-%m-%d')
media()
print(f"RMSE (Erro Quadrático Médio): {rmse:.2f}")
print(f"Previsão para o dia {prediction_date_str}: USD {predicted_price[0][0]:.2f}")
if predicted_price[0][0] > average_recent_values.iloc[0]:
  print("A previsão é positiva, aconselho a vender em relaçao a media dos ultimos 30 dias")
else:
  print("A previsão é negativa, aconselho a compra em relação a media dos ultimos 30")
