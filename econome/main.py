from flask import Flask, render_template, request
from flask import request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/analisis')
def analisis():
    return render_template('analisis.html')

@app.route('/validacion_login', methods=['POST'])
def validacion_login():
    email = request.form.get('email')
    password = request.form.get('password')
    return f'el email es {email} y el password es {password}'

if __name__ == '__main__':
    app.run(debug=True)

