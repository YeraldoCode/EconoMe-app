from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector 
import datos
import os


app = Flask(__name__)
# Configurar clave secreta para las sesiones
app.secret_key = os.urandom(24)
conexion = mysql.connector.connect(host=datos.host, 
                                   user=datos.user, 
                                   password=datos.password, 
                                   database=datos.database)
cursor = conexion.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/logout')
def logout():
    # Eliminar datos de la sesión
    session.clear()
    return redirect(url_for('login'))

# Proteger rutas que requieren autenticación
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/perfil')
def perfil():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html')

@app.route('/analisis')
def analisis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('analisis.html')

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form.get('unombre')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute('INSERT INTO usuarios (nombre, email, clave) VALUES (%s, %s, %s)', 
                  (nombre, email, password))
    conexion.commit()
    return render_template('home.html')

@app.route('/validacion_login', methods=['POST'])
def validacion_login():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute('SELECT * FROM usuarios WHERE email = %s AND clave = %s', (email, password))
    usuarios = cursor.fetchall()
    
    if len(usuarios) > 0:
        return render_template('home.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

