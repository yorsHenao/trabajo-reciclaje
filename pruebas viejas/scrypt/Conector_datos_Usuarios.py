#importar conector mySQL y la clase de Error para mejorar errores de conexión
"""""
import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="localhost",  # dirección del servidor mysql
        port=3307,  # número puerto correcto si es diferente
        user="root",  # usuario base datos
        password="Fornite1923",  # contraseña bd
        database="reciclaje_bd"  # nombre base de datos
    )
    if conexion.is_connected(): #inputs usuarios
        cursor = conexion.cursor()

        nombre= input("Ingrese su nombre")
        correo= input("Ingrese su correo")
        contraseña= input("Ingrese su contraseña")
        telefono= input("Ingrese su telefono")

        #Vereficar si el correo ya existe
        consulta_correo = "SELECT correo FROM usuarios WHERE correo = %s"
        cursor.execute(consulta_correo, (correo,)) #ejecuta la sentencia sql
        resultado = cursor.fetchone()


    if resultado:
        print("El correo ya esta registrado, por favor intente con otro.")

    else:
        #si no existe el correo
         sql = "INSERT INTO usuarios (nombre, correo, contraseña, telefono) VALUES (%s, %s, %s,%s)"
         valores = (nombre, correo, contraseña, telefono)
         cursor.execute(sql, valores)
         conexion.commit()
         print("Usuario registrado con exito.")
except Error as e:
    print("Error al insertar en la base de datos:",e)

finally:
    if conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada")

"""