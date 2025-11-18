import random

class Producto:
    def __init__(self, nombre, precio, tamaño):
        self.nombre = nombre
        self.precio = precio
        self.tamaño = tamaño
        self.inventario = random.randint(5, 50)  # inventario aleatorio entre 5 y 50 unidades
        self.vendidos = 0  

    def vender(self, cantidad):
        if cantidad <= self.inventario:
            self.inventario -= cantidad
            self.vendidos += cantidad
        else:
            print(f"No hay suficientes existencias de {self.nombre} para vender {cantidad} unidades.")

    def mostrar_info(self):
        return (f"Producto: {self.nombre}\n"
                f"Tamaño: {self.tamaño}\n"
                f"Precio: ${self.precio:.2f}\n"
                f"Existencias: {self.inventario} unidades")


class Bebida(Producto):
    def __init__(self, nombre, precio, tamaño, temperatura):
        super().__init__(nombre, precio, tamaño)
        self.temperatura = temperatura

    def mostrar_info(self):
        return (f"Bebida: {self.nombre}\n"
                f"Tamaño: {self.tamaño}\n"
                f"Temperatura: {self.temperatura}\n"
                f"Precio: ${self.precio:.2f}\n"
                f"Existencias: {self.inventario} unidades")


class Comida(Producto):
    def __init__(self, nombre, precio, tamaño, tipo):
        super().__init__(nombre, precio, tamaño)
        self.tipo = tipo

    def mostrar_info(self):
        return (f"Comida: {self.nombre}\n"
                f"Tipo: {self.tipo}\n"
                f"Porción: {self.tamaño}\n"
                f"Precio: ${self.precio:.2f}\n"
                f"Existencias: {self.inventario} unidades")


# --- Comidas ---
comida1 = Comida("Sándwich", 55, "Individual", "Salado")
comida2 = Comida("Ensalada", 60, "Grande", "Saludable")
comida3 = Comida("Pastel de Chocolate", 45, "Rebanada", "Dulce")

# --- Bebidas ---
bebida1 = Bebida("Café", 40, "Mediano", "Caliente")
bebida2 = Bebida("Jugo de Naranja", 35, "Grande", "Frío")
bebida3 = Bebida("Té de manzanilla", 38, "Mediano", "Caliente")

print(" COMIDAS DISPONIBLES ")
print("==========================\n")
print(comida1.mostrar_info())
print("\n" + comida2.mostrar_info())
print("\n" + comida3.mostrar_info())

print("\n\n BEBIDAS DISPONIBLES ")
print("=========================\n")
print(bebida1.mostrar_info())
print("\n" + bebida2.mostrar_info())
print("\n" + bebida3.mostrar_info())

total_existencias = (
    comida1.inventario + comida2.inventario + comida3.inventario +
    bebida1.inventario + bebida2.inventario + bebida3.inventario
)

print(f"\n\n Total de productos en inventario: {total_existencias} unidades")


productos = [comida1, comida2, comida3, bebida1, bebida2, bebida3]

print("\n\nREPORTE DE VENTAS DEL DÍA")
print("================================\n")

total_ventas = 0

for producto in productos:
    vendidos = random.randint(0, 5)  # se simulan entre 0 y 5 ventas por producto
    producto.vender(vendidos)
    subtotal = vendidos * producto.precio
    total_ventas += subtotal
    print(f"{producto.nombre}: {vendidos} vendidos (${subtotal:.2f})")

print("\n--------------------------------")
print(f" TOTAL GENERADO EN VENTAS: ${total_ventas:.2f}")
print("--------------------------------")

# Mostrar inventario actualizado tras las ventas
print("\n Inventario restante tras ventas:")
for producto in productos:
    print(f"- {producto.nombre}: {producto.inventario} unidades restantes")

