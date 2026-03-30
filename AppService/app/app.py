from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    entorno = os.environ.get('mi_entorno', 'No definido')
    return f"<h1>Bienvenido</h1><p>Variable de entorno mi_entorno: {entorno}</p>"

if __name__ == '__main__':
    app.run(debug=True)
