from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from conexion_bd.conexion import crear_conexion

class ventana_registro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de usuario")
        self.setGeometry(100, 100, 350, 250)

        self.setStyleSheet("background-color: #a3b18a;")

        layout = QVBoxLayout()

        # Título
        self.titulo = QLabel("Registro de Usuario")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            font-family: "Book Antiqua";
            color: #2E3440;
        """)
        layout.addWidget(self.titulo)

        # Campo: nombre
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre completo")
        self.nombre.setStyleSheet(self.estilo_input())
        layout.addWidget(self.nombre)

        # Campo: cédula
        self.cedula = QLineEdit()
        self.cedula.setPlaceholderText("Número de cédula")
        self.cedula.setStyleSheet(self.estilo_input())
        layout.addWidget(self.cedula)

        # Campo: correo
        self.correo = QLineEdit()
        self.correo.setPlaceholderText("Correo electrónico")
        self.correo.setStyleSheet(self.estilo_input())
        layout.addWidget(self.correo)

        # Botón guardar
        self.btn_guardar_
