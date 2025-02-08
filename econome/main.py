from flask import Flask, render_template

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




if __name__ == '__main__':
    app.run(debug=True)

