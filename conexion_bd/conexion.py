import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="Fornite1923",
            database="reciclaje_bd"

        )
        if conexion.is_connected():
            return conexion
        return None
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
