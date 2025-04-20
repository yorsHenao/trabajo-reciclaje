from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QPushButton, QComboBox
from conexion_bd.conexion import crear_conexion
import datetime
from PySide6.QtCore import Qt

class ventana_canje_beneficios(QWidget):
    def __init__(self, cedula):
        super().__init__()
        self.setWindowTitle("Canjear Beneficios")
        self.setGeometry(100, 150, 400, 300)
        self.setStyleSheet("background-color: #588157;")
        self.cedula = cedula

        layout = QVBoxLayout()
        self.titulo = QLabel("Selecciona un beneficio")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("""
               background-color: #588157;
                color: #2E3440;
                font-size: 20px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        layout.addWidget(self.titulo)

        # Contenedor con estilo para los beneficios
        self.beneficios_widget = QWidget()
        self.beneficios_layout = QVBoxLayout()
        self.beneficios_widget.setLayout(self.beneficios_layout)
        self.beneficios_widget.setStyleSheet("""
                background-color: #588157;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        layout.addWidget(self.beneficios_widget)

        self.setLayout(layout)

        self.beneficios_dict = {}
        self.cargar_beneficios()

    def cargar_beneficios(self):
        conexion = crear_conexion()
        if not conexion:
            return
        cursor = conexion.cursor()
        cursor.execute("SELECT beneficio_id, nombre, puntos_requeridos FROM beneficios")
        beneficios = cursor.fetchall()
        cursor.close()
        conexion.close()

        for beneficio in beneficios:
            beneficio_id, nombre, puntos = beneficio
            texto = f"{nombre} - {puntos} puntos"


            boton = QPushButton(texto)
            boton.setStyleSheet("""
                background-color: #344e41;
                color: #dad7cd;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px;
            """)
            boton.clicked.connect(
                lambda checked, b_id=beneficio_id, pts=puntos, txt=texto: self.canjear_beneficio(b_id, pts, txt))
            self.beneficios_layout.addWidget(boton)

    def canjear_beneficio(self, beneficio_id, puntos_requeridos, texto):
        conexion = crear_conexion()
        if not conexion:
            return

        try:
            cursor = conexion.cursor(buffered=True)

            # Buscar usuario_id
            cursor.execute("SELECT usuario_id FROM usuarios WHERE cedula = %s", (self.cedula,))
            resultado = cursor.fetchone()
            if not resultado:
                QMessageBox.warning(self, "Error", "Usuario no encontrado")
                return

            usuario_id = resultado[0]

            # Verificar puntos
            cursor.execute("SELECT puntos FROM puntos WHERE usuario_id = %s", (usuario_id,))
            resultado_puntos = cursor.fetchone()
            if not resultado_puntos or resultado_puntos[0] < puntos_requeridos:
                QMessageBox.warning(self, "Puntos insuficientes", "No tienes puntos suficientes para este canje.")
                return

            # Registrar el canje
            fecha = datetime.datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "INSERT INTO canjes (usuario_id, beneficio_id, fecha_canje) VALUES (%s, %s, %s)",
                (usuario_id, beneficio_id, fecha)
            )

            # Actualizar los puntos
            nuevos_puntos = resultado_puntos[0] - puntos_requeridos
            cursor.execute("UPDATE puntos SET puntos = %s WHERE usuario_id = %s",
                           (nuevos_puntos, usuario_id))

            conexion.commit()
            QMessageBox.information(self, "¡Canje exitoso!", f"Canjeaste: {texto}")

        except Exception as e:
            print("Error en canje:", e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()



