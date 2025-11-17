import os, json
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")

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
        self.tabla.setHorizontalHeaderLabels(["ID", "Fecha", "Cliente", "Productos", "Total", "Estado"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla)

        botones_layout = QHBoxLayout()
        btn_actualizar = QPushButton("Actualizar")
        btn_actualizar.setStyleSheet("background-color:#6b8e23;color:white;border-radius:5px;")
        btn_actualizar.clicked.connect(self.cargar_datos)
        botones_layout.addWidget(btn_actualizar)

        btn_completar = QPushButton("Marcar como completado")
        btn_completar.setStyleSheet("background-color:#4CAF50;color:white;border-radius:5px;")
        btn_completar.clicked.connect(self.marcar_completado)
        botones_layout.addWidget(btn_completar)

        botones_layout.addStretch()
        layout.addLayout(botones_layout)

        central.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(SALES_FILE, 'r', encoding='utf-8') as f:
                ventas = json.load(f)
        except Exception:
            ventas = []

        self.tabla.setRowCount(len(ventas))
        total = 0
        for i, v in enumerate(ventas):
            self.tabla.setItem(i, 0, QTableWidgetItem(v.get('id', '')))
            self.tabla.setItem(i, 1, QTableWidgetItem(v.get('fecha', '')))
            self.tabla.setItem(i, 2, QTableWidgetItem(v.get('cliente', '')))
            self.tabla.setItem(i, 3, QTableWidgetItem(v.get('productos', '')))
            self.tabla.setItem(i, 4, QTableWidgetItem(f"${v.get('total', 0):.2f}"))

            estado_item = QTableWidgetItem(v.get('estado', ''))
            estado_text = v.get('estado', '').lower()
            if estado_text in ('completado', 'completo', 'completed'):
                estado_item.setBackground(Qt.GlobalColor.green)
            else:
                estado_item.setBackground(Qt.GlobalColor.yellow)
            self.tabla.setItem(i, 5, estado_item)

            total += float(v.get('total', 0))

        self.total_ventas_label.setText(f"Total Ventas: ${total:.2f}")
        self.num_ventas_label.setText(f"Número de Ventas: {len(ventas)}")

    def marcar_completado(self):
        row = self.tabla.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Atención", "Seleccione un pedido para marcar como completado.")
            return

        sale_id_item = self.tabla.item(row, 0)
        if not sale_id_item:
            QMessageBox.warning(self, "Error", "No se encontró el ID del pedido seleccionado.")
            return
        sale_id = sale_id_item.text()

        try:
            with open(SALES_FILE, 'r', encoding='utf-8') as f:
                ventas = json.load(f)
        except Exception:
            ventas = []

        changed = False
        for venta in ventas:
            if venta.get('id') == sale_id:
                venta['estado'] = 'Completado'
                changed = True
                break

        if changed:
            with open(SALES_FILE, 'w', encoding='utf-8') as f:
                json.dump(ventas, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Completado", f"Pedido {sale_id} marcado como completado.")
            self.cargar_datos()
        else:
            QMessageBox.warning(self, "No encontrado", "No se pudo actualizar el pedido seleccionado.")

    def closeEvent(self, event):
        if hasattr(self, 'parent_window') and self.parent_window:
            self.parent_window.show()
        event.accept()
