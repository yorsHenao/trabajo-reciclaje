from conexion_bd.conexion import crear_conexion

def mostrar_beneficios(usuario_id):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    consulta = """
    SELECT b.beneficio_id, b.nombre, b.puntos_requeridos, b.stock, p.puntos
    FROM beneficios b
    JOIN aliados a ON b.aliado_id = a.aliado_id
    JOIN puntos p ON p.usuario_id = %s
    ORDER BY b.fecha_creacion DESC;
    """

    cursor.execute(consulta, (usuario_id,))
    resultados = cursor.fetchall()

    if resultados:
        print("\n Beneficios disponibles \n")
        for beneficio in resultados:
            beneficio_id, nombre, puntos_requeridos, stock, puntos_usuarios = beneficio
            estado = "Disponible" if puntos_usuarios >= puntos_requeridos and stock > 0 else "No disponible"
            print(f"ID: {beneficio_id}) | {nombre} - requiere: {puntos_requeridos} pts | stock: {stock} | Estado: {estado}")

    else:
        print("No hay beneficios registradoso aún no tienes puntos")

    cursor.close()
    conexion.close()
