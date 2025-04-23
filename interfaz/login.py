import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from conexion_bd.conexion import crear_conexion
from interfaz.ventana_menu import menu
from PySide6.QtGui import QPixmap
from interfaz.ventana_registro import VentanaRegistro
class ventana_inicio(QWidget):




    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")
        self.setGeometry(750, 300, 500, 500) #Dimensiones de la interfaz



        #fondo de imagen
        self.fondo = QLabel(self)
        pixmap = QPixmap("imagen/loguito.png")  # Usa tu ruta aquí
        self.fondo.setPixmap(pixmap)
        self.fondo.setScaledContents(True)
        self.fondo.lower()  # Mueve el fondo al fondo (por debajo de los demás widgets)



        layout = QVBoxLayout() #ordena verticalmente las opciones

        self.label = QLabel("Ingrese su número de cedula:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(50, 30)
        self.label.setStyleSheet("""
        color: #2E3440;
        font-size: 25px;
        font-family: "Book Antiqua";
        font-weight: bold;
        margin-top: 300px;
        """)

        self.input_cedula = QLineEdit() #modulo para que el usuario digite la información
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

        self.btn_registrar = QPushButton("Registrarse")
        self.btn_registrar.setStyleSheet("""
                background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
                """)
        self.btn_registrar.clicked.connect(self.registrar)

        self.btn_ingresar = QPushButton("Iniciar cesión")
        self.btn_ingresar.setStyleSheet("""
                background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
                """)
        self.btn_ingresar.clicked.connect(self.verificar_cedula)

        layout.addWidget(self.label)
        layout.addWidget(self.input_cedula)
        layout.addWidget(self.btn_ingresar)
        layout.addWidget(self.btn_registrar)

        self.setLayout(layout)

    def resizeEvent(self, event):
        self.fondo.resize(self.size())  # Para que el fondo se ajuste al tamaño
        super().resizeEvent(event)

    def registrar(self):
        self.ventana_registro = VentanaRegistro()
        self.ventana_registro.show()

    def verificar_cedula(self):
        cedula = self.input_cedula.text().strip()


        if not cedula.isdigit():
            QMessageBox.warning(self, "Error", "Por favor ingrese solo números.")
            return

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE cedula = %s", (cedula,))
        usuario = cursor.fetchone() #devuelve una tupla con todos los campos en el mismo orden que esta en mysql

        cursor.close()
        conexion.close()

        if usuario:
            self.hide()  # Oculta la ventana de login
            self.ventana_menu = menu(cedula = usuario[3],nombre=usuario[1])  # usuario[3] es la cédula
            self.ventana_menu.show()


        else:
            QMessageBox.critical(self,"Error", "Usuario no encontrado.")


if __name__ == "__main__": #se ejecuta direcamente
    app = QApplication([])
    ventana = ventana_inicio()
    ventana.show()
    app.exec_()


