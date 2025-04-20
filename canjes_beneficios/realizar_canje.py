from conexion_bd.conexion import crear_conexion


def realizar_canje(nombre):

    try:
        # Establecer conexión
        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Obtener el ID del usuario desde su nombre
        cursor.execute("SELECT usuario_id FROM usuarios WHERE nombre = %s", (nombre,))
        usuario_data = cursor.fetchone()

        if not usuario_data:
            print(f"\n❌ Error: El usuario '{nombre}' no existe.")
            return None

        usuario_id = usuario_data[0]
        print(f" Usuario '{nombre}' tiene ID: {usuario_id}")

        # 3. Calcular puntos acumulados
        cursor.execute("""
            SELECT COALESCE(SUM(puntos), 0) 
            FROM puntos 
            WHERE usuario_id = %s
            """, (usuario_id,))
        puntos_usuario = cursor.fetchone()[0]
        print(f" Puntos totales: {puntos_usuario}")

        # 4. Obtener beneficios disponibles
        cursor.execute("""
            SELECT b.beneficio_id, b.nombre, b.puntos_requeridos, b.stock
            FROM beneficios b
            JOIN aliados a ON b.aliado_id = a.aliado_id
            WHERE b.stock > 0
            ORDER BY b.puntos_requeridos ASC
            """)
        beneficios = cursor.fetchall()

        if not beneficios:
            print("\nℹ️ No hay beneficios disponibles actualmente.")
            return None

        # 5. Mostrar beneficios
        print("\n⭐ Beneficios disponibles:")
        for beneficio in beneficios:
            id_b, nombre, puntos_req, stock = beneficio
            disponible = puntos_usuario >= puntos_req
            icono = "✅" if disponible else "❌"
            print(f"{icono} ID: {id_b} | {nombre} | {puntos_req} pts | Stock: {stock}")

        # 6. Procesar selección
        try:
            beneficio_id = int(input("\n➡️ Ingrese el ID del beneficio: "))
            beneficio = next((b for b in beneficios if b[0] == beneficio_id), None)

            if not beneficio:
                print("\n❌ Error: ID inválido")
                return None

            _, nombre, puntos_req, stock = beneficio

            # Validaciones finales
            if puntos_usuario < puntos_req:
                print(f"\n❌ Error: Necesitas {puntos_req} puntos (tienes {puntos_usuario})")
                return None

            if stock <= 0:
                print("\n❌ Error: Stock agotado")
                return None

            # 7. Actualizar datos
            nuevos_puntos = puntos_usuario - puntos_req

            # Registrar movimiento de puntos sin concepto
            cursor.execute("""
                INSERT INTO puntos (usuario_id, puntos)
                VALUES (%s, %s)
                """, (usuario_id, -puntos_req))

            # Actualizar stock
            cursor.execute("""
                UPDATE beneficios 
                SET stock = stock - 1 
                WHERE beneficio_id = %s
                """, (beneficio_id,))

            # Registrar canje
            cursor.execute("""
                INSERT INTO canjes (usuario_id, beneficio_id)
                VALUES (%s, %s)
                """, (usuario_id, beneficio_id))

            conexion.commit()

            print(f"\n🎉 ¡Canje exitoso! Beneficio: {nombre}")
            print(f"📉 Puntos restantes: {nuevos_puntos}")
            return True

        except ValueError:
            print("\n❌ Error: Debes ingresar un número válido")
            return None

    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        conexion.rollback()
        return None

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexion' in locals(): conexion.close()

