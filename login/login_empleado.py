from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from empleado_window import EmpleadoWindow
from conexion.database import db


class LoginEmpleado(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Login - Empleado")
        self.setGeometry(150, 150, 500, 400)
        self.setStyleSheet("background-color: #e8f5e9;")
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        title = QLabel("Acceso Empleado")
        title.setFont(QFont("Georgia", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #4a7c59;")
        layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setFixedHeight(40)
        self.user_input.setStyleSheet("color: black; border: 2px solid #4a7c59; border-radius: 5px; padding: 6px;")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFixedHeight(40)
        self.pass_input.setStyleSheet("color: black; border: 2px solid #4a7c59; border-radius: 5px; padding: 6px;")
        layout.addWidget(self.pass_input)



        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setFixedHeight(45)
        btn_login.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        btn_login.setStyleSheet("background-color: #4a7c59; color: white; border-radius:8px;")
        btn_login.clicked.connect(self.do_login)
        layout.addWidget(btn_login)

        layout.addStretch()
        central.setLayout(layout)

    def do_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Complete todos los campos")
            return


        usuario = db.autenticar_usuario(username, password)

        if usuario and usuario['tipo'] in ['empleado', 'admin']:
            self.empleado_window = EmpleadoWindow(self.main_window, usuario)
            self.empleado_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def closeEvent(self, event):
        if self.main_window and not hasattr(self, 'empleado_window'):
            self.main_window.show()
        event.accept()