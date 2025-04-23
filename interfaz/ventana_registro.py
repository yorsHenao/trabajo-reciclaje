from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from conexion_bd.conexion import crear_conexion

class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(750, 300, 350, 300)
        self.setStyleSheet("background-color: #588157;")

        layout = QVBoxLayout()

        # Campos
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        self.input_nombre.setStyleSheet("""
        
        background-color: #dad7cd;
        border: 2px solid #dad7cd;
        color: #2E3440;
        font-size: 15px;
        font-family: "Consolas";
        font-weight: bold;
        border-radius: 6px;
                padding: 6px;
        
        """)

        self.input_cedula = QLineEdit()
        self.input_cedula.setPlaceholderText("Cédula")
        self.input_cedula.setStyleSheet("""
        background-color: #dad7cd;
        border: 2px solid #dad7cd;
        color: #2E3440;
        font-size: 15px;
        font-family: "Consolas";
        font-weight: bold;
        border-radius: 6px;
                padding: 6px;
        """)

        self.input_correo = QLineEdit()
        self.input_correo.setPlaceholderText("Correo electrónico")
        self.input_correo.setStyleSheet("""
        
        background-color: #dad7cd;
        border: 2px solid #dad7cd;
        color: #2E3440;
        font-size: 15px;
        font-family: "Consolas";
        font-weight: bold;
        border-radius: 6px;
                padding: 6px;
        """)

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Número de teléfono")
        self.input_telefono.setStyleSheet("""
        
        background-color: #dad7cd;
        border: 2px solid #dad7cd;
        color: #2E3440;
        font-size: 15px;
        font-family: "Consolas";
        font-weight: bold;
        border-radius: 6px;
                padding: 6px;
        """)

        self.btn_registrar = QPushButton("Registrar")
        self.btn_registrar.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
                """)

        self.btn_registrar.clicked.connect(self.registrar_usuario)

        # Añadir widgets al layout con estilo
        label_nombre = QLabel("Nombre:")
        label_nombre.setStyleSheet("""
            background-color: #588157;
            color: #cad2c5;
            font-size: 20px;
            font-family: "Book Antiqua";
            font-weight: bold;
        """)
        layout.addWidget(label_nombre)
        layout.addWidget(self.input_nombre)

        label_cedula = QLabel("Cédula:")
        label_cedula.setStyleSheet("""
            background-color: #588157;
            color: #cad2c5;
            font-size: 20px;
            font-family: "Book Antiqua";
            font-weight: bold;
        """)
        layout.addWidget(label_cedula)
        layout.addWidget(self.input_cedula)

        label_correo = QLabel("Correo:")
        label_correo.setStyleSheet("""
            background-color: #588157;
            color: #cad2c5;
            font-size: 20px;
            font-family: "Book Antiqua";
            font-weight: bold;
        """)
        layout.addWidget(label_correo)
        layout.addWidget(self.input_correo)

        label_telefono = QLabel("Teléfono:")
        label_telefono.setStyleSheet("""
            background-color: #588157;
            color: #cad2c5;
            font-size: 20px;
            font-family: "Book Antiqua";
            font-weight: bold;
        """)
        layout.addWidget(label_telefono)
        layout.addWidget(self.input_telefono)

        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

    def registrar_usuario(self):
        nombre = self.input_nombre.text().strip()
        cedula = self.input_cedula.text().strip()
        correo = self.input_correo.text().strip()
        telefono = self.input_telefono.text().strip()

        if not (nombre and cedula and correo and telefono):
            QMessageBox.warning(self, "Campos vacíos", "Por favor completa todos los campos.")
            return

        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE cedula = %s", (cedula,))
            existe = cursor.fetchone()

            if existe:
                QMessageBox.warning(self, "Error", "Este usuario ya está registrado.")
            else:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, cedula, correo, telefono) VALUES (%s, %s, %s, %s)",
                    (nombre, cedula, correo, telefono)
                )
                conexion.commit()
                QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente.")
                self.close()

            cursor.close()
            conexion.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar: {e}")
