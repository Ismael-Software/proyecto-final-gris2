import mysql.connector
from mysql.connector import Error
import hashlib


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'cafeteria_db'
        self.user = 'root'
        self.password = ''  # Cambia por tu contraseña si es necesario

    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    result = cursor.fetchall()
                    return result
                else:
                    connection.commit()
                    return cursor.lastrowid
            except Error as e:
                print(f"Error ejecutando query: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None

    def autenticar_usuario(self, username, password):
        """Autentica usuario y devuelve sus datos"""
        query = "SELECT id, username, tipo, cliente_id, empleado_id FROM usuarios WHERE username = %s AND password = %s AND activo = 1"
        result = self.execute_query(query, (username, password))
        if result and len(result) > 0:
            return {
                'id': result[0][0],
                'username': result[0][1],
                'tipo': result[0][2],
                'cliente_id': result[0][3],
                'empleado_id': result[0][4]
            }
        return None

    def obtener_cliente_por_usuario(self, usuario_id):
        """Obtiene datos del cliente asociado al usuario"""
        query = """
        SELECT c.id, c.nombre 
        FROM cliente c 
        JOIN usuarios u ON c.id = u.cliente_id 
        WHERE u.id = %s
        """
        result = self.execute_query(query, (usuario_id,))
        if result and len(result) > 0:
            return {'id': result[0][0], 'nombre': result[0][1]}
        return None

    def actualizar_stock_producto(self, producto_id, nueva_cantidad):
        """Actualiza el stock de un producto"""
        query = "UPDATE producto SET stock = %s WHERE id = %s"
        return self.execute_query(query, (nueva_cantidad, producto_id))


# Instancia global de la base de datos
db = Database()