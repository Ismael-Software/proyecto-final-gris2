import json, os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")

class ClienteWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Cliente - Realizar Pedido")
        self.setGeometry(100, 100, 900, 600)
        self.carrito = []

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Menú de Cafetería")
        header.setFont(QFont("Georgia", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #8b4513;")
        layout.addWidget(header)

        productos_layout = QVBoxLayout()
        layout.addLayout(productos_layout)

        self.products = self.load_products()
        row = None
        for i, prod in enumerate(self.products):
            if i % 3 == 0:
                row = QHBoxLayout()
                productos_layout.addLayout(row)
            btn = QPushButton(f"{prod['name']}\n${prod['price']:.2f}")
            btn.setFixedSize(200, 80)
            btn.setStyleSheet("QPushButton { background-color: #d2691e; color: white; border-radius: 8px; font-weight:bold; } QPushButton:hover { background-color: #8b4513; }")
            btn.clicked.connect(lambda checked, n=prod['name'], p=prod['price']: self.agregar_producto(n,p))
            row.addWidget(btn)

        carrito_label = QLabel("Carrito de Compras")
        carrito_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(carrito_label)

        self.carrito_table = QTableWidget()
        self.carrito_table.setColumnCount(3)
        self.carrito_table.setHorizontalHeaderLabels(["Producto", "Precio", "Acción"])
        self.carrito_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.carrito_table)

        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #8b4513;")
        layout.addWidget(self.total_label)

        btn_ordenar = QPushButton("Realizar Pedido")
        btn_ordenar.setFixedHeight(45)
        btn_ordenar.setStyleSheet("QPushButton { background-color: #6b8e23; color: white; border-radius:8px; font-weight:bold; } QPushButton:hover { background-color: #4a7c59; }")
        btn_ordenar.clicked.connect(self.realizar_pedido)
        layout.addWidget(btn_ordenar)

        central.setLayout(layout)

    def load_products(self):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def agregar_producto(self, nombre, precio):
        self.carrito.append({"nombre": nombre, "precio": precio})
        self.actualizar_carrito()

    def actualizar_carrito(self):
        self.carrito_table.setRowCount(len(self.carrito))
        total = 0
        for i, item in enumerate(self.carrito):
            self.carrito_table.setItem(i, 0, QTableWidgetItem(item['nombre']))
            self.carrito_table.setItem(i, 1, QTableWidgetItem(f"${item['precio']:.2f}"))
            btn_elim = QPushButton("Eliminar")
            btn_elim.clicked.connect(lambda checked, idx=i: self.eliminar_item(idx))
            self.carrito_table.setCellWidget(i, 2, btn_elim)
            total += item['precio']
        self.total_label.setText(f"Total: ${total:.2f}")

    def eliminar_item(self, idx):
        try:
            del self.carrito[idx]
        except Exception:
            pass
        self.actualizar_carrito()

    def realizar_pedido(self):
        if not self.carrito:
            QMessageBox.warning(self, "Carrito vacío", "Agregue productos al carrito")
            return
        try:
            if not os.path.exists(SALES_FILE):
                with open(SALES_FILE, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=2)
            with open(SALES_FILE, 'r', encoding='utf-8') as f:
                sales = json.load(f)
        except Exception:
            sales = []

        sale_id = str(len(sales)+1).zfill(3)
        total = sum(i['precio'] for i in self.carrito)
        products_str = ', '.join([i['nombre'] for i in self.carrito])
        from datetime import datetime
        sale = {
            "id": sale_id,
            "fecha": datetime.now().strftime('%d/%m/%Y %H:%M'),
            "cliente": "Cliente Local",
            "productos": products_str,
            "total": total,
            "estado": "En preparación"
        }
        sales.append(sale)
        with open(SALES_FILE, 'w', encoding='utf-8') as f:
            json.dump(sales, f, indent=2, ensure_ascii=False)
        QMessageBox.information(self, "Éxito", "Pedido realizado correctamente")
        self.carrito = []
        self.actualizar_carrito()

    def closeEvent(self, event):
        # al cerrar ventana cliente, mostramos main (si existe)
        if self.main_window:
            self.main_window.show()
        event.accept()
