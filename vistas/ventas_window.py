from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from conexion.database import db


class VentasWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Registro de Ventas")
        self.setGeometry(150, 100, 900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Registro de Ventas")
        title.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #4a7c59;")
        layout.addWidget(title)

        filtros_layout = QHBoxLayout()
        fecha_label = QLabel("Fecha:")
        filtros_layout.addWidget(fecha_label)

        self.fecha_combo = QComboBox()
        self.fecha_combo.addItems(["Hoy", "Esta semana", "Este mes", "Todo"])
        filtros_layout.addWidget(self.fecha_combo)
        filtros_layout.addStretch()

        resumen_layout = QHBoxLayout()
        self.total_ventas_label = QLabel("Total Ventas: $0.00")
        self.total_ventas_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.total_ventas_label.setStyleSheet("color: #2e7d32; padding:10px;")
        resumen_layout.addWidget(self.total_ventas_label)

        self.num_ventas_label = QLabel("Número de Ventas: 0")
        self.num_ventas_label.setFont(QFont("Arial", 14))
        self.num_ventas_label.setStyleSheet("color: #555; padding:10px;")
        resumen_layout.addWidget(self.num_ventas_label)

        filtros_layout.addLayout(resumen_layout)
        layout.addLayout(filtros_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Cliente", "Empleado", "Total", "Detalles"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla)

        botones_layout = QHBoxLayout()
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.setStyleSheet("background-color:#6b8e23;color:white;border-radius:5px;")
        btn_actualizar.clicked.connect(self.cargar_datos)
        botones_layout.addWidget(btn_actualizar)

        botones_layout.addStretch()
        layout.addLayout(botones_layout)

        central.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        query = """
        SELECT p.id, p.fecha, c.nombre, e.nombre, p.total 
        FROM pedido p 
        LEFT JOIN cliente c ON p.cliente_id = c.id 
        LEFT JOIN empleado e ON p.empleado_id = e.id 
        ORDER BY p.fecha DESC
        """
        ventas = db.execute_query(query)

        if ventas is None:
            ventas = []

        self.tabla.setRowCount(len(ventas))
        total = 0

        for i, v in enumerate(ventas):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(v[0])))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(v[1])))
            self.tabla.setItem(i, 2, QTableWidgetItem(v[2] or "Cliente Local"))
            self.tabla.setItem(i, 3, QTableWidgetItem(v[3] or "Empleado No Asignado"))
            self.tabla.setItem(i, 4, QTableWidgetItem(f"${v[4]:.2f}"))

            # Botón para ver detalles
            btn_detalles = QPushButton("Ver Detalles")
            btn_detalles.setStyleSheet("background-color:#2196F3;color:white;border-radius:3px;")
            btn_detalles.clicked.connect(lambda checked, pedido_id=v[0]: self.ver_detalles(pedido_id))
            self.tabla.setCellWidget(i, 5, btn_detalles)

            total += float(v[4])

        self.total_ventas_label.setText(f"Total Ventas: ${total:.2f}")
        self.num_ventas_label.setText(f"Número de Ventas: {len(ventas)}")

    def ver_detalles(self, pedido_id):
        query = """
        SELECT pr.nombre, pp.cantidad, pr.precio 
        FROM pedido_producto pp 
        JOIN producto pr ON pp.producto_id = pr.id 
        WHERE pp.pedido_id = %s
        """
        detalles = db.execute_query(query, (pedido_id,))

        if detalles:
            detalle_text = "Detalles del Pedido:\n\n"
            for detalle in detalles:
                detalle_text += f"{detalle[0]} x{detalle[1]} - ${detalle[2]:.2f}\n"

            QMessageBox.information(self, f"Detalles Pedido #{pedido_id}", detalle_text)

    def closeEvent(self, event):
        if hasattr(self, 'parent_window') and self.parent_window:
            self.parent_window.show()
        event.accept()