from conexion_bd.conexion import crear_conexion # Importamos la función de conexión

def registrar_reciclaje():
    try:
        conexion = crear_conexion()
        if conexion.is_connected():
            cursor = conexion.cursor()

            # verificamos usuario por correo
            correo = input("Ingrese su correo para registrar reciclaje :) : ")
            consulta_correo = "SELECT usuario_id FROM usuarios WHERE correo = %s"
            cursor.execute(consulta_correo, (correo,))
            usuario = cursor.fetchone()  # traer el primer resultado encontrado de la consulta SQL

            if usuario is None:
                print("El usuario no existe")
                return #Detenemos si no se encuentra el usuario


            usuario_id = usuario[0]

            # seleción del material
            material = input("Ingrese el material a reciclar: ").upper()
            if material not in ["PET", "ALUMINIO"]:
                print("material no valido")
                return
            try:
                cantidad = int(input("Ingrese la cantidad reciclada: "))
                if cantidad <= 0:
                    print("la cantidad debe ser positiva")
                    return
            except ValueError:
                 print("Ingrese un numero valido")
                 return

             # calcular puntos
            puntos = cantidad *20 if material == "PET" else cantidad *30

            # insertar en tabla de puntos
            maquina_id = 1
            sql_puntos = "INSERT INTO puntos (usuario_id,puntos) VALUES (%s,%s)"
            cursor.execute(sql_puntos, (usuario_id, puntos))
            # 6 Obtener el ultimo id de puntos insertados
            puntos_id = cursor.lastrowid

            # 5 insertar en tabla reciclaje
            sql_reciclaje = "INSERT INTO reciclaje (usuario_id, maquina_id, punto_id, material, cantidad) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_reciclaje, (usuario_id, maquina_id, puntos_id, material, cantidad))
            conexion.commit()
            print(f"¡Reciclaje registrado! Ganaste {puntos} puntos.")

    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("conexion cerrada")

