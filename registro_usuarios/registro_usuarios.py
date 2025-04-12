import mysql.connector
from mysql.connector import Error

def registrar_usuarios():
    conexion = None
    cursor = None
    #establecemos conexión con la base de datos
    try:
        nombre = input("Ingrese su nombre ")
        correo = input("Ingrese su correo ")
        cedula = input("Ingrese su cedula ")
        telefono = input("Ingrese su telefono ")

        conexion = mysql.connector.connect(
            host="localhost",  # dirección del servidor mysql
            port=3307,  # número puerto correcto si es diferente
            user="root",  # usuario base datos
            password="Fornite1923",  # contraseña bd
            database="reciclaje_bd"  # nombre base de datos
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = "INSERT INTO usuarios (nombre,correo,cedula,telefono) VALUES (%s,%s,%s,%s)"
            valores = (nombre,correo,cedula,telefono)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Usuario creado correctamente")

    except Error as e:
        print(f"Eror al registrar usuario: {e}")

    finally:
        if conexion is not None and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexion cerrada")