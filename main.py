from registro_usuarios.registro_usuarios import registrar_usuarios
from registro_reciclaje.registro_reciclaje import registrar_reciclaje
from usuarios.usuarios_existentes import consultar_puntos
from usuarios.historial_reciclaje import consultar_historial
from canjes_beneficios.canjes import mostrar_beneficios
from canjes_beneficios.realizar_canje import realizar_canje
from usuarios.login import login_usuario


# Menú para usuarios después de iniciar sesión
def menu_usuario(nombre):
    while True:
        print(f"\n Bienvenido, {nombre}")
        print("1. Registrar Reciclaje")
        print("2. Canjear Puntos")
        print("3. Consultar Puntos")
        print("4. Consultar Historial")
        print("5. Cerrar sesión")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_reciclaje()
        elif opcion == "2":
            realizar_canje(nombre)
        elif opcion == "3":
            consultar_puntos()
        elif opcion == "4":
            consultar_historial()
        elif opcion == "5":
            print("Cerrando sesión...\n")
            break
        else:
            print("Opción no válida")


# Menú principal para nuevos usuarios o sin sesión
def menu_principal():
    while True:
        print("\n Bienvenido al sistema de reciclaje \n")
        print("1. Registrar Usuario")
        print("2. Iniciar Sesión")
        print("3. Consultar Beneficios")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_usuarios()
        elif opcion == "2":
            nombre = login_usuario()
            if nombre:
                menu_usuario(nombre)
        elif opcion == "3":
            mostrar_beneficios(None)  # Se pueden ver sin iniciar sesión
        elif opcion == "4":
            print("Hasta luego 👋")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    menu_principal()
