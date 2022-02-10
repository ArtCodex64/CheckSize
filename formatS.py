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

#CLASE FORMAT
class Format():
    def __init__(self):
        super(Format, self).__init__()
    #Función GETSIZEFORMAT
    #Le pasamos un parámetro en BYTES y nos devuelve su unidad más alta con 2 decimales
    def getSizeFormat(self, b, factor=1024, suffix="B"):
            for unit in [ "", "K", "M", "G", "T", "P", "E", "Z"]:
                if b < factor:
                    return f"{b:.2f}-{unit}{suffix}"
                b /= factor
            #Retorna el valor de la función GETSIZEFORMAT
            return f"{b:.2f}-{suffix}"