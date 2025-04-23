from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QComboBox, QSpinBox, QPushButton
from conexion_bd.conexion import crear_conexion
from PySide6.QtCore import Qt

class ventana_registrar_reciclaje(QWidget): #ventana
    def __init__(self,cedula):
        super().__init__()
        self.setWindowTitle("Registrar reciclaje") #titulo de ventana
        self.setGeometry(750, 300,400,300)
        self.setStyleSheet("background-color: #588157;")
        self.cedula = cedula

        layout = QVBoxLayout()

        self.label_material = QLabel("Selecciona el material a reciclar")
        self.label_material.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_material)
        self.label_material.setStyleSheet("""
        background-color: #588157;
                color: #cad2c5;
                font-size: 20px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)


        self.material_seleccionado = None  # Aquí se guarda la opción seleccionada

        self.btn_pet = QPushButton("Botella PET")
        self.btn_pet.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_pet.clicked.connect(lambda: self.seleccionar_material("Botella PET"))


        self.btn_aluminio = QPushButton("Lata Aluminio")
        self.btn_aluminio.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_aluminio.clicked.connect(lambda: self.seleccionar_material("Lata Aluminio"))

        layout.addWidget(self.btn_pet)
        layout.addWidget(self.btn_aluminio)



        self.cantidad =QSpinBox()
        self.cantidad.setRange(1,100)
        self.cantidad.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)

        self.btn_registrar = QPushButton("Registrar reciclaje")

        self.btn_registrar.clicked.connect(self.registrar_reciclaje)



        self.label_cantidad = (QLabel("Cantidad reclicada"))
        self.label_cantidad.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.cantidad)
        layout.addWidget(self.btn_registrar)
        self.btn_registrar.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_registrar.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)

        self.setLayout(layout)

    def seleccionar_material(self, material):
        self.material_seleccionado = material
        QMessageBox.information(self, "Material seleccionado", f"Seleccionaste: {material}")

    def registrar_reciclaje(self):
        material = self.material_seleccionado
        cantidad = self.cantidad.value()

        if not material:
            QMessageBox.warning(self, "Falta selección", "Por favor, selecciona un material para reciclar.")
            return

        puntos_unidad = 20 if material =="Botella PET" else 30
        puntos_totales = cantidad * puntos_unidad

        try:
            conexion = crear_conexion()
            cursor1 = conexion.cursor(buffered=True)

            cursor1.execute("SELECT usuario_id FROM usuarios WHERE cedula = %s", (self.cedula,))
            resultado = cursor1.fetchone()
            cursor1.close()


            if resultado:
                usuario_id = resultado[0]

                conexion = crear_conexion()
                cursor2 = conexion.cursor(buffered=True)

                cursor2.execute("SELECT puntos FROM puntos WHERE usuario_id = %s", (usuario_id,))
                resultado_puntos = cursor2.fetchone()

                if resultado_puntos:
                    # Actualizar puntos
                    nuevos_puntos = resultado_puntos[0] + puntos_totales
                    cursor2.execute("UPDATE puntos SET puntos = %s WHERE usuario_id = %s", (nuevos_puntos, usuario_id))
                else:
                    # Insertar nuevo registro de puntos
                    cursor2.execute("INSERT INTO puntos (usuario_id, puntos) VALUES (%s, %s)",
                                   (usuario_id, puntos_totales))

                conexion.commit()
                QMessageBox.information(self, "Felicidades", f"¡Reciclaje registrado! Ganaste {puntos_totales} puntos.")
            else:
                QMessageBox.warning(self, "Error", "Usuario no encontrado.")

            cursor2.close()
            conexion.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")







