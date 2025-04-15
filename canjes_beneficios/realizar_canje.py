from conexion_bd.conexion import crear_conexion

def realizar_canje(usuario_id):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    # Obtener puntos del usuario
    try:
        cursor.execute("SELECT SUM(puntos) FROM puntos WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        puntos_usuario = resultado[0] if resultado[0] is not None else 0

        print(f"[DEBUG] Puntos del usuario: {puntos_usuario}")

        if puntos_usuario <= 0:
            print("No tienes puntos disponibles.")
            return

    except Exception as e:
        print(f"[ERROR] Al consultar los puntos: {e}")
        return

    if puntos_usuario <= 0:
        print("No tienes puntos disponibles.")
        return

    # Obtener beneficios disponibles
    consulta_beneficios = """
    SELECT b.beneficio_id, b.nombre, b.puntos_requeridos, b.stock
    FROM beneficios b
    JOIN aliados a ON b.aliado_id = a.aliado_id
    ORDER BY b.fecha_creacion DESC;
    """

    cursor.execute(consulta_beneficios)
    beneficios = cursor.fetchall()

    if not beneficios:
        print("No hay beneficios disponibles.")
        return


    print("\nBeneficios disponibles:")
    for b in beneficios:
        beneficio_id, nombre, puntos_req, stock = b
        estado = "Disponible" if puntos_usuario >= puntos_req and stock > 0 else "No disponible"
        print(f"ID: {beneficio_id}) | {nombre} - Requiere: {puntos_req} pts | Stock: {stock} | Estado: {estado}")

    try:
        beneficio_id_elegido = int(input("\nIngresa el ID del beneficio que deseas canjear: "))

        # Buscar el beneficio seleccionado
        beneficio = next((b for b in beneficios if b[0] == beneficio_id_elegido), None)

        if not beneficio:
            print("ID de beneficio no válido.")
            return

        beneficio_id, nombre, puntos_req, stock = beneficio

        if puntos_usuario < puntos_req:
            print("No tienes suficientes puntos.")
            return
        if stock <= 0:
            print("Este beneficio no tiene stock disponible.")
            return

        # Actualizar puntos (asumimos que es un solo registro, puedes mejorar con lógica de prioridad más adelante)
        actualizar_puntos = "UPDATE puntos SET puntos = puntos - %s WHERE usuario_id = %s LIMIT 1"
        cursor.execute(actualizar_puntos, (puntos_req, usuario_id))

        # Disminuir stock
        actualizar_stock = "UPDATE beneficios SET stock = stock - 1 WHERE beneficio_id = %s"
        cursor.execute(actualizar_stock, (beneficio_id,))

        # Registrar el canje
        insertar_canje = "INSERT INTO canjes (usuario_id, beneficio_id) VALUES (%s, %s)"
        cursor.execute(insertar_canje, (usuario_id, beneficio_id))

        conexion.commit()
        puntos_restantes = puntos_usuario - puntos_req
        print(f"\n¡Has canjeado exitosamente: {nombre}!\nPuntos restantes: {puntos_restantes}")

    except ValueError:
        print("Entrada inválida. Debes ingresar un número.")
    finally:
        cursor.close()
        conexion.close()
