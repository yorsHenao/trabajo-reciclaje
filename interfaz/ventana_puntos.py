from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from conexion_bd.conexion import crear_conexion
from PySide6.QtCore import Qt


class ventana_puntos(QWidget): #ventana
    def __init__(self,cedula,nombre):
        super().__init__()
        self.setWindowTitle("Puntos acumulados") #titulo de ventana
        self.setGeometry(750, 300,400,300)
        self.setStyleSheet("background-color: #3a5a40;")

        self.cedula = cedula
        self.nombre_usuario = nombre
        print("📤 Cédula recibida en ventana_puntos:", self.cedula)

        layout = QVBoxLayout()
        # layout para ordenar verticalmente los elementos
        layout.setSpacing(0)  # Esto reduce el espacio vertical entre los labels
        self.label_mensaje = QLabel("")
        self.label_mensaje.setAlignment(Qt.AlignCenter)
        self.label_mensaje.setContentsMargins(0, 0, 0, 0)
        self.label_mensaje.setStyleSheet("""
            color: #a3b18a;
            font-size: 25px;
            font-family: "Book Antiqua";
            font-weight: bold;
        """)

        layout.addWidget(self.label_mensaje)

        self.setLayout(layout) #Guardamos el layout en la ventana

        self.obtener_puntos() #consultamos los puntos del usuario

    def obtener_puntos(self):
        try:
            conexion = crear_conexion()

            # Usa cursor con buffered=True
            cursor1 = conexion.cursor(buffered=True)
            cursor1.execute("SELECT usuario_id FROM usuarios WHERE nombre = %s", (self.nombre_usuario,))
            resultado_usuario = cursor1.fetchone()
            cursor1.close()

            if resultado_usuario:
                usuario_id = resultado_usuario[0]

                cursor2 = conexion.cursor(buffered=True)
                cursor2.execute("SELECT puntos FROM puntos WHERE usuario_id = %s", (usuario_id,))
                resultado_puntos = cursor2.fetchone()
                cursor2.close()

                if resultado_puntos:
                    puntos = resultado_puntos[0]
                    mensaje = f"\n¡ {self.nombre_usuario}!\n tienes en total {puntos} puntos. ¡Sigue cuidando del planeta!"
                    self.label_mensaje.setText(mensaje)

                else:
                    self.label_mensaje.setText("No se encontraron puntos registrados.")
            else:
                self.label_mensaje.setText("Usuario no encontrado.")



            conexion.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al consultar los puntos:\n{str(e)}")
            print("❌ Error:", e)



