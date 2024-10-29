from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

df = pd.read_csv("pizzas.csv")
modelo = LinearRegression()
y = df[["TAMANHO"]]
x = df[["VALOR"]]
modelo.fit(y, x)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        tamanho = float(request.form['tamanho'])
        valor = modelo.predict([[tamanho]])[0][0]
        resultado = f"O valor previsto para uma pizza de tamanho {tamanho} de circunferência é: {valor:.2f}$"

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Previsão de Valores</title>
    <style>
     body{
         height:100dvh;
         display:flex;
         flex-direction:column;
         justify-content:center;
         align-items:center; 
         font-family:;
     }
    </style>
    </head>
    <body class="bg-info-subtle">
        <h1>Prever o Valor das Pizzas</h1>
        <form action="/" method="post">
            Tamanho da Pizza: <input type="number" name="tamanho"><br>
            <input type="submit" value="Prever Valor">
        </form>
        {% if resultado %}
            <p>{{ resultado }}</p>
        {% endif %}
    </body>
    </html>
    ''', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
