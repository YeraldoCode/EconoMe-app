from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector 
import datos
import os
from datetime import datetime

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
    if 'id' not in session:
        return redirect(url_for('login'))
    
    id_usuario = session['id']
    
    # Obtener total de ingresos
    cursor.execute('''
        SELECT COALESCE(SUM(monto), 0) 
        FROM movimientos 
        WHERE id_usuario = %s AND tipo = 'ingreso'
    ''', (id_usuario,))
    total_ingresos = cursor.fetchone()[0]
    
    # Obtener total de egresos
    cursor.execute('''
        SELECT COALESCE(SUM(monto), 0) 
        FROM movimientos 
        WHERE id_usuario = %s AND tipo = 'egreso'
    ''', (id_usuario,))
    total_egresos = cursor.fetchone()[0]
    
    # Calcular saldo
    saldo = float(total_ingresos) - float(total_egresos)
    
    # Obtener movimientos
    cursor.execute('''
        SELECT id, descripcion, monto, tipo, fecha 
        FROM movimientos 
        WHERE id_usuario = %s 
        ORDER BY fecha DESC
    ''', (id_usuario,))
    movimientos = cursor.fetchall()
    
    return render_template('home.html',
                         total_ingresos=total_ingresos,
                         total_egresos=total_egresos,
                         saldo=saldo,
                         movimientos=movimientos)

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
        return redirect(url_for('home'))  # Cambiar a redirect en lugar de render_template
    else:
        return render_template('login.html')
    

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    try:
        nombre = request.form.get('unombre')
        email = request.form.get('uemail')
        password = request.form.get('upassword')
        
        # Insertar nuevo usuario
        cursor.execute('INSERT INTO usuarios (nombre, email, clave) VALUES (%s, %s, %s)', 
                      (nombre, email, password))
        conexion.commit()
        
        # Obtener el ID del usuario recién creado
        cursor.execute('SELECT id FROM usuarios WHERE email = %s', (email,))
        usuario = cursor.fetchone()
        
        # Guardar el ID en la sesión
        session['id'] = usuario[0]
        
        # Redirigir a home en lugar de render_template
        return redirect(url_for('home'))
        
    except Exception as e:
        conexion.rollback()
        print(f"Error al agregar usuario: {str(e)}")
        return redirect(url_for('registro'))



@app.route('/agregar_movimiento', methods=['POST'])
def agregar_movimiento():
    if 'id' not in session:  # Cambiar 'user_id' por 'id'
        return redirect(url_for('login'))
    
    try:
        descripcion = request.form.get('descripcion')
        monto = float(request.form.get('monto'))
        tipo = request.form.get('tipo')
        fecha = datetime.now()
        id_usuario = session['id']  # Cambiar 'user_id' por 'id'
        
        if not descripcion or not monto or not tipo:
            return redirect(url_for('home'))
        
        cursor.execute('''
            INSERT INTO movimientos 
            (descripcion, monto, tipo, fecha, id_usuario) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (descripcion, monto, tipo, fecha, id_usuario))
        
        conexion.commit()
        return redirect(url_for('home'))
        
    except Exception as e:
        conexion.rollback()
        print(f"Error al agregar movimiento: {str(e)}")
        return redirect(url_for('home'))
    



if __name__ == '__main__':
    app.run(debug=True)

