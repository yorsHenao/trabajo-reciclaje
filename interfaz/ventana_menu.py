from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QLabel
from interfaz.ventana_puntos import ventana_puntos
from interfaz.Registro_reciclaje import ventana_registrar_reciclaje
from interfaz.canje_beneficios import ventana_canje_beneficios
from interfaz.Consultar_Historial import historial_usuario
from PySide6.QtCore import Qt

class menu(QWidget):
    def __init__(self, cedula, nombre):
        super().__init__()
        self.cedula = cedula
        self.nombre_usuario = nombre
        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 150, 400, 300)
        self.setStyleSheet("background-color: #588157;")

        layout = QVBoxLayout()

        self.label_nombre = QLabel(f"¡¡Hola {self.nombre_usuario}!!")
        self.label_nombre.setAlignment(Qt.AlignCenter)
        self.label_nombre.setStyleSheet("""
        background-color: #588157;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
                
        
        """)
        layout.addWidget(self.label_nombre)

        # 2. Botones
        self.btn_consultar_puntos = QPushButton("Consultar puntos")
        self.btn_consultar_puntos.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_registrar_reciclaje = QPushButton("Registrar reciclaje")
        self.btn_registrar_reciclaje.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_canjear_beneficios = QPushButton("Canjear Beneficios")
        self.btn_canjear_beneficios.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)

        self.btn_ver_historial = QPushButton("Ver historial")
        self.btn_ver_historial.setStyleSheet(""" 
                background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_salir = QPushButton("Salir")
        self.btn_salir.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        # Conexiones
        self.btn_consultar_puntos.clicked.connect(self.ventana_puntos)
        self.btn_registrar_reciclaje.clicked.connect(self.ventana_registro_reciclaje)
        self.btn_canjear_beneficios.clicked.connect(self.ventana_canje_beneficios)
        self.btn_ver_historial.clicked.connect(self.historial_usuario)
        self.btn_salir.clicked.connect(self.close)

        # Añadir botones al layout
        layout.addWidget(self.btn_consultar_puntos)
        layout.addWidget(self.btn_registrar_reciclaje)
        layout.addWidget(self.btn_canjear_beneficios)
        layout.addWidget(self.btn_ver_historial)
        layout.addWidget(self.btn_salir)

        self.setLayout(layout)

    def ventana_puntos(self):
        self.ventana_puntos = ventana_puntos(self.cedula,self.nombre_usuario)
        self.ventana_puntos.show()

    def ventana_registro_reciclaje(self):
        self.ventana_reciclaje = ventana_registrar_reciclaje(self.cedula)
        self.ventana_reciclaje.show()

    def ventana_canje_beneficios(self):
        self.ventana_beneficios = ventana_canje_beneficios(self.cedula)
        self.ventana_beneficios.show()

    def historial_usuario(self):
        # Versión correcta - pasa los parámetros directamente
        print(">>> Desde menú - Cédula:", self.cedula, "Tipo:", type(self.cedula))
        print(">>> Desde menú - Nombre:", self.nombre_usuario, "Tipo:", type(self.nombre_usuario))
        self.ventana_historial = historial_usuario(self.cedula, self.nombre_usuario)
        self.ventana_historial.show()

if __name__ == "__main__":
    app = QApplication([])

