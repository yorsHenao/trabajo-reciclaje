from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from conexion_bd.conexion import crear_conexion
from interfaz.ventana_menu import menu

class ventana_inicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de sesión")
        self.setGeometry(100, 100, 300, 150) #Dimensiones de la interfaz
        self.setStyleSheet("background-color: #588157;") #Color fondo


        layout = QVBoxLayout() #ordena verticalmente las opciones

        self.label = QLabel("Ingrese su número de cedula:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
        color: #2E3440;
        font-size: 25px;
        font-family: "Book Antiqua";
        font-weight: bold;
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

        self.setLayout(layout)

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


