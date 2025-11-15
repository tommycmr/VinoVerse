import os
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, send_file
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import MySQLdb.cursors
import time

app = Flask(__name__, static_url_path='/static')

# Configuración de Flask y MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'vinoverse'
app.secret_key = 'supersecretkey'

# Configuración de la carpeta de subida de imágenes
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/image')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} 
mysql = MySQL(app)

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Tienes que iniciar sesión para entrar a la página."

class User(UserMixin):
    def __init__(self, id, email, contraseña):
        self.id = id
        self.email = email
        self.contraseña = contraseña

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, email, contraseña FROM usuarios WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT id, email, contraseña FROM usuarios WHERE email = %s", (email,))
            user = cur.fetchone()
        
        if user and user[2] == contraseña:  # Verifica que la contraseña sea correcta
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            return redirect(url_for('perfil', usuario_id=user_obj.id))  # Usar el ID del usuario autenticado
        else:
            flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    tipo_cuenta = None
    tipo_empresa = None

    if request.method == 'POST':
        # Obtención de datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        confirm_password = request.form['confirm_password']
        tipo_cuenta = request.form['tipo_cuenta']
        tipo_empresa = request.form.get('tipo_empresa')  # Esto solo se enviará si 'tipo_cuenta' es 'empresa'

        # Validación de que las contraseñas coincidan
        if contraseña != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('register'))

        # Verificación de que el correo no esté registrado
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            
            if existing_user:
                flash('El correo ya está registrado', 'error')
                return redirect(url_for('register'))

            # Inserción de datos en la base de datos
            if tipo_cuenta == 'empresa':
                cur.execute("INSERT INTO usuarios (nombre, apellido, email, contraseña, tipo_cuenta, tipo_empresa, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
                            (nombre, apellido, email, contraseña, tipo_cuenta, tipo_empresa))
            else:
                cur.execute("INSERT INTO usuarios (nombre, apellido, email, contraseña, tipo_cuenta, fecha_registro) VALUES (%s, %s, %s, %s, %s, NOW())",
                            (nombre, apellido, email, contraseña, tipo_cuenta))

            # Commit para guardar los cambios en la base de datos
            mysql.connection.commit()

        # Mensaje de éxito
        flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))

    # Renderizamos la página de registro
    return render_template('register.html', tipo_cuenta=tipo_cuenta, tipo_empresa=tipo_empresa)


@app.route('/buscar', methods=['POST'])
@login_required
def buscar():
    query = request.form['query']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    usuario_id = current_user.id 
    cur.execute("SELECT * FROM usuarios WHERE nombre LIKE %s OR apellido LIKE %s", 
                ('%' + query + '%', '%' + query + '%'))
    resultados = cur.fetchall()
    
    if not resultados:
        flash('No se encontraron usuarios', 'info')
    
    return render_template('resultados_busqueda.html', resultados=resultados, user_id=usuario_id)

@app.route('/empresas/<tipo_empresa>', methods=['GET'])
def resultados_empresas(tipo_empresa):
    usuario_id = current_user.id 
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
        # Filtrar todas las empresas por el tipo (por ejemplo, Bodega, Hotel, Transporte)
        cur.execute("SELECT * FROM usuarios WHERE tipo_cuenta = 'empresa' AND tipo_empresa = %s", (tipo_empresa,))
        resultados = cur.fetchall()
    
    # Renderizamos el template de resultados y pasamos los datos
    return render_template('resultados_empresa.html', resultados=resultados, tipo_empresa=tipo_empresa, user_id=usuario_id)



@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario actual
    flash('Has cerrado sesión.', 'info')  # Mensaje de confirmación
    return redirect(url_for('login'))  # Redirige a la página de inicio de sesión

@app.route('/inicio')
@login_required

def inicio():
    
    usuario_id = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener los IDs de los amigos del usuario actual, tanto en usuario_id como en amigo_id
    cursor.execute("""
        SELECT amigo_id FROM relaciones 
        WHERE usuario_id = %s AND estado = 'amigo'
        UNION
        SELECT usuario_id FROM relaciones 
        WHERE amigo_id = %s AND estado = 'amigo'
    """, (usuario_id, usuario_id))
    amigos_ids = cursor.fetchall()
    amigos_ids = [amigo['amigo_id'] for amigo in amigos_ids]

    # Verificar que tenemos amigos (si no, no hay publicaciones que mostrar)
    if amigos_ids:
        # Obtener publicaciones de los amigos
        cursor.execute("""
            SELECT p.*, u.nombre, u.apellido 
            FROM publicaciones p 
            JOIN usuarios u ON p.usuario_id = u.id 
            WHERE u.id IN %s 
            ORDER BY p.fecha_publicacion DESC
        """, (tuple(amigos_ids),))
        publicaciones = cursor.fetchall()

        for publicacion in publicaciones:
            cursor.execute("""
                SELECT nombre_archivo FROM imagenes_publicacion 
                WHERE id_publicacion = %s
            """, (publicacion['id'],))
            imagen = cursor.fetchone()
            publicacion['imagen'] = imagen['nombre_archivo'] if imagen else None
    else:
        publicaciones = []

    # Obtener los IDs de las publicaciones guardadas por el usuario
    cursor.execute("""
        SELECT publicacion_id FROM guardados WHERE usuario_id = %s
    """, (usuario_id,))
    publicaciones_guardadas = {item['publicacion_id'] for item in cursor.fetchall()}

    cursor.close()

    return render_template('inicio.html', publicaciones=publicaciones, 
                           publicaciones_guardadas=publicaciones_guardadas, 
                           user_id=usuario_id)


