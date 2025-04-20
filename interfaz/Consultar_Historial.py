from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QPushButton, QTableWidget,QTableWidgetItem,QHeaderView
from conexion_bd.conexion import crear_conexion
from PySide6.QtCore import Qt


class historial_usuario(QWidget):
    def __init__(self, cedula,nombre):
        super().__init__()
        print(">>> En historial_usuario - Cédula:", cedula, "Tipo:", type(cedula))
        self.setWindowTitle("Ver historial")
        self.setGeometry(100, 150, 560, 470)
        self.setStyleSheet("background-color: #588157;")
        self.cedula = cedula
        self.nombre = nombre

        layout = QVBoxLayout()

        self.nombre_usuario = QLabel(f"¡¡Hola {self.nombre}!!")
        self.nombre_usuario.setAlignment(Qt.AlignCenter)
        self.nombre_usuario.setStyleSheet("""
        background-color: #588157;
                color: #2E3440;
                font-size: 20px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        layout.addWidget(self.nombre_usuario)

        self.tabla_historial = QTableWidget()
        layout.addWidget(self.tabla_historial)
        self.tabla_historial.setStyleSheet("""
        background-color: #344e41;
                color: #dad7cd;
                font-size: 15px;
                border-radius: 8px;
                padding: 10px;
        
        """)

        #botones
        self.btn_historial = QPushButton("Cerrar")
        self.btn_historial.setStyleSheet("""
        background-color: #8FBC8F;
                color: #2E3440;
                font-size: 15px;
                font-family: "Book Antiqua";
                font-weight: bold;
        """)
        self.btn_historial.clicked.connect(self.close)
        layout.addWidget(self.btn_historial)

        self.setLayout(layout)

        self.ver_historial()

    def ver_historial(self):
        conexion = crear_conexion()

        if not conexion:
            QMessageBox.critical(self,"Error", "No se pudo conectar la base de datos")
            return
        try:
            cursor = conexion.cursor()

            #Setencia SQL, historial reciclaje y puntos
            cursor.execute("""
                    SELECT 
                r.fecha AS 'Fecha',  -- ← Tabla 'reciclaje'
                'Reciclaje' AS 'Tipo',
                CONCAT('Material: ', r.material, ' - Cantidad: ', r.cantidad) AS 'Detalle',
                p.puntos AS 'Puntos'
            FROM 
                reciclaje r
            JOIN 
                puntos p ON r.punto_id = p.punto_id
            WHERE 
                r.usuario_id = (SELECT usuario_id FROM usuarios WHERE cedula = %s)
        
            UNION ALL
        
            SELECT 
                c.fecha_canje AS 'Fecha',  -- ← Tabla 'canjes'
                'Canje' AS 'Tipo',
                CONCAT( b.nombre) AS 'Detalle',
                -b.puntos_requeridos AS 'Puntos'
            FROM 
                canjes c
            JOIN 
                beneficios b ON c.beneficio_id = b.beneficio_id
            WHERE 
                c.usuario_id = (SELECT usuario_id FROM usuarios WHERE cedula = %s)
        
            ORDER BY 
                Fecha DESC  
                """, (self.cedula, self.cedula))

            historial = cursor.fetchall()

            # Configurar tabla
            self.tabla_historial.setColumnCount(4)
            self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "Tipo", "Detalle", "Puntos"])



            # Llenar tabla
            self.tabla_historial.setRowCount(len(historial))

            header = self.tabla_historial.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Tipo
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Detalle (expansible)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Puntos

            self.tabla_historial.setStyleSheet("""
                    background-color: #344e41;
                color: #dad7cd;
                font-size: 15px;
                font-family: "Book Antiqua";
                border-radius: 2px;
                padding: 2px;
                    
                    """)

            for fila, registro in enumerate(historial):
                for columna, dato in enumerate(registro):
                    self.tabla_historial.setItem(fila, columna, QTableWidgetItem(str(dato)))

                # Mostrar mensaje si no hay registros
            if len(historial) == 0:
                QMessageBox.information(self, "Historial", "No hay registros para mostrar")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")
        finally:
            cursor.close()
            conexion.close()
