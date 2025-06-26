from Modelo import *
from Vista import *
print hola
class Controlador:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.vista.asignarCoordinador(self)

    def verificar_login(self, usuario, contrasena):
        datos = self.modelo.validar_usuario(usuario, contrasena)
        if datos:
            msg = QMessageBox(self.vista)
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Bienvenid@ {datos[0]} con rol: {datos[2]}")
            msg.setWindowTitle("Ingreso exitoso")
            msg.exec_() #para bloquear la ejecución hasta que el usuario haga clic en "Aceptar"
            if datos[2]=='Señales':
                self.ventana_senales = self.vista.ventana_Senales()
                self.ventana_senales.asignarCoordinador(self)
                self.vista.hide()  # Oculta la ventana de login
                self.ventana_senales.show()  # Muestra la ventana de señales
            elif datos[2]=='Imágenes':
                self.ventana_Imagenes = self.vista.ventana_Imagenes(self)
                self.ventana_Imagenes.asignarCoordinador(self)
                self.vista.hide()  # Oculta la ventana de login
                self.ventana_Imagenes.show()  # Muestra
        else:
            QMessageBox.warning(self.vista, "Error", "Usuario o contraseña incorrectos.")
        

    
def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    modelo = Login()
    controlador = Controlador(ventana, modelo)
    ventana.show()
    sys.exit(app.exec_())  
    
if __name__ == "__main__":
    main()   
