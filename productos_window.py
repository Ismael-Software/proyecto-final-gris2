import json, os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QLineEdit, QDoubleSpinBox, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

class ProductosWindow(QMainWindow):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(150, 100, 800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Gestión de Productos")
        title.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #4a7c59;")
        layout.addWidget(title)

        form_layout = QHBoxLayout()
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del producto")
        form_layout.addWidget(self.nombre_input)

        self.precio_input = QDoubleSpinBox()
        self.precio_input.setPrefix("$ ")
        self.precio_input.setMaximum(9999.99)
        form_layout.addWidget(self.precio_input)

        self.categoria_input = QComboBox()
        self.categoria_input.addItems(["Bebidas Calientes", "Bebidas Frías", "Alimentos", "Postres"])
        form_layout.addWidget(self.categoria_input)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.setStyleSheet("background-color: #6b8e23; color:white; border-radius:5px;")
        btn_agregar.clicked.connect(self.agregar_producto)
        form_layout.addWidget(btn_agregar)
        layout.addLayout(form_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Precio", "Categoría", "Acciones"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla)

        central.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                productos = json.load(f)
        except Exception:
            productos = []
        self.tabla.setRowCount(len(productos))
        for i, p in enumerate(productos):
            self.tabla.setItem(i, 0, QTableWidgetItem(p['name']))
            self.tabla.setItem(i, 1, QTableWidgetItem(f"${p['price']:.2f}"))
            self.tabla.setItem(i, 2, QTableWidgetItem(p.get('category','')))
            btn = QPushButton("Eliminar")
            btn.setStyleSheet("background-color:#d32f2f;color:white;border-radius:3px;")
            btn.clicked.connect(lambda checked, idx=i: self.eliminar_producto(idx))
            self.tabla.setCellWidget(i, 3, btn)

    def save_products(self, productos):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(productos, f, indent=2, ensure_ascii=False)

    def agregar_producto(self):
        name = self.nombre_input.text().strip()
        price = float(self.precio_input.value())
        cat = self.categoria_input.currentText()
        if not name:
            QMessageBox.warning(self, "Error", "Ingrese el nombre del producto")
            return
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                productos = json.load(f)
        except Exception:
            productos = []
        productos.append({"name": name, "price": price, "category": cat})
        self.save_products(productos)
        self.nombre_input.clear()
        self.precio_input.setValue(0)
        self.cargar_datos()

    def eliminar_producto(self, idx):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                productos = json.load(f)
        except Exception:
            productos = []
        if 0 <= idx < len(productos):
            productos.pop(idx)
            self.save_products(productos)
            self.cargar_datos()

    def closeEvent(self, event):
        if self.login_window:
            self.login_window.show()
        event.accept()
