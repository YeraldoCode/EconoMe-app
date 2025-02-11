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

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/')
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Proteger rutas que requieren autenticación
@app.route('/home')
def home():
        if 'id' in session:
            return render_template('home.html')
        else:
            return redirect(url_for('/'))

@app.route('/perfil')
def perfil():
        if 'id' in session:
            return render_template('perfil.html')
        else:
            return redirect(url_for('/'))

@app.route('/analisis')
def analisis():
        if 'id' in session:
            return render_template('analisis.html')
        else:
            return redirect(url_for('/'))


@app.route('/validacion_login', methods=['POST'])
def validacion_login():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute('SELECT * FROM usuarios WHERE email = %s AND clave = %s', (email, password))
    usuarios = cursor.fetchall()


    if len(usuarios) > 0:
        session['id'] = usuarios[0][0]
        return render_template('home.html')
    else:
        return render_template('login.html')
    

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form.get('unombre')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute('INSERT INTO usuarios (nombre, email, clave) VALUES (%s, %s, %s)', 
                  (nombre, email, password))
    conexion.commit()
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)

