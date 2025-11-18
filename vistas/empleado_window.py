from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from vistas.productos_window import ProductosWindow
from vistas.empleados_window import EmpleadosWindow
from vistas.ventas_window import VentasWindow


class EmpleadoWindow(QMainWindow):
    def __init__(self, main_window=None, usuario_data=None):
        super().__init__()
        self.main_window = main_window
        self.usuario_data = usuario_data
        self.setWindowTitle("Empleado - Panel de Administración")
        self.setGeometry(100, 100, 1000, 650)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)

        # Mostrar información del usuario
        if usuario_data:
            user_info = QLabel(f"Usuario: {usuario_data['username']} - Tipo: {usuario_data['tipo']}")
            user_info.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            user_info.setStyleSheet("color: #4a7c59; background-color: #f1f8e9; padding: 8px; border-radius: 5px;")
            layout.addWidget(user_info)

        header = QLabel("Panel de Administración")
        header.setFont(QFont("Georgia", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #4a7c59;")
        layout.addWidget(header)

        nav_layout = QHBoxLayout()
        btn_productos = QPushButton("Gestión de Productos")
        btn_productos.setFixedHeight(45)
        btn_productos.setStyleSheet(self.get_button_style())
        btn_productos.clicked.connect(self.abrir_productos)
        nav_layout.addWidget(btn_productos)

        btn_empleados = QPushButton("Gestión de Empleados")
        btn_empleados.setFixedHeight(45)
        btn_empleados.setStyleSheet(self.get_button_style())
        btn_empleados.clicked.connect(self.abrir_empleados)
        nav_layout.addWidget(btn_empleados)

        btn_ventas = QPushButton("Registro de Ventas")
        btn_ventas.setFixedHeight(45)
        btn_ventas.setStyleSheet(self.get_button_style())
        btn_ventas.clicked.connect(self.abrir_ventas)
        nav_layout.addWidget(btn_ventas)

        layout.addLayout(nav_layout)

        info = QLabel("Seleccione una opción del menú para administrar la cafetería")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setFont(QFont("Arial", 12))
        info.setStyleSheet("color: #666; padding: 40px;")
        layout.addWidget(info)

        central.setLayout(layout)

    def get_button_style(self):
        return "QPushButton { background-color: #6b8e23; color: white; border-radius: 8px; font-size:13px; font-weight:bold; } QPushButton:hover { background-color: #4a7c59; }"

    def abrir_productos(self):
        self.productos_window = ProductosWindow()
        self.productos_window.show()

    def abrir_empleados(self):
        self.empleados_window = EmpleadosWindow()
        self.empleados_window.show()

    def abrir_ventas(self):
        self.ventas_window = VentasWindow()
        self.ventas_window.show()

    def closeEvent(self, event):
        if self.main_window:
            self.main_window.show()
        event.accept()