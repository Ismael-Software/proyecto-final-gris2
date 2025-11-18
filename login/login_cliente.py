from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox, QHBoxLayout)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from vistas.cliente_window import ClienteWindow
from conexion.database import db


class LoginCliente(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Login - Cliente")
        self.setGeometry(150, 150, 500, 450)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fffaf0, stop:0.5 #f5f5dc, stop:1 #d2b48c);
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        title = QLabel("Bienvenido Cliente")
        title.setFont(QFont("Georgia", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #8b4513; padding: 10px;")
        layout.addWidget(title)

        # Selección de cliente
        cliente_layout = QHBoxLayout()
        cliente_label = QLabel("Cliente:")
        cliente_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        cliente_label.setStyleSheet("color: #654321;")
        cliente_layout.addWidget(cliente_label)

        self.cliente_combo = QComboBox()
        self.cliente_combo.setFixedHeight(35)
        self.cliente_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #8b4513;
                border-radius: 5px;
                padding: 5px;
                color: #333;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #8b4513;
            }
        """)
        self.cargar_clientes()
        cliente_layout.addWidget(self.cliente_combo)
        layout.addLayout(cliente_layout)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setFixedHeight(40)
        self.user_input.setStyleSheet("""
            QLineEdit {
                color: #333;
                border: 2px solid #8b4513;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #d2691e;
            }
        """)
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFixedHeight(40)
        self.pass_input.setStyleSheet("""
            QLineEdit {
                color: #333;
                border: 2px solid #8b4513;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #d2691e;
            }
        """)
        layout.addWidget(self.pass_input)

        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setFixedHeight(45)
        btn_login.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #8b4513;
                color: white;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #d2691e;
            }
            QPushButton:pressed {
                background-color: #654321;
            }
        """)
        btn_login.clicked.connect(self.do_login)
        layout.addWidget(btn_login)

        layout.addStretch()
        central.setLayout(layout)

    def cargar_clientes(self):
        clientes = db.execute_query("""
            SELECT c.id, c.nombre, u.username 
            FROM cliente c 
            LEFT JOIN usuarios u ON c.id = u.cliente_id 
            WHERE u.activo = 1 OR u.activo IS NULL
            ORDER BY c.nombre
        """)

        if clientes:
            for cliente in clientes:
                cliente_id, nombre, username = cliente
                display_text = f"{nombre} ({username})" if username else f"{nombre} (Sin usuario)"
                self.cliente_combo.addItem(display_text, cliente_id)

    def do_login(self):
        selected_index = self.cliente_combo.currentIndex()
        if selected_index == -1:
            QMessageBox.warning(self, "Error", "Seleccione un cliente")
            return

        cliente_id = self.cliente_combo.currentData()
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Complete todos los campos")
            return

        # Autenticar usuario
        usuario = db.autenticar_usuario(username, password)

        if usuario and usuario['tipo'] == 'cliente' and usuario['cliente_id'] == cliente_id:

            cliente_data = db.obtener_cliente_por_usuario(usuario['id'])
            if cliente_data:
                self.cliente_window = ClienteWindow(self.main_window, cliente_data)
                self.cliente_window.show()
                self.hide()
            else:
                QMessageBox.warning(self, "Error", "No se encontraron datos del cliente")
        else:
            QMessageBox.warning(self, "Error", "Credenciales incorrectas para el cliente seleccionado")

    def closeEvent(self, event):
        if self.main_window and not hasattr(self, 'cliente_window'):
            self.main_window.show()
        event.accept()