@app.route('/guardados/<int:user_id>', methods=['GET', 'POST'])
@login_required
def guardados(user_id):
    # Verifica que el ID del usuario autenticado coincida con el user_id de la URL
    if current_user.id != user_id:
        flash('Acceso no autorizado.')
        return redirect(url_for('inicio'))
    usuario_id = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Procesar eliminación de publicaciones guardadas si es POST
    if request.method == 'POST':
        if 'eliminar_guardado' in request.form:
            publicacion_id = request.form['eliminar_guardado']
            cursor.execute("""
                DELETE FROM guardados 
                WHERE usuario_id = %s AND publicacion_id = %s
            """, (user_id, publicacion_id))
            mysql.connection.commit()
            flash('Publicación eliminada de guardados.')
    
    # Obtener las publicaciones guardadas por el usuario, ordenadas por fecha_guardado DESC
    cursor.execute("""
        SELECT p.*, u.nombre AS autor_nombre, u.apellido AS autor_apellido, g.fecha_guardado 
        FROM guardados g
        JOIN publicaciones p ON g.publicacion_id = p.id
        JOIN usuarios u ON p.usuario_id = u.id
        WHERE g.usuario_id = %s
        ORDER BY g.fecha_guardado DESC
    """, (user_id,))
    publicaciones_guardadas = cursor.fetchall()
    
    # Obtener la imagen asociada a cada publicación guardada
    for publicacion in publicaciones_guardadas:
        cursor.execute("""
            SELECT nombre_archivo FROM imagenes_publicacion 
            WHERE id_publicacion = %s
        """, (publicacion['id'],))
        imagen = cursor.fetchone()
        publicacion['imagen'] = imagen['nombre_archivo'] if imagen else None
    
    # Cerrar el cursor
    cursor.close()
    
    # Renderizar la plantilla 'guardados.html' con las publicaciones guardadas
    return render_template('guardados.html', publicaciones_guardadas=publicaciones_guardadas, user_id=user_id)

@app.route('/guardar_publicacion', methods=['POST'])
@login_required
def guardar_publicacion():
    # Obtener el ID del usuario autenticado
    usuario_id = current_user.id
    publicacion_id = request.form['publicacion_id']
    
    cursor = mysql.connection.cursor()

    # Verificar si la publicación ya está guardada
    cursor.execute("""
        SELECT * FROM guardados WHERE usuario_id = %s AND publicacion_id = %s
    """, (usuario_id, publicacion_id))
    guardado_existente = cursor.fetchone()

    if guardado_existente:
        flash('Esta publicación ya está guardada.')
    else:
        # Insertar la publicación en guardados
        cursor.execute("""
            INSERT INTO guardados (usuario_id, publicacion_id, fecha_guardado) 
            VALUES (%s, %s, NOW())
        """, (usuario_id, publicacion_id))
        mysql.connection.commit()
        flash('Publicación guardada exitosamente.')

    # Cerrar el cursor
    cursor.close()

    # Redirigir de nuevo a la página de inicio
    return redirect(request.referrer) 


@app.route("/")
def presentacion():
    return render_template("principal.html")


@app.route('/mensajes')
@login_required
def mensajes():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener el último mensaje por cada conversación
    cur.execute("""
        SELECT 
            CASE
                WHEN m.emisor_id = %s THEN m.receptor_id
                ELSE m.emisor_id
            END AS usuario_id,
            u.nombre, 
            u.apellido,
            m.contenido,
            m.fecha
        FROM 
            mensajes m
        JOIN 
            usuarios u ON (m.emisor_id = u.id OR m.receptor_id = u.id)
        WHERE 
            (m.emisor_id = %s OR m.receptor_id = %s)
        AND 
            u.id != %s  -- Asegúrate de no incluir al usuario actual
        ORDER BY 
            m.fecha DESC
    """, (current_user.id, current_user.id, current_user.id, current_user.id))

    # Obtener los resultados y agrupar por usuario_id para solo obtener el último mensaje
    mensajes = cur.fetchall()
    conversaciones = {}
    
    for mensaje in mensajes:
        usuario_id = mensaje['usuario_id']
        if usuario_id not in conversaciones:
            conversaciones[usuario_id] = {
                'nombre': mensaje['nombre'],
                'apellido': mensaje['apellido'],
                'contenido': mensaje['contenido'],
                'fecha': mensaje['fecha'],
                'usuario_id': usuario_id  # Guardamos el ID del usuario para el enlace
            }

    cur.close()
    
    # Convertir el diccionario a una lista para facilitar la renderización
    return render_template('mensajes.html', mensajes=conversaciones.values(), user_id=usuario_id)


@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    if request.method == 'POST':
        emisor_id = current_user.id  # ID del emisor desde la sesión actual
        receptor_id = request.form['receptor_id']
        contenido = request.form['contenido']

        # Crear el cursor
        cur = mysql.connection.cursor()
        # Insertar el mensaje en la base de datos
        cur.execute("INSERT INTO mensajes (emisor_id, receptor_id, contenido) VALUES (%s, %s, %s)", 
                    (emisor_id, receptor_id, contenido))
        # Confirmar los cambios
        mysql.connection.commit()
        cur.close()

        flash('Mensaje enviado correctamente!', 'success')
        # Redirigir a la página de chat
        return redirect(url_for('chat', receptor_id=receptor_id))
  # Redirige al chat con el receptor



