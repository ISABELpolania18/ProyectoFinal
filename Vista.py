import sys
#QFileDialog que es una ventana para abrir/guardar archivos
#QVBoxLayout es un organizador de widget en la ventana, este en particular los apila en vertical
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QMessageBox, QDialog
#ell layout es el organizador haciendo desde el codigo
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from matplotlib.figure import Figure
# Contenedor (canvas = lienzo) para graficos de Matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas #es la que mensajea los graficos
import scipy.io as sio
import numpy as np
import mysql
import mysql.connector as sql

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('Login.ui', self)
        self.setup()

    def setup(self):
        # Aquí se conectan los widgets directamente como ud quiere
        self.Boton_Ingresar.clicked.connect(self.ingresar)

    def ingresar(self):
        usuario = self.Usuario.text()
        contrasena = self.Contrasena.text()
        self.__mensajero.verificar_login(usuario, contrasena)
        
    def asignarCoordinador(self,c):
        self.__mensajero = c
        self.modelo = c.modelo

    class ventana_Senales(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            loadUi('Ventana_Senales.ui', self)
            self.setup()

        def setup(self):
            self.botonCSV.clicked.connect(self.abrir_ventana_csv)
            self.botonMAT.clicked.connect(self.abrir_ventana_mat)
            
        
        def abrir_ventana_csv(self):
            self.ventanaCSV = Ventana_CSV(self)
            self.ventanaCSV.asignarCoordinador(self.__mensajero)
            self.hide()  # Oculta la ventana de señales
            self.ventanaCSV.show()  # Muestra la ventana de CSV
        
        def abrir_ventana_mat(self):
            self.ventanaMAT = Ventana_MAT(self)
            self.ventanaMAT.asignarCoordinador(self.__mensajero)
            self.hide()  # Oculta la ventana de señales
            self.ventanaMAT.show()  # Muestra la ventana de MAT
        def asignarCoordinador(self, c):
            self.__mensajero = c
            self.modelo = c.modelo

    class ventana_Imagenes(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            loadUi('Ventana_Imagenes.ui', self)
            self.setup()

        def setup(self):
            self.botonDicom.clicked.connect(self.abrir_ventana_dicom)
            self.botonPNG.clicked.connect(self.abrir_ventana_png)
            
        
        def abrir_ventana_dicom(self):
            self.ventanaDICOM = Ventana_DICOM(self)
            self.ventanaDICOM.asignarCoordinador(self.__mensajero)
            self.hide()  # Oculta la ventana de señales
            self.ventanaDICOM.show()  # Muestra la ventana de CSV
        
        def abrir_ventana_png(self):
            self.ventanaPNG = Ventana_PNG(self)
            self.ventanaPNG.asignarCoordinador(self.__mensajero)
            self.hide()  # Oculta la ventana de señales
            self.ventanaPNG.show()  # Muestra la ventana de MAT
        def asignarCoordinador(self, c):
            self.__mensajero = c
            self.modelo = c.modelo

class Ventana_CSV(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaCSV.ui', self)
        self.__ventana_principal = parent
        self.setup()
    def setup(self):
        pass
    def asignarCoordinador(self, c):
        self.__mensajero = c

class Ventana_MAT(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaMAT.ui', self)
        self.__ventana_principal = parent
        self.setup()
    def setup(self):
        pass
    def asignarCoordinador(self, c):
        self.__mensajero = c

class Ventana_DICOM(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaDICOM.ui', self)
        self.__ventana_principal = parent
        self.setup()
    def setup(self):
        pass
    def asignarCoordinador(self, c):
        self.__mensajero = c

class Ventana_PNG(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaPNG.ui', self)
        self.__ventana_principal = parent
        self.setup()
    def setup(self):
        pass
    def asignarCoordinador(self, c):
        self.__mensajero = c


