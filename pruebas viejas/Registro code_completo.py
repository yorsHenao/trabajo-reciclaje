import mysql.connector
from mysql.connector import Error

from Conector_datos_Usuarios import consulta_correo

try:
    conexion = mysql.connector.connect(
        host="localhost",  # dirección del servidor mysql
        port=3307,  # número puerto correcto si es diferente
        user="root",  # usuario base datos
        password="Fornite1923",  # contraseña bd
        database="reciclaje_bd"  # nombre base de datos
    )
    if conexion.is_connected():
        cursor = conexion.cursor()

        #verificamos usuario por correo
        correo = input("Ingrese su correo para registrar reciclaje :) : ")
        consulta_correo = "SELECT usuario_id FROM usuarios WHERE correo = %s"
        cursor.execute(consulta_correo, (correo,))
        usuario = cursor.fetchone() #traer el primer resultado encontrado de la consulta SQL

        if usuario is None:
            print("El usuario no existe")
        else:
            usuario_id = usuario[0]

        #seleción del material
        material = input("Ingrese el material a reciclar: ").upper()

        if material not in ["PET", "ALUMINIO"]:
            print ("material no valido")
        else:
            try:
                cantidad = int(input("Ingrese la cantidad reciclada"))
                if cantidad <= 0:
                    print("la cantidad debe ser positiva")
                    exit()
            except ValueError:
                print("Ingrese un numero valido")
                exit()

            # calcular puntos
            if material == "PET":
                puntos = cantidad * 20 #puntos por unidad pet
            else:
                puntos = cantidad * 30 #puntos por unidad aluminio

            #insertar en tabla de puntos
            maquina_id = 1
            sql_puntos = "INSERT INTO puntos (usuario_id,puntos) VALUES (%s,%s)"
            cursor.execute(sql_puntos, (usuario_id, puntos))
            # 6 Obtener el ultimo id de puntos insertados
            puntos_id = cursor.lastrowid

            #5 insertar en tabla reciclaje
            sql_reciclaje = "INSERT INTO reciclaje (usuario_id, maquina_id, punto_id, material, cantidad) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_reciclaje, (usuario_id, maquina_id, puntos_id, material, cantidad))
            conexion.commit()
            print(f"¡Reciclaje registrado! Ganaste {puntos} puntos.")


except Error as e:
    print("Error en el proceso:",e)

finally:
    if "conexion" in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("conexion cerrada")

