from conexion_bd.conexion import crear_conexion

def consultar_historial():
    try:
        conexion = crear_conexion()
        if conexion.is_connected():
            cursor = conexion.cursor()

            cedula = input("Ingresa tu cedula, para ver el tú historial de reciclaje: ")

            #Consultar el ID del usuario

            consulta_usuario = "SELECT usuario_id FROM usuarios WHERE cedula = %s"
            cursor.execute(consulta_usuario, (cedula,))
            usuario = cursor.fetchone()

        if usuario is None:
            print("El cedula no esta registrado. ")
            return

        usuario_id = usuario[0]

        #consultar historial
        consulta_historial = (
            "SELECT u.nombre, r.material, r.cantidad, r.fecha "
            "FROM reciclaje r "
            "JOIN usuarios u ON r.usuario_id = u.usuario_id "
            "WHERE r.usuario_id = %s "
            "ORDER BY r.fecha DESC"
        )

        cursor.execute(consulta_historial, (usuario_id,))
        historial =cursor.fetchall()

        if historial:
            print("\n Historial de reciclaje   ")
            for fila in historial:
                nombre,material,cantidad,fecha = fila
                print(f" Usuario: {nombre} \n Material: {material} \n Cantidad:{cantidad}\n Fecha: {fecha}")
        else:
            print(f"No se encontraron registro de reciclaje")

    except Exception as e:
        print(f"Error al consultar el historial: {e}")

    finally:
        if conexion is not None and conexion.is_connected():
            if "cursor" in locals():
                cursor.close()
            conexion.close()
            print(" conexion cerrada")



