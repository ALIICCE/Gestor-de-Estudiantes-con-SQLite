import sqlite3

# Conexión y creación de tabla

conn = sqlite3.connect("alumnos.db")

cursor = conn.cursor()



cursor.execute("""

CREATE TABLE IF NOT EXISTS estudiantes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    edad INTEGER,

    correo TEXT

)

""")

conn.commit()



# Funciones principales

def agregar_estudiante(nombre, edad, correo):
    # Validar edad mínima
    if edad < 17:
        print("La edad mínima para registrarse es 17 años.")
        return

    # Validar correo electrónico
    mensaje_error = ""

    def validador(cadena, validador):
        resultado = cadena.split(validador)
        if len(resultado) > 1:
            return True
        nonlocal mensaje_error
        mensaje_error = f"Error de validación: falta '{validador}'"
        return False

    def valida_nombre_correo(cadena):
        separado = cadena.split('@')
        if len(separado[0]) < 4:
            nonlocal mensaje_error
            mensaje_error = "Error de nombre: muy corto"
            return False
        return True

    def valida_dominio(cadena):
        separado = cadena.split('@')
        if len(separado) < 2:
            global mensaje_error
            mensaje_error = "Error: falta el dominio"
            return False
        dominio = separado[1]
        if '..' in dominio:
            mensaje_error = "Error de dominio: contiene puntos consecutivos"
            return False
        partes_dominio = dominio.split('.')
        if len(partes_dominio) < 2:
            mensaje_error = "Error de dominio: incompleto"
            return False
        return True


    def validar_correo(correo):
        nonlocal mensaje_error
        mensaje_error = ""
        if correo.count('@') != 1:
            mensaje_error = "Error: el correo debe tener exactamente un '@'"
            return False

        arroba = validador(correo, '@')
        punto = validador(correo, '.')
        nombre = valida_nombre_correo(correo)
        dominio = valida_dominio(correo)

        if arroba and punto and nombre and dominio:
            return True
        else:
            return False

    if not validar_correo(correo):
        print(mensaje_error)
        return

    # Insertar en la base de datos
    cursor.execute("INSERT INTO estudiantes (nombre, edad, correo) VALUES (?, ?, ?)", (nombre, edad, correo))
    conn.commit()
    print("Estudiante agregado correctamente.")


def mostrar_estudiantes():

    cursor.execute("SELECT * FROM estudiantes")

    filas = cursor.fetchall()

    for fila in filas:

        print(fila)



def buscar_por_nombre(nombre):
    cursor.execute("SELECT nombre, edad, correo FROM estudiantes WHERE nombre LIKE ?", ('%' + nombre + '%',))
    resultados = cursor.fetchall()
    if resultados:
        print("\nResultados encontrados:")
        for estudiante in resultados:
            print(f"Nombre: {estudiante[0]}, Edad: {estudiante[1]}, Correo: {estudiante[2]}")
    else:
        print("No se encontraron estudiantes con ese nombre.")


# Menú principal

while True:

    print("\n1. Agregar estudiante\n2. Mostrar todos\n3. Buscar por nombre\n4. Salir")

    op = input("Elige una opción: ")



    if op == '1':

        nombre = input("Nombre: ")

        try:

            edad = int(input("Edad: "))

        except ValueError:

            print("Edad inválida.")

            continue

        correo = input("Correo: ")

        agregar_estudiante(nombre, edad, correo)

    elif op == '2':

        mostrar_estudiantes()

    elif op == '3':

        nombre = input("Nombre a buscar: ")

        buscar_por_nombre(nombre)

    elif op == '4':

        break

    else:

        print("Opción no válida.")



# Cierre de conexión

conn.close()

