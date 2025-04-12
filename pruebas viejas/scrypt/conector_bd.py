#importar conector mySQL y la clase de Error para mejorar errores de conexión
""""
import mysql.connector
from mysql.connector import Error
conexion = None
cursor = None
try:
    #establecemos la conexión con la base de datos
    conexion = mysql.connector.connect(
        host="localhost",  #dirección del servidor mysql
        port=3307,  # número puerto correcto si es diferente
        user="root",  #usuario base datos
        password="Fornite1923",  #password bd
        database="reciclaje_bd"  #nombre base de datos
    )

    #usamos if para verificar si la coneción fue exitosa
    if conexion.is_connected():
        #creamos un cursor para ejecutar sentencias SQL
        cursor = conexion.cursor()
        #se define sentencia SQL para insertar nuevos usuarios
        sql = "INSERT INTO usuarios (nombre, correo, contraseña, telefono) VALUES (%s, %s, %s,%s)"
        #valores que ingresamos
        valores = ("yors", "yorshenao@gmail.com", "12345", "3223152268")
        #ejecuatamos sentencia SQL
        cursor.execute(sql, valores)
        #Guardamos los cambios en la BD
        conexion.commit()
        print("Usuario Insertado correctamente")
#Si existe un error lo imprimimos
except Error as e:
    print(f"Error {e}")

#Cerramos conexión al finalizar
finally:
    if "conexion" in locals() and conexion.is_connected():
        cursor.close()
"""
