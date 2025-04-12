from registro_usuarios.registro_usuarios import registrar_usuarios
from registro_reciclaje.registro_reciclaje import registrar_reciclaje
from usuarios.usuarios_existentes import consultar_puntos
from usuarios.historial_reciclaje import consultar_historial
from canjes_beneficios.canjes import mostrar_beneficios

def menu_principal():
    print("Bienvenido al sistema de reciclaje")
    print("1. Registrar Usuario")
    print("2. Registrar Reciclaje")
    print("3. Consultar puntos")
    print("4. Consultar historial")
    print("5. Consultar beneficios")
    print("6. Salir")


    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        registrar_usuarios()
    elif opcion == "2":
        registrar_reciclaje()
    elif opcion == "3":
        consultar_puntos()
    elif opcion == "4":
        consultar_historial()
    elif opcion == "5":
        mostrar_beneficios(usuario_id)
    elif opcion == "6":
        print("Hasta luego")
    else:
        print("Opción no válida")

# Asegúrate de que esta sea la única línea fuera de las funciones
menu_principal()





