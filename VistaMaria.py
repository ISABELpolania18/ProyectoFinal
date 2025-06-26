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
import pydicom
import os

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

class MyGraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MyGraphCanvas, self).__init__(self.fig)

    def graficar_imagen(self, datos):
        self.axes.clear()
        self.axes.imshow(datos, cmap='gray')
        self.axes.axis('off')
        self.draw()

class Ventana_DICOM(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaDICOM.ui', self)
        self.__ventana_principal = parent
        self.setup()
    def setup(self):
        self.botonCargarArchivos.clicked.connect(self.cargar_dicom)
        self.sliderZ.valueChanged.connect(self.corte_axial)
        self.sliderY.valueChanged.connect(self.corte_coronal)
        self.sliderX.valueChanged.connect(self.corte_sagital)

        self.volumen = None 
        self.sc = MyGraphCanvas(self, width=5, height=4, dpi=100)
        self.layoutImagen.addWidget(self.sc)
        pass
    def asignarCoordinador(self, c):
        self.__mensajero = c

    def cargar_dicom(self):
        carpeta = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta')
        archivos_dicom = [f for f in os.listdir(carpeta) if f.endswith('.dcm')]
        slices = []
        for archivo in archivos_dicom:
            path = os.path.join(carpeta, archivo)
            ds = pydicom.dcmread(path)
            slices.append(ds)
        #volumen
        slices.sort(key=lambda x: int(x.InstanceNumber))
        volumen = np.stack([ds.pixel_array for ds in slices])
        self.volumen = volumen
        #metadatos
        self.nombre_usuario = self.__mensajero.vista.Usuario.text()
        cod=123
        nombre = str(slices[0].get('PatientName', 'Anónimo'))
        id_= str(slices[0].get('PatientID', '0'))
        edad = str(slices[0].get('PatientAge', 'NA'))
        ruta = carpeta #no se si sería carpeta o solo path  

        self.labelNombre.setText(f"Nombre: {nombre}")
        self.labelID.setText(f"ID: {id_}")
        self.labelEdad.setText(f"Edad: {edad}")
        self.labelRuta.setText(f"Ruta: {ruta}")
        
        consulta = """
            INSERT INTO archivos_medicos 
            (nombre_usuario, cod_archivo, Nombre_Paciente, ID_Paciente, Edad_Paciente, Ruta_Dicom)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        cursor = self.__mensajero.modelo.cursor

        datos = (
            self.nombre_usuario,
            cod,
            nombre,
            id_,
            edad,
            ruta,
        )

        cursor.execute(consulta, datos)
        self.__mensajero.modelo.conexion.commit()

        profundidad, alto, ancho = self.volumen.shape
        self.sliderZ.setMinimum(0)
        self.sliderZ.setMaximum(profundidad - 1)
        self.sliderZ.setValue(profundidad // 2)

        self.sliderY.setMinimum(0)
        self.sliderY.setMaximum(alto - 1)
        self.sliderY.setValue(alto // 2)

        self.sliderX.setMinimum(0)
        self.sliderX.setMaximum(ancho - 1)
        self.sliderX.setValue(ancho // 2)

        # Mostrar corte axial
        img = self.volumen[profundidad // 2]
        self.sc.graficar_imagen(img)
        self.labelCorte.setText(f"Axial (Z): {profundidad // 2}")

    def corte_axial(self):
        if self.volumen is not None:
            z = self.sliderZ.value()
            self.sc.graficar_imagen(self.volumen[z])
            self.labelCorte.setText(f"Corte: {z}") 
    def corte_coronal(self):
        if self.volumen is not None:
            y = self.sliderY.value()
            self.sc.graficar_imagen(self.volumen[:,y,:])
            self.labelCorte.setText(f"Corte: {y}")
    def corte_sagital(self):
        if self.volumen is not None:
            x = self.sliderX.value()
            self.sc.graficar_imagen(self.volumen[:,:,x])
            self.labelCorte.setText(f"Corte: {x}")

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


