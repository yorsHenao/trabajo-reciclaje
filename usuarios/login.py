from conexion_bd.conexion import crear_conexion


def login_usuario():
    cedula = input("Ingresa tu número de cédula: ")
    conexion = crear_conexion()
    cursor = conexion.cursor()

    consulta = "SELECT nombre FROM usuarios WHERE cedula = %s"
    cursor.execute(consulta, (cedula,))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        print("\nInicio de sesión exitoso.\n")
        return resultado[0]
    else:
        print("Usuario no encontrado.")
        return None
