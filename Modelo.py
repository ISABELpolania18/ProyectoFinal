import mysql.connector
import mysql 

class Login:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="", 
            database="filesbank"
        )
        self.cursor = self.conexion.cursor()

    def validar_usuario(self, usuario, contrasena):
        buscar = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND Contraseña = %s"
        self.cursor.execute(buscar, (usuario, contrasena))
        return self.cursor.fetchone() # Devuelve una tupla con los datos del usuario si existe, o None si no existe


