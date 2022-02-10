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
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction, QProgressBar,
    QTableView, QHeaderView, QDialogButtonBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QMessageBox
)
# PYQT5 - Elementos gráficos
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QFont
# Módulos y librerias necesarias para su correcto funcionamiento
import showDF
import unidades
# Clase VOLVER
#  Sirve para volver atrás un directorio
class Volver():
    def __init__(self, directorio_anterior, unidadIN, scrollArea, pbar, CURRENT_DIRECTORY, unidadInfoMostrar, filtroEx, filtroS):
        super(Volver, self).__init__()
        self.unidadIN = unidadIN
        self.scrollArea = scrollArea
        self.pbar = pbar
        self.CURRENT_DIRECTORY = CURRENT_DIRECTORY
        self.unidadInfoMostrar = unidadInfoMostrar
        self.filtroEx = filtroEx
        self.filtroS = filtroS
        self.directorio_anterior = directorio_anterior
    # Función VOLVERATRAS
    #  A través de la ruta recibida la descompone en los directorios y elimina el último para de esta forma volver un directorio atrás
    def volverAtras(self, path):
        unidadesLogicasX = unidades.Unidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        showDFX = showDF.ShowDF(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Reemplazamos los carácteres \\ por /
        pathB = path.replace('\\', "/")
        # Dividimos en trozos la ruta por el carácter /
        directorios = pathB.split("/")
        directoriosOK = []
        # Excluimos los directorios ''
        for x in range(len(directorios)):
            if directorios[x] != '':
                directoriosOK.append(directorios[x])
        # Borramos el último directorio
        directoriosOK.pop(-1)
        directorioPath = ""
        # Creamos la nueva ruta con los directorios
        for x in range(len(directoriosOK)):
            directorioPath += directoriosOK[x] + "/"
        # En el caso que el nuevo directorio tenga 3 letras
        if len(directorioPath) == 3:
            # Ejecutamos la función UNIDADESLOGICAS para que nos devuelva el widget y almacenamo su valor en WINDOW
            window = unidadesLogicasX.unidadesLogicas()
            self.scrollArea.setAlignment(Qt.AlignLeft)
            # Añadimos el widget WINDOW a SCROLLAREA
            self.scrollArea.setWidget(window)
        # En el resto de casos ejecutamos la función SHOWDF
        else:
            # Ejecutamos la función SHOWDF para que nos devuelva el widget y se lo asignamos a la variable WINDOW
            window = showDFX.showDF(directorioPath)
            self.scrollArea.setAlignment(Qt.AlignLeft)
            # Añadimos el widget WINDOW a SCROLLAREA
            self.scrollArea.setWidget(window)
    # Función VOLVER
    #  Sirve par volver atras desde el apartado INFOUNIDADES
    def volver(self, path):
        # Creamos un objeto de la clase SHOWDF
        showDFX = showDF.ShowDF(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Ejecutamos la función SHOWDF para que nos devuelva un widget que almacenamos en la variable WINDOW
        window = showDFX.showDF(path)
        self.scrollArea.setAlignment(Qt.AlignLeft)
        # Añadimos la variable WINDOW a SCROLLAREA
        self.scrollArea.setWidget(window)