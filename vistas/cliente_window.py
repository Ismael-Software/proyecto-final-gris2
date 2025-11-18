from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QSpinBox, QScrollArea, QGridLayout)
from PyQt6.QtGui import QFont
from conexion.database import db


class ClienteWindow(QMainWindow):
    def __init__(self, main_window=None, cliente_data=None):
        super().__init__()
        self.main_window = main_window
        self.cliente_data = cliente_data
        self.setWindowTitle("Cliente - Realizar Pedido")
        self.setGeometry(100, 100, 900, 600)
        self.carrito = []

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Mostrar información del cliente
        if cliente_data:
            cliente_info = QLabel(f"Bienvenido: {cliente_data['nombre']}")
            cliente_info.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            cliente_info.setStyleSheet("color: #8b4513; background-color: #fff8dc; padding: 8px; border-radius: 5px;")
            layout.addWidget(cliente_info)

        header = QLabel("Menú de Cafetería")
        header.setFont(QFont("Georgia", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #8b4513;")
        layout.addWidget(header)

        # Área de productos con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #d2691e;
                border-radius: 5px;
                background-color: white;
            }
        """)

        products_widget = QWidget()
        self.products_layout = QGridLayout()
        self.products_layout.setSpacing(10)
        self.products_layout.setContentsMargins(10, 10, 10, 10)

        self.products = self.load_products()
        self.mostrar_productos()

        products_widget.setLayout(self.products_layout)
        scroll_area.setWidget(products_widget)
        layout.addWidget(scroll_area)

        carrito_label = QLabel("Carrito de Compras")
        carrito_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(carrito_label)

        self.carrito_table = QTableWidget()
        self.carrito_table.setColumnCount(5)
        self.carrito_table.setHorizontalHeaderLabels(["ID", "Producto", "Precio", "Cantidad", "Acción"])
        self.carrito_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.carrito_table)

        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #8b4513;")
        layout.addWidget(self.total_label)

        btn_ordenar = QPushButton("Realizar Pedido")
        btn_ordenar.setFixedHeight(45)
        btn_ordenar.setStyleSheet(
            "QPushButton { background-color: #6b8e23; color: white; border-radius:8px; font-weight:bold; } QPushButton:hover { background-color: #4a7c59; }")
        btn_ordenar.clicked.connect(self.realizar_pedido)
        layout.addWidget(btn_ordenar)

        central.setLayout(layout)
        self.actualizar_carrito()

    def load_products(self):
        query = "SELECT id, nombre, precio, categoria, stock FROM producto WHERE disponible = 1 AND stock > 0"
        result = db.execute_query(query)
        if result:
            return [{"id": row[0], "nombre": row[1], "precio": row[2], "categoria": row[3], "stock": row[4]} for row in
                    result]
        return []

    def mostrar_productos(self):
        """Muestra los productos en una cuadrícula simple"""
        row = 0
        col = 0
        for prod in self.products:
            btn = QPushButton(f"{prod['nombre']}\n${prod['precio']:.2f}\nStock: {prod['stock']}")
            btn.setFixedSize(150, 80)
            if prod['stock'] > 0:
                btn.setStyleSheet(
                    "QPushButton { background-color: #d2691e; color: white; border-radius: 8px; font-weight:bold; } QPushButton:hover { background-color: #8b4513; }")
                btn.clicked.connect(lambda checked, n=prod['nombre'], p=float(prod['precio']), id=prod['id'],
                                           stock=prod['stock']: self.agregar_producto(n, p, id, stock))
            else:
                btn.setStyleSheet("QPushButton { background-color: #cccccc; color: #666666; border-radius: 8px; }")
                btn.setEnabled(False)

            self.products_layout.addWidget(btn, row, col)
            col += 1
            if col >= 4:  # 4 productos por fila
                col = 0
                row += 1

    def agregar_producto(self, nombre, precio, producto_id, stock):
        # Verificar si el producto ya está en el carrito
        for item in self.carrito:
            if item['id'] == producto_id:
                if item['cantidad'] < stock:
                    item['cantidad'] += 1
                    item['subtotal'] = item['precio'] * item['cantidad']
                else:
                    QMessageBox.warning(self, "Stock insuficiente", f"No hay suficiente stock de {nombre}")
                self.actualizar_carrito()
                return

        # Si no está en el carrito, agregarlo
        self.carrito.append({
            "id": producto_id,
            "nombre": nombre,
            "precio": precio,
            "cantidad": 1,
            "subtotal": precio
        })
        self.actualizar_carrito()

    def actualizar_carrito(self):
        self.carrito_table.setRowCount(len(self.carrito))
        total = 0

        for i, item in enumerate(self.carrito):
            self.carrito_table.setItem(i, 0, QTableWidgetItem(str(item['id'])))
            self.carrito_table.setItem(i, 1, QTableWidgetItem(item['nombre']))
            self.carrito_table.setItem(i, 2, QTableWidgetItem(f"${item['precio']:.2f}"))

            # SpinBox para cantidad
            spin_box = QSpinBox()
            spin_box.setMinimum(1)
            spin_box.setMaximum(100)
            spin_box.setValue(item['cantidad'])
            spin_box.valueChanged.connect(lambda value, idx=i: self.actualizar_cantidad(idx, value))
            self.carrito_table.setCellWidget(i, 3, spin_box)

            btn_elim = QPushButton("Eliminar")
            btn_elim.setStyleSheet("background-color:#d32f2f;color:white;border-radius:3px;")
            btn_elim.clicked.connect(lambda checked, idx=i: self.eliminar_item(idx))
            self.carrito_table.setCellWidget(i, 4, btn_elim)

            total += item['subtotal']

        self.total_label.setText(f"Total: ${total:.2f}")

    def actualizar_cantidad(self, idx, nueva_cantidad):
        if 0 <= idx < len(self.carrito):
            # Verificar stock disponible
            query = "SELECT stock FROM producto WHERE id = %s"
            result = db.execute_query(query, (self.carrito[idx]['id'],))
            if result and nueva_cantidad <= result[0][0]:
                self.carrito[idx]['cantidad'] = nueva_cantidad
                self.carrito[idx]['subtotal'] = self.carrito[idx]['precio'] * nueva_cantidad
                self.actualizar_carrito()
            else:
                QMessageBox.warning(self, "Stock insuficiente", "No hay suficiente stock disponible")
                # Resetear al valor anterior
                self.actualizar_carrito()

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

        # Verificar stock antes de realizar el pedido
        for item in self.carrito:
            query = "SELECT stock FROM producto WHERE id = %s"
            result = db.execute_query(query, (item['id'],))
            if result and item['cantidad'] > result[0][0]:
                QMessageBox.warning(self, "Stock insuficiente",
                                    f"No hay suficiente stock de {item['nombre']}. Stock disponible: {result[0][0]}")
                return

        # Insertar pedido
        total = sum(i['subtotal'] for i in self.carrito)
        cliente_id = self.cliente_data['id'] if self.cliente_data else 1

        query_pedido = "INSERT INTO pedido (total, cliente_id, empleado_id) VALUES (%s, %s, %s)"
        pedido_id = db.execute_query(query_pedido, (total, cliente_id, 1))

        if pedido_id:
            # Insertar productos del pedido y actualizar stock
            for item in self.carrito:
                query_detalle = "INSERT INTO pedido_producto (pedido_id, producto_id, cantidad) VALUES (%s, %s, %s)"
                db.execute_query(query_detalle, (pedido_id, item['id'], item['cantidad']))

                # Actualizar stock
                query_update_stock = "UPDATE producto SET stock = stock - %s WHERE id = %s"
                db.execute_query(query_update_stock, (item['cantidad'], item['id']))

            QMessageBox.information(self, "Éxito", f"Pedido realizado correctamente. ID: {pedido_id}")
            self.carrito = []
            self.actualizar_carrito()
            # Recargar productos para actualizar stock
            self.products = self.load_products()
            # Limpiar y volver a mostrar productos
            for i in reversed(range(self.products_layout.count())):
                self.products_layout.itemAt(i).widget().setParent(None)
            self.mostrar_productos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo realizar el pedido")

    def closeEvent(self, event):
        if self.main_window:
            self.main_window.show()
        event.accept()