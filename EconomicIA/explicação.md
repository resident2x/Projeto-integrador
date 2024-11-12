### 1. Importação de Bibliotecas
```python
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import yfinance as yf
from datetime import datetime, timedelta
```
Aqui, importamos todas as bibliotecas necessárias para manipulação de dados, requisições HTTP, visualização, modelagem preditiva e obtenção de dados financeiros.

### 2. Coleta de Dados com `yfinance`
```python
today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
ticker = 'GC=F'
data = yf.download(ticker, start="2024-01-01", end=today_str)
```
Obtemos os dados financeiros do ativo identificado pelo ticker `'GC=F'` (que representa contratos futuros de ouro) desde 1 de janeiro de 2024 até a data atual.

### 3. Tratamento de Dados
```python
data = data[['Close']]
data.dropna(inplace=True)
```
Selecionamos a coluna de preços de fechamento e removemos quaisquer valores nulos.

### 4. Preparação dos Dados para o Modelo
```python
n_days = 30

X = []
y = []

for i in range(n_days, len(data)):
    X.append(data['Close'].iloc[i-n_days:i].values)
    y.append(data['Close'].iloc[i])

X = np.array(X)
y = np.array(y)

X = X.reshape(X.shape[0], -1)
```
Criamos janelas de 30 dias de dados passados (`X`) para prever o preço no dia seguinte (`y`). Convertendo em arrays numpy e ajustando a forma dos dados para se adequar ao modelo.

### 5. Divisão dos Dados em Treino e Teste
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
```
Dividimos os dados em conjuntos de treinamento e teste, sem embaralhar (shuffle=False) para manter a ordem temporal.

### 6. Treinamento do Modelo
```python
modelo = LinearRegression()
modelo.fit(X_train, y_train)
```
Treinamos um modelo de regressão linear com os dados de treinamento.

### 7. Previsão e Avaliação do Modelo
```python
y_pred = modelo.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
```
Usamos o modelo treinado para prever os preços de teste e calculamos o erro quadrático médio (MSE) e a raiz do erro quadrático médio (RMSE).

### 8. Visualização dos Resultados
```python
plt.figure(figsize=(10,6))
plt.plot(data.index[-len(y_test):], y_test, label="Preço Real", color="blue")
plt.plot(data.index[-len(y_test):], y_pred, label="Preço Previsto", color="red")
plt.title(f'Previsão de Preços - {ticker}')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.legend()
plt.show()
```
Criamos um gráfico para comparar os preços reais e previstos.

### 9. Obtenção de Taxas de Câmbio
```python
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
```
Criamos uma função para obter as taxas de câmbio do USD e EUR para BRL usando uma API externa.

### 10. Previsão de Preços Futuro e Cálculo das Cotações
```python
recent_days = 30
average_recent_values = data['Close'].iloc[-recent_days:].mean()

prediction_date = datetime.now() + timedelta(days=1)
past_prices = data['Close'].iloc[-n_days:].values.reshape(1, -1)
predicted_price = modelo.predict(past_prices)
prediction_date_str = prediction_date.strftime('%Y-%m-%d')

cotacao_usd, cotacao_eur = obter_cotacoes()
cotacao_usd = round(cotacao_usd, 2)
cotacao_eur = round(cotacao_eur, 2)

cotacao_usd_brl = round(predicted_price[0][0] / cotacao_usd, 2)
cotacao_eur_brl = round(predicted_price[0][0] / cotacao_eur, 2)
```
Calculamos a previsão de preço futuro e convertemos os valores previstos em BRL utilizando as taxas de câmbio obtidas.

### 11. Exibição de Resultados e Recomendações
```python
print(f"A media do valor no periodo de ({recent_days} dias): BRL {float(average_recent_values.iloc[0]):.2f}")
print(f"RMSE (Erro Quadrático Médio): {rmse:.2f}")
print(f"Previsão para o dia {prediction_date_str}: BRL {predicted_price[0][0]:.2f}")
print(f"Valor brl: {cotacao_usd_brl} USD")
print(f"Valor brl: {cotacao_eur_brl} EUR")
if predicted_price[0][0] > average_recent_values.iloc[0]:
  print("A previsão é positiva, aconselho a vender em relaçao a media dos ultimos 30 dias")
else:
  print("A previsão é negativa, aconselho a compra em relação a media dos ultimos 30")
```
Mostramos a média dos preços recentes, o RMSE, a previsão de preço para o dia seguinte, e as cotações em USD e EUR. Também fornecemos uma recomendação com base na previsão.
