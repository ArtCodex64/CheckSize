# ------------------------------- #
#  INFORMACIÓN SOBRE EL PROGRAMA  #
# ------------------------------- #
#
# --------------------------------- #
#  Versión de Python: Python 3.10.1 #
# --------------------------------- #
#   
#
# -------------------- #
#  Fecha:  10-02-2022  #
# -------------------- #
#
# --------------------------- #
#  Autor:  ArtCodex64         #
# --------------------------- #
#
# ------------ #
# Descripción: # ----------------------------------------------------------------------------------------------------------------- #
#   Este programa sirve para listar las unidades de almacenamiento en red y borrar los archivos que no necesitemos.                #
#   También nos permite saber el peso de la unidad de almacenamiento Y.                                                            #
#   Podremos filtrar por diferentes extensiones de archivos (JPG, JPEG, PNG, TIFF, ...) y por su peso (Bytes, KB, MB, GB, TB)      #
#   Una vez obtenemos los archivos nos da la posibilidad de poder borrar el archivo o carpeta seleccionada.                        #
# -------------------------------------------------------------------------------------------------------------------------------- #
#
#
#
#
# --------------------- #
#  Librerias y módulos  #
# --------------------- #
#   Importamos las librerias y módulos necesarios para el correcto funcionamiento del programa en Python
import sys, time
import subprocess
import os
import re
import math
import ctypes
import threading
import pandas as pd
import shutil
import time
from pathlib import Path
from os.path import join, getsize, abspath
from os import scandir
#PYQT5 - ELEMENTOS GRÁFICOS
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction, QProgressBar,
    QTableView, QHeaderView, QDialogButtonBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QMessageBox
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QFont
#Importamos los ficheros de los que depende el programa
import pandasModel
import extraerUR
import unidades
#Clase principal MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #VARIABLES
        #SCROLL AREA -> Nos permite hacer scroll arriba y abajo en la ventana
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        #LAYOUTVPROGRESSBAR -> Es el layout en el cual añadiremos la barra de progreso, LAYOUT VERTICAL
        self.layoutVProgressBar = QVBoxLayout()
        #CURRENT_DIRECTORY -> Nos sirve para obtener la ruta total hasta el directorio del proyecto
        self.CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
        #SETWINDOWTITLE -> Sirve para poner el titulo que queramos al programa
        self.setWindowTitle("Check Size")
        #SETWINDOWINCON -> Sirve para poner el icono que queramos a la ventana del programa
        self.setWindowIcon(QIcon(os.path.join(self.CURRENT_DIRECTORY, "icons/py-file-icon.png")))
        #PROGRESS BAR -> Es la barra de progreso que nos mostrará el cargado de la nueva ventana
        self.pbar = QProgressBar()
        #SETALIGMENT -> Sirve para centrar la Barra de progreso en el centro
        self.pbar.setAlignment(Qt.AlignCenter)
        #DIRECTORIO-ANTERIOR -> Inicializamos el valor de directorio anteriror con el valor de Y:/
        self.directorio_anterior = "Y:/"
        #FILTROS -> Es el encargado de indicar el tamaño del archivo que vamos a filtrar, por defecto es 0
        self.filtroS = 0
        #FILTROEX -> Es el encargado de indicar la extensión del archivo que vamos a filtrar, por defecto está vacío
        self.filtroEx = ""
        self.operacion = 0
        self.unidadInfoMostrar = ""
        self.unidadIN = ""
        #BUTTON_UNITS -> Es el botón encargado de mostrar las unidades de red.
        button_units = QAction(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "&Unidades", self)
        button_units.setStatusTip("Listar unidades de almacenamiento")
        #BUTTON_UNITS -> TRIGGERED.CONNECT -> Llama a la función self.initUni cuando pulsamos el botón
        button_units.triggered.connect(self.initUni)
        #Button_UNITSINFO -> Es el botón encargado de mostrar el peso total de la unidad Y.
        button_unitsInfo = QAction(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "&Unidades info", self)
        button_unitsInfo.setStatusTip("Listar unidades de almacenamiento")
        #BUTTON_UNITSINFO -> TRIGGERED.CONNECT -> Llama a la función self.initUniSize cuando pulsamos el botón
        button_unitsInfo.triggered.connect(self.initUniSize)
        #SETSTATUSBAR -> Sirve para colocar el menú principal del programa
        self.setStatusBar(QStatusBar(self))
        #MENU -> Creamos un objeto de tipo menuBar()
        menu = self.menuBar()
        #ESTILOS para el menuBar
        menu.setStyleSheet(
            "background-color: #ffffff;" + 
            "color: #000000;"
        )
        
        #Añadimos al layout LAYOUTPROGRESSBAR el widget de la barra de progreso (self.pbar)
        self.layoutVProgressBar.addWidget(self.pbar)
        #LSUNITS -> Añadimos al menú el apartado Archivos para que nos liste Unidades y Unidades info
        lsUnits = menu.addMenu("&Archivos")
        #LSUNITS -> ADDACTION -> La función agrega la acción recién creada a la lista de acciones del menú y la devuelve
        lsUnits.addAction(button_units)
        lsUnits.addAction(button_unitsInfo)
        #Mostramos el contenido expandido al máximo, ocupando toda la pantalla
        self.showMaximized()

    def initUni(self):
        #UNIDADES LÓGICAS
        #Creamos un objetos de tipo UNIDADES, le pasamos los parámetros que necesita para crear el objeto correctamente
        self.unidadesLogicas = unidades.Unidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        #Ejecutamos la función de UNIDADESLOGICAS y alcenamos le objeto QWIDGET que nos devuelve en la variable WINDOW
        window = self.unidadesLogicas.unidadesLogicas()
        #Indicamos que el SCROLLAREA se alinee en el lado IZQUIERDO
        self.scrollArea.setAlignment(Qt.AlignLeft)
        #Añadimos el objeto WINDOW al SCROLLAREA
        self.scrollArea.setWidget(window)
        #Colocamos el SCROLLAREA en el WIDGET central
        self.setCentralWidget(self.scrollArea)

    def initUniSize(self):
        #UNIDADES LÓGICAS
        #Creamos un objetos de tipo UNIDADES, le pasamos los parámetros que necesita para crear el objeto correctamente
        self.unidadesLogicas = unidades.Unidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        #Ejecutamos la función de PROGRESSBARULS y alcenamos le objeto QWIDGET que nos devuelve en la variable WINDOW
        window = self.unidadesLogicas.progressBarULS()
        #Indicamos que el SCROLLAREA se alinee en el lado IZQUIERDO
        self.scrollArea.setAlignment(Qt.AlignLeft)
        #Añadimos el objeto WINDOW al SCROLLAREA
        self.scrollArea.setWidget(window)
        #Colocamos el SCROLLAREA en el WIDGET central
        self.setCentralWidget(self.scrollArea)

    def is_admin(self):
        #ISADMIN
        #Sirve para comprobar si el usuario que está ejecutando el programa es el administrador, no ejecutamos esta función por el momento
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
                

            

#Creamos un objeto llamado APP de tipo QApplication
app = QApplication(sys.argv)
#Creamos un objeto de la clase MainWindow (w)
w = MainWindow()
#Ejecutamos la función IS_ADMIN para comprobar cercionarnos que el usuario que ejecuta el programa es administrador
#if w.is_admin():
#Añadimos los estilos del objeto W, color de fondo
w.setStyleSheet(
    "background-color: #1A2332;"
)
#Mostramos el objeto W
w.show()
#Ejecutamos el programa
app.exec_()
#else:
#    print("Ejecuta el programa como administrador")