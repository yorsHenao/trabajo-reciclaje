from conexion_bd.conexion import crear_conexion

def consultar_puntos():
    try:
        conexion = crear_conexion()
        if conexion.is_connected():
            cursor = conexion.cursor()
            cedula =input("Ingresa tu cedula para consultar puntos: ")

            consulta = "SELECT SUM(p.puntos) FROM puntos p JOIN usuarios u ON p.usuario_id = u.usuario_id WHERE u.cedula = %s"
            cursor.execute(consulta, (cedula,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] is not None:
                print(f"Tienes acumulados {resultado[0]} puntos")
            else:
                print("No se encontraron puntos o el cedula no esta registrado")

    except Exception as e:
        print(f"Error al consultar puntos: {e}")


    finally:

        if conexion is not None and conexion.is_connected():
            if 'cursor' in locals():
                cursor.close()
            conexion.close()
            print("Conexión cerrada")