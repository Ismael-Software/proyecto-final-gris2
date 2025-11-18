import json, os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QLineEdit, QDoubleSpinBox, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QSpinBox
)
from PyQt6.QtGui import QFont
from database import db


class ProductosWindow(QMainWindow):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Gestión de Productos")
        self.setGeometry(150, 100, 900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Gestión de Productos")
        title.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #4a7c59;")
        layout.addWidget(title)

        # Formulario para agregar producto
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

        self.stock_input = QSpinBox()
        self.stock_input.setPrefix("Stock: ")
        self.stock_input.setMaximum(1000)
        self.stock_input.setValue(0)
        form_layout.addWidget(self.stock_input)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.setStyleSheet("background-color: #6b8e23; color:white; border-radius:5px;")
        btn_agregar.clicked.connect(self.agregar_producto)
        form_layout.addWidget(btn_agregar)
        layout.addLayout(form_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Precio", "Categoría", "Stock", "Actualizar Stock", "Acciones"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla)

        central.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        query = "SELECT id, nombre, precio, categoria, stock FROM producto"
        productos = db.execute_query(query)

        if productos is None:
            productos = []

        self.tabla.setRowCount(len(productos))
        for i, p in enumerate(productos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(p[0])))
            self.tabla.setItem(i, 1, QTableWidgetItem(p[1]))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"${p[2]:.2f}"))
            self.tabla.setItem(i, 3, QTableWidgetItem(p[3]))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(p[4])))

            # SpinBox para actualizar stock
            stock_spin = QSpinBox()
            stock_spin.setValue(p[4])
            stock_spin.setMaximum(1000)
            stock_spin.valueChanged.connect(lambda value, prod_id=p[0]: self.actualizar_stock(prod_id, value))
            self.tabla.setCellWidget(i, 5, stock_spin)

            btn = QPushButton("Eliminar")
            btn.setStyleSheet("background-color:#d32f2f;color:white;border-radius:3px;")
            btn.clicked.connect(lambda checked, idx=p[0]: self.eliminar_producto(idx))
            self.tabla.setCellWidget(i, 6, btn)

    def actualizar_stock(self, producto_id, nuevo_stock):
        """Actualiza el stock de un producto en tiempo real"""
        query = "UPDATE producto SET stock = %s WHERE id = %s"
        result = db.execute_query(query, (nuevo_stock, producto_id))
        if result:
            # Actualizar la visualización inmediatamente
            self.cargar_datos()

    def agregar_producto(self):
        name = self.nombre_input.text().strip()
        price = float(self.precio_input.value())
        cat = self.categoria_input.currentText()
        stock = self.stock_input.value()

        if not name:
            QMessageBox.warning(self, "Error", "Ingrese el nombre del producto")
            return

        query = """INSERT INTO producto (nombre, precio, categoria, stock, disponible, cafeteria_id) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        result = db.execute_query(query, (name, price, cat, stock, 1, 1))

        if result:
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente")
            self.nombre_input.clear()
            self.precio_input.setValue(0)
            self.stock_input.setValue(0)
            self.cargar_datos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el producto")

    def eliminar_producto(self, producto_id):
        reply = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar este producto?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM producto WHERE id = %s"
            result = db.execute_query(query, (producto_id,))

            if result:
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
                self.cargar_datos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el producto")

    def closeEvent(self, event):
        if self.login_window:
            self.login_window.show()
        event.accept()