import json, os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EMP_FILE = os.path.join(DATA_DIR, "employees.json")

class EmpleadosWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Gestión de Empleados")
        self.setGeometry(150, 100, 900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)

        title = QLabel("Gestión de Empleados")
        title.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #4a7c59;")
        layout.addWidget(title)

        form_layout = QHBoxLayout()
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        form_layout.addWidget(self.nombre_input)

        self.puesto_input = QComboBox()
        self.puesto_input.addItems(["Barista", "Cajero", "Cocinero", "Gerente", "Limpieza"])
        form_layout.addWidget(self.puesto_input)

        self.turno_input = QComboBox()
        self.turno_input.addItems(["Matutino", "Vespertino", "Nocturno"])
        form_layout.addWidget(self.turno_input)

        btn_agregar = QPushButton("Agregar")
        btn_agregar.setStyleSheet("background-color:#6b8e23;color:white;border-radius:5px;")
        btn_agregar.clicked.connect(self.agregar_empleado)
        form_layout.addWidget(btn_agregar)

        layout.addLayout(form_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Nombre","Puesto","Turno","Acciones"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla)

        central.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(EMP_FILE, 'r', encoding='utf-8') as f:
                empleados = json.load(f)
        except Exception:
            empleados = []
        self.tabla.setRowCount(len(empleados))
        for i, e in enumerate(empleados):
            self.tabla.setItem(i, 0, QTableWidgetItem(e['name']))
            self.tabla.setItem(i, 1, QTableWidgetItem(e.get('role','')))
            self.tabla.setItem(i, 2, QTableWidgetItem(e.get('shift','')))
            btn = QPushButton("Eliminar")
            btn.setStyleSheet("background-color:#d32f2f;color:white;border-radius:3px;")
            btn.clicked.connect(lambda checked, idx=i: self.eliminar_empleado(idx))
            self.tabla.setCellWidget(i, 3, btn)

    def save_emps(self, empleados):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(EMP_FILE, 'w', encoding='utf-8') as f:
            json.dump(empleados, f, indent=2, ensure_ascii=False)

    def agregar_empleado(self):
        name = self.nombre_input.text().strip()
        role = self.puesto_input.currentText()
        shift = self.turno_input.currentText()
        if not name:
            QMessageBox.warning(self, "Error", "Ingrese el nombre del empleado")
            return
        try:
            with open(EMP_FILE, 'r', encoding='utf-8') as f:
                empleados = json.load(f)
        except Exception:
            empleados = []
        empleados.append({"name": name, "role": role, "shift": shift})
        self.save_emps(empleados)
        self.nombre_input.clear()
        self.cargar_datos()

    def eliminar_empleado(self, idx):
        try:
            with open(EMP_FILE, 'r', encoding='utf-8') as f:
                empleados = json.load(f)
        except Exception:
            empleados = []
        if 0 <= idx < len(empleados):
            empleados.pop(idx)
            self.save_emps(empleados)
            self.cargar_datos()

    def closeEvent(self, event):
        if hasattr(self, 'parent_window') and self.parent_window:
            self.parent_window.show()
        event.accept()
