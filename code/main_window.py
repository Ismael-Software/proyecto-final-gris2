from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from login_cliente import LoginCliente
from login_empleado import LoginEmpleado

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main cafeteria")
        self.setGeometry(100, 100, 700, 550)
        self.setStyleSheet("QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:0.5 #f5f5dc, stop:1 #d2b48c); }")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        title = QLabel("Cafetería")
        title.setFont(QFont("Georgia", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #6f4e37;")
        main_layout.addWidget(title)

        subtitle = QLabel("Sistema de Gestión • Seleccione su acceso")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #8b4513;")
        main_layout.addWidget(subtitle)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)

        cliente_frame = self.create_access_card("Cliente", "Realizar pedidos y consultar menú", "#8b4513", "#d2691e", self.open_cliente)
        empleado_frame = self.create_access_card("Empleado", "Gestión de pedidos y administración", "#4a7c59", "#6b8e23", self.open_empleado)

        buttons_layout.addWidget(cliente_frame)
        buttons_layout.addWidget(empleado_frame)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        central_widget.setLayout(main_layout)

    def create_access_card(self, title, description, color, hover_color, callback):
        frame = QFrame()
        frame.setFixedSize(260, 240)
        frame.setStyleSheet(f"QFrame {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #faf0e6); border-radius: 15px; border: 3px solid {color}; }} QFrame:hover {{ border: 3px solid {hover_color}; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fffacd, stop:1 #fff8dc); }}")

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 28, 25, 28)
        layout.setSpacing(18)

        card_title = QLabel(title)
        card_title.setFont(QFont("Georgia", 20, QFont.Weight.Bold))
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_title.setStyleSheet(f"color: {color}; border: none;")
        layout.addWidget(card_title)

        desc = QLabel(description)
        desc.setFont(QFont("Arial", 10))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #654321; border: none;")
        layout.addWidget(desc)

        layout.addStretch()
        btn = QPushButton("Ingresar")
        btn.setFixedHeight(45)
        btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"QPushButton {{ background-color: {hover_color}; color: white; border-radius: 8px; }} QPushButton:hover {{ background-color: {color}; }}")
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        frame.setLayout(layout)
        return frame

    def open_cliente(self):
        self.login_cliente = LoginCliente(self)
        self.login_cliente.show()
        self.hide()

    def open_empleado(self):
        self.login_empleado = LoginEmpleado(self)
        self.login_empleado.show()
        self.hide()