@app.route('/chat/<int:receptor_id>', methods=['GET', 'POST'])
@login_required
def chat(receptor_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    usuario_id = current_user.id

    # Obtener el nombre del receptor
    cur.execute("SELECT nombre FROM usuarios WHERE id = %s", (receptor_id,))
    receptor = cur.fetchone()
    receptor_nombre = receptor['nombre'] if receptor else "Usuario desconocido"

    # Obtener los mensajes entre el usuario actual y el receptor
    cur.execute("""
        SELECT m.*, u1.nombre AS emisor_nombre, u2.nombre AS receptor_nombre
        FROM mensajes m
        JOIN usuarios u1 ON m.emisor_id = u1.id
        JOIN usuarios u2 ON m.receptor_id = u2.id
        WHERE (m.emisor_id = %s AND m.receptor_id = %s) OR (m.emisor_id = %s AND m.receptor_id = %s)
        ORDER BY m.fecha ASC
    """, (current_user.id, receptor_id, receptor_id, current_user.id))

    mensajes = cur.fetchall()
    cur.close()

    return render_template('chat.html', mensajes=mensajes, receptor_id=receptor_id, receptor_nombre=receptor_nombre, user_id=usuario_id)
# Función para validar las extensiones de los archivos de imagen (opcional)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/perfil/<int:usuario_id>')
@login_required
def perfil(usuario_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Obtener el perfil y las publicaciones
    cur.execute('SELECT * FROM perfiles WHERE usuario_id = %s', [usuario_id])
    perfil = cur.fetchone()
    
    cur.execute('SELECT * FROM usuarios WHERE id = %s', [usuario_id])
    usuario = cur.fetchone()

    usuario['nombre'] = usuario['nombre'].capitalize()
    usuario['apellido'] = usuario['apellido'].capitalize()

    # Obtener las publicaciones del perfil
    cur.execute('''SELECT p.*, i.nombre_archivo
                   FROM publicaciones p
                   LEFT JOIN imagenes_publicacion i ON p.id = i.id_publicacion
                   WHERE p.usuario_id = %s
                   ORDER BY p.fecha_publicacion DESC''', [usuario_id])
    publicaciones = cur.fetchall()
    if not publicaciones:
        publicaciones = []

    # Obtener las publicaciones guardadas por el usuario actual
    cur.execute('SELECT publicacion_id FROM guardados WHERE usuario_id = %s', [current_user.id])
    publicaciones_guardadas = {pub['publicacion_id'] for pub in cur.fetchall()}

    # Añadir un campo para indicar si la publicación está guardada
    for publicacion in publicaciones:
        publicacion['guardada'] = publicacion['id'] in publicaciones_guardadas

    # Lógica para determinar qué botones mostrar
    es_mi_perfil = (current_user.id == usuario_id)
    es_empresa = (usuario['tipo_cuenta'] == 'empresa')

    # Verificar el estado de la relación entre el usuario actual y el que se está viendo
    cur.execute('''SELECT estado FROM relaciones
                   WHERE (usuario_id = %s AND amigo_id = %s) OR (usuario_id = %s AND amigo_id = %s)''',
                [current_user.id, usuario_id, usuario_id, current_user.id])
    relacion = cur.fetchone()

    if relacion:
        relacion_estado = relacion['estado']
    else:
        relacion_estado = 'ninguna'

    # Aquí definimos qué opciones se mostrarán en el perfil
    if es_mi_perfil:
        # Mostrar opciones para el perfil del usuario autenticado
        return render_template('perfil_mi_perfil.html', usuario=usuario, perfil=perfil, publicaciones=publicaciones, 
                               relacion_estado=relacion_estado, user_id=usuario_id)
    elif es_empresa:
        # Mostrar opciones para un perfil de empresa
        return render_template('perfil_empresa.html', usuario=usuario, perfil=perfil, publicaciones=publicaciones, 
                               relacion_estado=relacion_estado, user_id=usuario_id)
    else:
        # Mostrar opciones para un perfil de otro usuario
        return render_template('perfil_otro_usuario.html', usuario=usuario, perfil=perfil, publicaciones=publicaciones, 
                               relacion_estado=relacion_estado, user_id=usuario_id)

@app.route('/add', methods=['POST'])
@login_required
def agregar():
    if request.method == 'POST':
        usuario_id = current_user.id  # Obtener el ID del usuario autenticado

        titulo_agregado = request.form['titulo_agregado']
        contenido_agregado = request.form['Contenido_agregado']
        
        imagen = request.files.get('imagen')  # Obtener la imagen si se sube

        # Guardar el nombre del archivo de la imagen
        imagen_filename = None
        if imagen and allowed_file(imagen.filename):
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

        # Insertar la publicación en la base de datos (con o sin imagen)
        cursor = mysql.connection.cursor()
        query = "INSERT INTO publicaciones (usuario_id, titulo, contenido) VALUES (%s, %s, %s)"
        cursor.execute(query, (usuario_id, titulo_agregado, contenido_agregado))
        mysql.connection.commit()

        # Recuperar el ID de la publicación recién insertada
        publicacion_id = cursor.lastrowid
        
        # Si se subió una imagen, insertarla en la tabla 'imagenes_publicacion'
        if imagen_filename:
            query_imagen = "INSERT INTO imagenes_publicacion (id_publicacion, nombre_archivo) VALUES (%s, %s)"
            cursor.execute(query_imagen, (publicacion_id, imagen_filename))
            mysql.connection.commit()

        cursor.close()

        return redirect(url_for('perfil', usuario_id=usuario_id))  # Usar el ID del usuario autenticado

@app.route('/editar/<int:publicacion_id>', methods=['GET', 'POST'])
@login_required
def editar_publicacion(publicacion_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        nuevo_titulo = request.form['titulo']
        nuevo_contenido = request.form['contenido']
        
        cursor.execute('UPDATE publicaciones SET titulo = %s, contenido = %s WHERE id = %s', 
                       (nuevo_titulo, nuevo_contenido, publicacion_id))
        mysql.connection.commit()
        
        flash('Publicación editada con éxito', 'success')
        return redirect(url_for('perfil', usuario_id=current_user.id))  # Usar el ID del usuario autenticado
    else:
        cursor.execute('SELECT * FROM publicaciones WHERE id = %s', [publicacion_id])
        publicacion = cursor.fetchone() 
        
        if publicacion:
            return render_template('editar_publicaciones.html', publicacion=publicacion)
        else:
            flash('Publicación no encontrada', 'error')
            return redirect(url_for('perfil', usuario_id=current_user.id))  # Usar el ID del usuario autenticado

@app.route('/eliminar/<int:publicacion_id>', methods=['GET'])
@login_required
def eliminar_publicacion(publicacion_id):
    cursor = mysql.connection.cursor()

    cursor.execute('DELETE FROM publicaciones WHERE id = %s', [publicacion_id])
    mysql.connection.commit()

    cursor.close()

    flash('Publicación eliminada con éxito', 'success')
    return redirect(url_for('perfil', usuario_id=current_user.id))  # Usar el ID del usuario autenticado

def obtener_amigos(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Consultar amigos aceptados
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido 
        FROM relaciones r
        JOIN usuarios u ON r.amigo_id = u.id
        WHERE r.usuario_id = %s AND r.estado = 'amigo'
    """, (user_id,))
    amigos = cursor.fetchall()

    # Consultar solicitudes pendientes
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido 
        FROM relaciones r
        JOIN usuarios u ON r.amigo_id = u.id
        WHERE r.usuario_id = %s AND r.estado = 'pendiente'
    """, (user_id,))
    solicitudes_pendientes = cursor.fetchall()

    cursor.close()

    # Retornar amigos y solicitudes pendientes como un diccionario
    return {
        'amigos': amigos,
        'solicitudes_pendientes': solicitudes_pendientes
    }



@app.route('/amigos/<int:user_id>', methods=['GET', 'POST'])
@login_required
def amigos(user_id):
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        # Manejo de solicitudes de amistad (aceptar/rechazar/eliminar)
        if 'aceptar_amigo' in request.form:
            amigo_id = request.form['aceptar_amigo']
            print(f"Aceptando solicitud de amistad con amigo_id: {amigo_id} para el usuario {user_id}")
            
            # Actualizar ambos registros de la relación a 'amigo' (aceptar)
            cursor.execute("""
                UPDATE relaciones 
                SET estado = 'amigo' 
                WHERE (usuario_id = %s AND amigo_id = %s) OR (usuario_id = %s AND amigo_id = %s)
            """, (user_id, amigo_id, amigo_id, user_id))
            
            # Commit para guardar los cambios
            mysql.connection.commit()

            # Verificar si se actualizó correctamente
            cursor.execute("""
                SELECT estado 
                FROM relaciones 
                WHERE (usuario_id = %s AND amigo_id = %s) OR (usuario_id = %s AND amigo_id = %s)
            """, (user_id, amigo_id, amigo_id, user_id))
            estado = cursor.fetchone()
            print(f"Nuevo estado de la relación: {estado}")

            flash('Solicitud de amistad aceptada.')
        
        elif 'rechazar_amigo' in request.form:
            amigo_id = request.form['rechazar_amigo']
            cursor.execute("DELETE FROM relaciones WHERE usuario_id = %s AND amigo_id = %s", (user_id, amigo_id))
            mysql.connection.commit()
            flash('Solicitud de amistad rechazada.')

        elif 'eliminar_amigo' in request.form:
            amigo_id = request.form['eliminar_amigo']
            cursor.execute("DELETE FROM relaciones WHERE (usuario_id = %s AND amigo_id = %s) OR (usuario_id = %s AND amigo_id = %s)", (user_id, amigo_id, amigo_id, user_id))
            mysql.connection.commit()
            flash('Amigo eliminado.')

    # Obtener solicitudes pendientes
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido 
        FROM relaciones r 
        JOIN usuarios u ON r.usuario_id = u.id 
        WHERE r.amigo_id = %s AND r.estado = 'pendiente'
    """, (user_id,))
    solicitudes_pendientes = cursor.fetchall()

    # Obtener amigos confirmados (modificado)
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido 
        FROM relaciones r 
        JOIN usuarios u ON (r.amigo_id = u.id AND r.usuario_id = %s OR r.usuario_id = u.id AND r.amigo_id = %s)
        WHERE r.estado = 'amigo'
        ORDER BY u.nombre, u.apellido 
                   
    """, (user_id, user_id))
    amigos_confirmados = cursor.fetchall()

    cursor.close()
    
    return render_template('amigos.html', user_id=user_id, 
                           solicitudes_pendientes=solicitudes_pendientes, 
                           amigos_confirmados=amigos_confirmados)



@app.route('/enviar_solicitud_amigo/<int:usuario_id>', methods=['POST'])
@login_required
def enviar_solicitud_amigo(usuario_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Obtener el tipo de cuenta del usuario que está siendo agregado como amigo
    cursor.execute("SELECT tipo_cuenta FROM usuarios WHERE id = %s", (usuario_id,))
    amigo = cursor.fetchone()

    if not amigo:
        flash('El usuario no existe.', 'error')
        cursor.close()
        return redirect(request.referrer)  # Redirige al usuario a la página anterior

    # Verificar si ya existe una relación
    cursor.execute("SELECT * FROM relaciones WHERE usuario_id = %s AND amigo_id = %s", (current_user.id, usuario_id))
    amistad_existente = cursor.fetchone()

    if amistad_existente:
        if amistad_existente['estado'] == 'pendiente':
            flash('Ya has enviado una solicitud de amistad a este usuario.', 'info')
        elif amistad_existente['estado'] == 'amigo':
            flash('Ya eres amigo de este usuario.', 'info')
    else:
        # Si es una cuenta de empresa, directamente se marca como amigo
        estado = 'amigo' if amigo['tipo_cuenta'] == 'empresa' else 'pendiente'
        
        cursor.execute("INSERT INTO relaciones (usuario_id, amigo_id, estado) VALUES (%s, %s, %s)", 
                       (current_user.id, usuario_id, estado))
        mysql.connection.commit()

        if estado == 'amigo':
            flash('Ahora sigues a esta empresa.', 'success')
        else:
            flash('Solicitud de amistad enviada exitosamente!', 'success')

    cursor.close()

    # Redirigir al usuario a la página anterior (o a la página de resultados de búsqueda si venía de allí)
    return redirect(request.referrer)  # Redirigir siempre a la página de origen


# Código para "Dejar de seguir" en el perfil de otro usuario
@app.route('/dejar_de_seguir/<int:usuario_id>', methods=['POST'])
@login_required
def dejar_de_seguir(usuario_id):
    cursor = mysql.connection.cursor()

    # Eliminar o cambiar el estado de la relación en la base de datos
    cursor.execute('DELETE FROM relaciones WHERE (usuario_id = %s AND amigo_id = %s) OR (usuario_id = %s AND amigo_id = %s)', (current_user.id, usuario_id, usuario_id, current_user.id))
    mysql.connection.commit()
    flash("Has dejado de seguir a este usuario.")

    cursor.close()
    return redirect(url_for('perfil', usuario_id=usuario_id))  # Redirigir al perfil

@app.route('/grupos', methods=['GET', 'POST'])
@login_required
def grupos():
    cursor = mysql.connection.cursor()
    usuario_id = current_user.id 
    if request.method == 'POST':
        # Lógica para crear un nuevo grupo
        if 'crear_grupo' in request.form:
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            foto = request.files.get('foto')  # Obtener la foto

            # Guardar el nombre del archivo de la foto de perfil
            foto_filename = None
            if foto and allowed_file(foto.filename):  # Verifica si el archivo es válido
                foto_filename = secure_filename(foto.filename)
                # Guardar la foto en el directorio adecuado
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

            # Insertar los datos del grupo en la base de datos
            cursor.execute("""
                INSERT INTO grupos (nombre, descripcion, creador_id, foto_perfil)
                VALUES (%s, %s, %s, %s)
            """, (nombre, descripcion, current_user.id, foto_filename))
            mysql.connection.commit()
            flash('Grupo creado exitosamente.', 'success')

    # Obtener los grupos creados por el usuario
    cursor.execute("""
        SELECT id, nombre, descripcion, foto_perfil FROM grupos WHERE creador_id = %s
    """, (current_user.id,))
    mis_grupos = cursor.fetchall()

    # Obtener los grupos donde el usuario es miembro
    cursor.execute("""
        SELECT g.id, g.nombre, g.descripcion, g.foto_perfil 
        FROM grupos g
        INNER JOIN miembros_grupo m ON g.id = m.grupo_id
        WHERE m.usuario_id = %s
    """, (current_user.id,))
    grupos_unidos = cursor.fetchall()

    cursor.close()

    return render_template('grupos.html', mis_grupos=mis_grupos, grupos_unidos=grupos_unidos, user_id=usuario_id)



@app.route('/unirse_grupo/<int:grupo_id>', methods=['POST'])
@login_required
def unirse_grupo(grupo_id):
    cursor = mysql.connection.cursor()

    # Comprobar si el usuario ya es miembro del grupo
    cursor.execute("""
        SELECT * FROM miembros_grupo WHERE grupo_id = %s AND usuario_id = %s
    """, (grupo_id, current_user.id))
    miembro_existente = cursor.fetchone()

    if miembro_existente:
        flash('Ya eres miembro de este grupo.', 'warning')
    else:
        # Agregar al usuario al grupo
        cursor.execute("""
            INSERT INTO miembros_grupo (grupo_id, usuario_id) 
            VALUES (%s, %s)
        """, (grupo_id, current_user.id))
        mysql.connection.commit()
        flash('Te has unido al grupo.', 'success')

    cursor.close()
    return redirect(url_for('ver_grupo', grupo_id=grupo_id))


@app.route('/grupo/<int:grupo_id>', methods=['GET', 'POST'])
@login_required
def ver_grupo(grupo_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Usa DictCursor
    usuario_id = current_user.id 
    # Obtener información del grupo
    cursor.execute("SELECT * FROM grupos WHERE id = %s", (grupo_id,))
    grupo = cursor.fetchone()

    if not grupo:
        return redirect(url_for('grupos'))  # Si no se encuentra el grupo, redirigir

    # Obtener detalles del creador del grupo
    cursor.execute("""
        SELECT nombre, apellido FROM usuarios WHERE id = %s
    """, (grupo['creador_id'],))
    creador = cursor.fetchone()

    # Obtener miembros del grupo
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido, u.email 
        FROM usuarios u
        INNER JOIN miembros_grupo m ON u.id = m.usuario_id
        WHERE m.grupo_id = %s
    """, (grupo_id,))
    miembros = cursor.fetchall()

    # Verificar si el usuario ya es miembro del grupo
    cursor.execute("""
        SELECT * FROM miembros_grupo WHERE grupo_id = %s AND usuario_id = %s
    """, (grupo_id, current_user.id))
    es_miembro = cursor.fetchone() is not None

    # Verificar si el usuario es el propietario del grupo
    es_dueño = grupo['creador_id'] == current_user.id  # Asumiendo que 'creador_id' es el campo que indica al dueño del grupo

    if request.method == 'POST':
        # Si el usuario no es miembro y no es dueño, se puede unir
        if not es_miembro and not es_dueño:
            cursor.execute("INSERT INTO miembros_grupo (grupo_id, usuario_id) VALUES (%s, %s)", (grupo_id, current_user.id))
            mysql.connection.commit()
            return redirect(url_for('ver_grupo', grupo_id=grupo_id, user_id=usuario_id))  # Redirigir para actualizar la página

        # Si el usuario es miembro, se puede salir del grupo
        if es_miembro:
            cursor.execute("DELETE FROM miembros_grupo WHERE grupo_id = %s AND usuario_id = %s", (grupo_id, current_user.id))
            mysql.connection.commit()
            return redirect(url_for('ver_grupo', grupo_id=grupo_id, user_id=usuario_id))  # Redirigir para actualizar la página

    cursor.close()

    return render_template(
        'ver_grupo.html',
        grupo=grupo,
        miembros=miembros,
        creador=creador,  # Agregamos los detalles del creador
        es_miembro=es_miembro,
        es_dueño=es_dueño
          # Pasamos también si es dueño del grupo
    )


@app.route('/salir_grupo/<int:grupo_id>', methods=['POST'])
@login_required
def salir_grupo(grupo_id):
    cursor = mysql.connection.cursor()

    # Verificar si el usuario es miembro del grupo
    cursor.execute("""
        SELECT * FROM miembros_grupo WHERE grupo_id = %s AND usuario_id = %s
    """, (grupo_id, current_user.id))
    miembro = cursor.fetchone()

    if miembro:
        # Eliminar al usuario del grupo
        cursor.execute("""
            DELETE FROM miembros_grupo WHERE grupo_id = %s AND usuario_id = %s
        """, (grupo_id, current_user.id))
        mysql.connection.commit()
        flash('Has salido del grupo.', 'success')
    else:
        flash('No eres miembro de este grupo.', 'danger')

    cursor.close()
    return redirect(url_for('ver_grupo', grupo_id=grupo_id))

@app.route('/eliminar_grupo/<int:grupo_id>', methods=['POST'])
@login_required
def eliminar_grupo(grupo_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Asegurarse de usar DictCursor

    # Verificar que el usuario es el creador del grupo
    cursor.execute("""
        SELECT creador_id FROM grupos WHERE id = %s
    """, (grupo_id,))
    grupo = cursor.fetchone()  # Debería devolver un diccionario, no una tupla

    if grupo and grupo['creador_id'] == current_user.id:
        # Eliminar miembros del grupo
        cursor.execute("""
            DELETE FROM miembros_grupo WHERE grupo_id = %s
        """, (grupo_id,))
        
        # Eliminar el grupo
        cursor.execute("""
            DELETE FROM grupos WHERE id = %s
        """, (grupo_id,))
        mysql.connection.commit()
        flash('Grupo eliminado.', 'success')
    else:
        flash('No tienes permisos para eliminar este grupo.', 'danger')

    cursor.close()
    return redirect(url_for('grupos'))


@app.route('/buscar_grupos', methods=['GET'])
@login_required
def buscar_grupos():
    query = request.args.get('query', '').strip()  # Toma la consulta de búsqueda del usuario
    cursor = mysql.connection.cursor()

    # Realiza la búsqueda solo si hay una consulta
    if query:
        cursor.execute("""
            SELECT id, nombre, descripcion, foto_perfil
            FROM grupos
            WHERE nombre LIKE %s OR descripcion LIKE %s
        """, (f"%{query}%", f"%{query}%"))
        resultados_busqueda = cursor.fetchall()
    else:
        resultados_busqueda = []

    # Obtener siempre los grupos creados por el usuario
    cursor.execute("""
        SELECT id, nombre, descripcion, foto_perfil
        FROM grupos
        WHERE creador_id = %s
    """, (current_user.id,))
    mis_grupos = cursor.fetchall()

    # Obtener siempre los grupos a los que el usuario se ha unido
    cursor.execute("""
        SELECT g.id, g.nombre, g.descripcion, g.foto_perfil
        FROM grupos g
        INNER JOIN miembros_grupo m ON g.id = m.grupo_id
        WHERE m.usuario_id = %s
    """, (current_user.id,))
    grupos_unidos = cursor.fetchall()

    cursor.close()

    # Renderiza la plantilla con todos los datos
    return render_template('grupos.html', query=query, resultados_busqueda=resultados_busqueda, mis_grupos=mis_grupos, grupos_unidos=grupos_unidos)

@app.route('/grupo/<int:grupo_id>/chat', methods=['GET', 'POST'])
@login_required
def ver_chat(grupo_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Usa DictCursor

    # Obtener información del grupo
    cursor.execute("SELECT * FROM grupos WHERE id = %s", (grupo_id,))
    grupo = cursor.fetchone()

    if not grupo:
        return redirect(url_for('grupos'))  # Si no se encuentra el grupo, redirigir

    # Obtener los mensajes del grupo
    cursor.execute("""
        SELECT m.mensaje, m.fecha_envio, u.nombre AS emisor_nombre, u.apellido AS emisor_apellido
        FROM mensajes_grupo m
        INNER JOIN usuarios u ON m.usuario_id = u.id
        WHERE m.grupo_id = %s
        ORDER BY m.fecha_envio
    """, (grupo_id,))
    mensajes = cursor.fetchall()

    if request.method == 'POST':
        # Obtener el mensaje y el usuario
        contenido = request.form['contenido']
        cursor.execute("""
            INSERT INTO mensajes_grupo (grupo_id, usuario_id, mensaje)
            VALUES (%s, %s, %s)
        """, (grupo_id, current_user.id, contenido))
        mysql.connection.commit()

        # Redirigir al mismo chat después de enviar el mensaje
        return redirect(url_for('ver_chat', grupo_id=grupo_id))

    cursor.close()

    return render_template(
        'ver_chat.html',
        grupo=grupo,
        mensajes=mensajes,
    )

@app.route('/eventos', methods=['GET', 'POST'])
@login_required
def eventos():
    usuario_id = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Buscador de eventos: Si se envió una búsqueda
    busqueda = request.args.get('buscar')  # Obtiene lo que el usuario ingrese en el buscador
    if busqueda:
        cursor.execute("""
            SELECT e.*, u.nombre AS organizador_nombre, u.apellido AS organizador_apellido
            FROM eventos e
            JOIN usuarios u ON e.organizador_id = u.id  
            WHERE e.nombre LIKE %s OR e.ubicacion_corta LIKE %s
            ORDER BY e.fecha DESC
        """, (f"%{busqueda}%", f"%{busqueda}%"))
    else:
        # Obtener todos los eventos si no hay búsqueda
        cursor.execute("""
            SELECT e.*, u.nombre AS organizador_nombre, u.apellido AS organizador_apellido
            FROM eventos e
            JOIN usuarios u ON e.organizador_id = u.id 
            ORDER BY e.fecha DESC
        """)
    
    eventos = cursor.fetchall()
    
    cursor.close()

    return render_template('eventos.html', eventos=eventos, user_id=usuario_id)


@app.route('/evento/<int:evento_id>')
@login_required
def evento_detalle(evento_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Obtener los detalles del evento
    cursor.execute("""
        SELECT e.*, u.nombre AS organizador_nombre, u.apellido AS organizador_apellido
        FROM eventos e
        JOIN usuarios u ON e.organizador_id = u.id 
        WHERE e.id = %s
    """, (evento_id,))
    evento = cursor.fetchone()

    # Si no se encuentra el evento, redirigir a eventos
    if not evento:
        flash('Evento no encontrado', 'danger')
        return redirect(url_for('eventos'))
    
    # Obtener la ubicación completa
    ubicacion_completa = evento['ubicacion_completa']
    
    cursor.close()

    return render_template('evento_detalle.html', evento=evento, ubicacion_completa=ubicacion_completa)


@app.route('/crear_evento', methods=['GET', 'POST'])
@login_required
def crear_evento():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        ubicacion_corta = request.form['ubicacion_corta']
        ubicacion_completa = request.form['ubicacion_completa']
        descripcion_detallada = request.form['descripcion_detallada']
        leve_descripcion = request.form['leve_descripcion']
        duracion = request.form['duracion']
        precio = request.form['precio'].strip()  # Eliminar espacios extra al principio y final
        imagen = request.files['imagen']
        
        # Determinar si el evento es gratuito o tiene precio
        if precio == '0':  # Si el precio es 0, lo consideramos como gratuito
            precio_valido = 0.00  # Usamos DECIMAL con dos decimales
            es_gratuito = True
        else:
            try:
                # Intentar convertir el precio a un número decimal
                precio_valido = float(precio)
                es_gratuito = False
            except ValueError:
                # Si el valor no es válido (no es un número), asignar 0 y marcar como gratuito
                precio_valido = 0.00
                es_gratuito = True

        # Guardar la imagen si existe
        if imagen:
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
        else:
            imagen_filename = None
        
        # Insertar los datos del evento en la base de datos, usando el nombre correcto para la clave foránea
        cursor = mysql.connection.cursor()
        cursor.execute("""
    INSERT INTO eventos (nombre, fecha, ubicacion_corta, ubicacion_completa, descripcion_detallada, leve_descripcion, duracion, precio, imagen, organizador_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (nombre, fecha, ubicacion_corta, ubicacion_completa, descripcion_detallada, leve_descripcion, duracion, precio_valido, imagen_filename, current_user.id))

        mysql.connection.commit()
        cursor.close()
        
        # Redirigir a la página de eventos
        return redirect('/eventos')
    
    # Si el método es GET, renderizamos el formulario de creación
    return render_template('crear_evento.html')

# Ruta para mostrar los productos disponibles en la tienda
@app.route('/tienda')
@login_required
def tienda():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    usuario_id = current_user.id 
    
    # Obtener todos los productos disponibles
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    
    cursor.close()
    
    return render_template('tienda.html', productos=productos, user_id=usuario_id)

# Ruta para buscar productos
@app.route('/buscar_producto', methods=['GET'])
@login_required
def buscar_producto():
    query = request.args.get('query', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Buscar productos cuyo nombre o descripción coincida parcialmente con la consulta
    cursor.execute("""
        SELECT * FROM productos 
        WHERE nombre LIKE %s OR descripcion LIKE %s
    """, (f"%{query}%", f"%{query}%"))
    productos = cursor.fetchall()
    
    cursor.close()
    
    return render_template('tienda.html', productos=productos)

# Ruta para añadir un producto al carrito

@app.route('/añadir_carrito', methods=['POST'])
@login_required
def añadir_carrito():
    producto_id = request.form.get('producto_id')
    cantidad = int(request.form.get('cantidad', 1))
    usuario_id = current_user.id
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Verificar si el producto ya está en el carrito
    cursor.execute("""
        SELECT * FROM carrito 
        WHERE id_usuario = %s AND id_producto = %s
    """, (usuario_id, producto_id))
    producto_en_carrito = cursor.fetchone()
    
    if producto_en_carrito:
        # Actualizar cantidad si el producto ya está en el carrito
        nueva_cantidad = producto_en_carrito['cantidad'] + cantidad
        cursor.execute("""
            UPDATE carrito 
            SET cantidad = %s 
            WHERE id_usuario = %s AND id_producto = %s
        """, (nueva_cantidad, usuario_id, producto_id))
    else:
        # Insertar el producto en el carrito si no está
        cursor.execute("""
            INSERT INTO carrito (id_usuario, id_producto, cantidad) 
            VALUES (%s, %s, %s)
        """, (usuario_id, producto_id, cantidad))
    
    mysql.connection.commit()

    # Obtener el carrito actualizado
    cursor.execute("""
        SELECT c.*, p.nombre, p.precio, p.imagen 
        FROM carrito c 
        JOIN productos p ON c.id_producto = p.id 
        WHERE c.id_usuario = %s
    """, (usuario_id,))
    carrito = cursor.fetchall()
    
    # Calcular el total
    total = sum(item['cantidad'] * item['precio'] for item in carrito)

    cursor.close()

    # Enviar el carrito y total como respuesta JSON
    return jsonify({'carrito': carrito, 'total': total})


# Ruta para mostrar los productos del carrito
@app.route('/ver_carrito')
@login_required
def ver_carrito():
    usuario_id = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Obtener los productos del carrito del usuario
    cursor.execute("""
        SELECT c.*, p.nombre, p.precio, p.imagen 
        FROM carrito c 
        JOIN productos p ON c.id_producto = p.id 
        WHERE c.id_usuario = %s
    """, (usuario_id,))
    carrito = cursor.fetchall()
    
    # Calcular el total
    total = sum(item['cantidad'] * item['precio'] for item in carrito)
    
    cursor.close()
    
    return jsonify({'carrito': carrito, 'total': total})

@app.route('/remover_carrito/<int:producto_id>', methods=['POST'])
@login_required
def remover_carrito(producto_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Eliminar el producto del carrito usando solo el id
    cursor.execute("DELETE FROM carrito WHERE id = %s", (producto_id,))
    
    if cursor.rowcount > 0:
        # Si se eliminó el producto, actualizar el carrito
        cursor.execute("""
            SELECT c.*, p.nombre, p.precio, p.imagen 
            FROM carrito c 
            JOIN productos p ON c.id_producto = p.id 
            WHERE c.id_usuario = %s
        """, (current_user.id,))
        carrito = cursor.fetchall()

        total = sum(item['cantidad'] * item['precio'] for item in carrito)

        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'carrito': carrito, 'total': total})
    else:
        cursor.close()
        return jsonify({'success': False, 'message': 'No se pudo eliminar el producto'})

# Ruta para procesar la facturación

@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    usuario_id = current_user.id
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Verificar si la carpeta 'facturas' existe en 'static'
    factura_dir = os.path.join(os.getcwd(), 'static', 'facturas')  # Ruta absoluta
    print(f"Ruta completa del directorio de facturas: {factura_dir}")  # Depuración
    
    if not os.path.exists(factura_dir):
        print("La carpeta 'facturas' no existe. Creándola...")
        os.makedirs(factura_dir)  # Si no existe, la crea
    else:
        print("La carpeta 'facturas' ya existe.")
    
    if request.method == 'POST':
        # Recoger los datos de facturación
        nombre = request.form.get('nombre')
        dni = request.form.get('dni')
        ubicacion = request.form.get('ubicacion')
        metodo_pago = request.form.get('metodo_pago')
        
        # Obtener los productos del carrito
        cursor.execute("""
            SELECT c.*, p.nombre, p.precio, p.imagen
            FROM carrito c 
            JOIN productos p ON c.id_producto = p.id 
            WHERE c.id_usuario = %s
        """, (usuario_id,))
        carrito = cursor.fetchall()
        
        # Calcular el total
        total = sum(item['cantidad'] * item['precio'] for item in carrito)
        
        # Crear la factura
        cursor.execute("""
            INSERT INTO factura (id_usuario, dni, direccion_envio, metodo_pago, total) 
            VALUES (%s, %s, %s, %s, %s)
        """, (usuario_id, dni, ubicacion, metodo_pago, total))
        factura_id = cursor.lastrowid
        
        # Insertar los detalles de la factura
        for item in carrito:
            cursor.execute("""
                INSERT INTO detalle_factura (id_factura, id_producto, cantidad, subtotal) 
                VALUES (%s, %s, %s, %s)
            """, (factura_id, item['id_producto'], item['cantidad'], item['cantidad'] * item['precio']))
        
        # Vaciar el carrito
        cursor.execute("DELETE FROM carrito WHERE id_usuario = %s", (usuario_id,))
        
        mysql.connection.commit()
        cursor.close()

        # Generar la ruta completa para el archivo PDF
        pdf_path = os.path.join(factura_dir, f"factura_{factura_id}.pdf")
        print(f"Generando PDF en: {pdf_path}")  # Depuración
        
        # Generar el PDF de la factura
        generate_pdf(pdf_path, nombre, dni, ubicacion, metodo_pago, carrito, total)
        
        # Redirigir a la tienda con un archivo temporal para descarga
        return redirect(url_for('descargar_factura', factura_id=factura_id))
    
    # Si es GET, mostrar el formulario de facturación
    cursor.execute("""
        SELECT c.*, p.nombre, p.precio, p.imagen 
        FROM carrito c 
        JOIN productos p ON c.id_producto = p.id 
        WHERE c.id_usuario = %s
    """, (usuario_id,))
    carrito = cursor.fetchall()
    
    total = sum(item['cantidad'] * item['precio'] for item in carrito)
    cursor.close()
    
    return render_template('facturacion.html', carrito=carrito, total=total, user_id=usuario_id)

@app.route('/descargar_factura/<int:factura_id>', methods=['GET'])
@login_required
def descargar_factura(factura_id):
    # Obtener la ruta del archivo PDF generado
    factura_dir = os.path.join(os.getcwd(), 'static', 'facturas')  # Ruta absoluta
    pdf_path = os.path.join(factura_dir, f"factura_{factura_id}.pdf")
    
    # Enviar el archivo para su descarga
    return send_file(pdf_path, as_attachment=True)
      # Redirigir a la tienda después de la descarga

# Función para generar el PDF
def generate_pdf(pdf_path, nombre, dni, ubicacion, metodo_pago, carrito, total):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Información de la factura
    c.drawString(100, 750, f"Factura para: {nombre}")
    c.drawString(100, 735, f"DNI: {dni}")
    c.drawString(100, 720, f"Ubicación: {ubicacion}")
    c.drawString(100, 705, f"Método de pago: {metodo_pago}")
    
    c.drawString(100, 675, "Productos Comprados:")
    y_position = 660
    
    for item in carrito:
        c.drawString(100, y_position, f"{item['nombre']} - Cantidad: {item['cantidad']} - Subtotal: ${item['cantidad'] * item['precio']}")
        y_position -= 15
    
    c.drawString(100, y_position, f"Total: ${total}")
    
    c.save()


@app.route('/subir_producto', methods=['GET', 'POST'])
@login_required
def subir_producto():
    if request.method == 'POST':
        usuario_id = current_user.id  # Obtener el ID del usuario autenticado

        # Obtener los campos del formulario
        nombre_producto = request.form['nombre']
        descripcion_producto = request.form['descripcion']
        precio_producto = request.form['precio']
        
        imagen = request.files.get('imagen')  # Obtener la imagen si se sube

        # Guardar el nombre del archivo de la imagen
        imagen_filename = None
        if imagen and allowed_file(imagen.filename):
            imagen_filename = imagen.filename  # Sin usar `secure_filename`
            # Guardar la imagen en el directorio especificado
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))  # Usar app.config['UPLOAD_FOLDER']

        # Insertar el producto en la base de datos
        cursor = mysql.connection.cursor()
        query = "INSERT INTO productos (nombre, descripcion, precio, imagen, id_vendedor) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nombre_producto, descripcion_producto, precio_producto, imagen_filename, usuario_id))
        mysql.connection.commit()

        cursor.close()

        flash("Producto subido con éxito", "success")
        return redirect(url_for('tienda'))  # Redirigir al usuario a la tienda o donde lo desees

    # Si es un GET request, simplemente renderiza el formulario para subir el producto
    return render_template('subir_producto.html')

@app.route('/paquetes')
def paquetes():
    cursor = mysql.connection.cursor()
    usuario_id = current_user.id 
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, b.nombre AS bodega, b.descripcion AS bodega_desc, b.ubicacion AS bodega_ubicacion, 
               t.nombre AS transporte, h.nombre AS hotel, p.imagen
        FROM paquetes_turisticos p
        LEFT JOIN bodegas b ON p.bodega_id = b.id
        LEFT JOIN empresas_transporte t ON p.transporte_id = t.id
        LEFT JOIN hoteles h ON p.hotel_id = h.id
    """)
    paquetes = cursor.fetchall()
    cursor.close()
    
    # Convertimos los resultados en un diccionario para usarlos en el template
    paquetes = [{'id': p[0], 'nombre': p[1], 'descripcion': p[2], 'precio': p[3], 'bodega': p[4], 'bodega_desc': p[5], 
                 'bodega_ubicacion': p[6], 'transporte': p[7], 'hotel': p[8], 'imagen': p[9]} for p in paquetes]
    
    return render_template("paquetes.html", paquetes=paquetes, user_id=usuario_id)


@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    if 'imagen' not in request.files:
        return 'No file part', 400
    file = request.files['imagen']

    
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Aquí puedes actualizar la base de datos con el nombre de la imagen
        paquete_id = request.form['paquete_id']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE paquetes_turisticos SET imagen = %s WHERE id = %s", (filename, paquete_id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('paquetes'))



# Ruta para procesar la reserva
@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form['nombre']
    email = request.form['email']
    fecha = request.form['fecha']
    personas = request.form['personas']
    paquete_id = request.form.get('paquete_id')

    # Conectar a la base de datos
    cursor = mysql.connection.cursor()

    # Verificar si el paquete_id existe en la base de datos
    cursor.execute("SELECT id FROM paquetes_turisticos WHERE id = %s", (paquete_id,))
    paquete = cursor.fetchone()  # Si existe, devuelve el paquete, si no, devuelve None

    if paquete:
        # Si el paquete existe, proceder con la inserción
        cursor.execute("""
            INSERT INTO reservas (nombre, email, fecha, personas, paquete_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, email, fecha, personas, paquete_id))
        mysql.connection.commit()
        cursor.close()

        # Redirigir al usuario a la página de paquetes con una confirmación o mensaje
        return redirect(url_for('paquetes'))
    else:
        # Si el paquete no existe, mostrar un error
        cursor.close()
        return "Error: El paquete seleccionado no existe. Por favor, selecciona un paquete válido.", 400

if __name__ == '__main__':
    app.run(port=3000, debug=True)
