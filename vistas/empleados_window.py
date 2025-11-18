from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont
from conexion.database import db


class EmpleadosWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Gestión de Empleados")
        self.setGeometry(150, 100, 900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

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
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Puesto", "Turno", "Acciones"])
        self.tabla.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tabla)

        central.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        query = "SELECT id, nombre, puesto, disponible FROM empleado"
        empleados = db.execute_query(query)

        if empleados is None:
            empleados = []

        self.tabla.setRowCount(len(empleados))
        for i, e in enumerate(empleados):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(e[0])))
            self.tabla.setItem(i, 1, QTableWidgetItem(e[1]))
            self.tabla.setItem(i, 2, QTableWidgetItem(e[2]))
            self.tabla.setItem(i, 3, QTableWidgetItem("Disponible" if e[3] else "No disponible"))
            btn = QPushButton("Eliminar")
            btn.setStyleSheet("background-color:#d32f2f;color:white;border-radius:3px;")
            btn.clicked.connect(lambda checked, idx=e[0]: self.eliminar_empleado(idx))
            self.tabla.setCellWidget(i, 4, btn)

    def agregar_empleado(self):
        name = self.nombre_input.text().strip()
        role = self.puesto_input.currentText()
        shift = self.turno_input.currentText()

        if not name:
            QMessageBox.warning(self, "Error", "Ingrese el nombre del empleado")
            return

        query = """INSERT INTO empleado (nombre, puesto, disponible, cafeteria_id) 
                   VALUES (%s, %s, %s, %s)"""
        result = db.execute_query(query, (name, role, 1, 1))

        if result:
            QMessageBox.information(self, "Éxito", "Empleado agregado correctamente")
            self.nombre_input.clear()
            self.cargar_datos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el empleado")

    def eliminar_empleado(self, empleado_id):
        reply = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar este empleado?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            query = "DELETE FROM empleado WHERE id = %s"
            result = db.execute_query(query, (empleado_id,))

            if result:
                QMessageBox.information(self, "Éxito", "Empleado eliminado correctamente")
                self.cargar_datos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el empleado")

    def closeEvent(self, event):
        if hasattr(self, 'parent_window') and self.parent_window:
            self.parent_window.show()
        event.accept()