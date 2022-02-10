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
# PYQT5 - Elementos gráficos
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction, QProgressBar,
    QTableView, QHeaderView, QDialogButtonBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QMessageBox
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QFont
# Módulos y librerias necesarias para su correcto funcionamiento
import sizes
import formatS
import windowSizeFunc
# Clase UNIDADESLOGICASSIZE
#  Sirve para mostra el peso de cada directorio y va mostrandolo por pantalla
class UnidadesLogicasSize(QVBoxLayout, QWidget):
    def __init__(self, unidad, filtroEx, filtroS, CURRENT_DIRECTORY):
        super(UnidadesLogicasSize, self).__init__()
        self.CURRENT_DIRECTORY = CURRENT_DIRECTORY
        self.unidad = unidad
        self.filtroEx = filtroEx
        self.filtroS = filtroS
        self.CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    # Función UNIDADESLOGICASSIZE
    #  Muestra el tamaño de los directorios
    def unidadesLogicasSize(self, window, layoutHAll, scrollArea, pbar):
        # Crea un objet Window de tipo QWidget
        window = QWidget()
        # Crea un objeto de nombre SIZESX de la clase SIZES
        sizesX = sizes.Sizes(self.filtroEx, self.filtroS)
        # Crea un objeto de nombre FORMATSX de la clase FORMAT
        formatSX = formatS.Format()
        # Crea un objeto de nombre WINDOWSIZEX de la clase WINDOWSIZEFUNC
        windowSizeX = windowSizeFunc.WindowSizeFunc()
        # Crea un objeto llamado LAYOUTPROGRESSBAR de tipo QVBOXLAOUT
        layoutProgressBar = QVBoxLayout()
        # Crea un objeto llamdo LAYOUTPUSHX de tipo QHBOXLAYOUT
        layoutPushX = QHBoxLayout()
        # Crea un objeto llamado LAYOUTPUSHXX de tipo QHBOXLAYOUT
        layoutPushXX = QHBoxLayout()
        # Crea un objeto llamado LAYOUTPUSHXX de tipo QHBOXLAYOUT
        layoutGeneral = QVBoxLayout()
        # Crea un objeto llamado LAYOUTGENERAL de tipo QVBOXLAYOUT
        layoutSend = QHBoxLayout()
        # En caso que sea WINDOWS
        if 'win' in sys.platform:
            self.subx = self.unidad
        #####################################################################
        # OBTENER LAS RUTAS A TRAVÉS DE FSUTIL FSINFO DRIVES
            #unidades,rutas = self.subx.extraer()
            #storage = subprocess.getoutput('fsutil fsinfo drives')
            #unidades = storage.split(" ")
            #unidades.pop(0)
            #unidades.pop(-1)
        #####################################################################
            rutasUNI = []
            uniGood = self.subx
            rutaMos = uniGood
            # Creamos un objeto de nombre BUTTONUN de tipo QPUSHBUTTON
            buttonUn = QPushButton(QIcon("%s/icons/storage-device.png"  % self.CURRENT_DIRECTORY ), rutaMos)
            # Creamos un objeto de nombre BUTTONUNN de tipo QPUSHBUTTON
            buttonUnn = QPushButton(QIcon("%s/icons/storage-device.png"  % self.CURRENT_DIRECTORY ), rutaMos)
            # Añadimos a RUTASUNI el valor de RUTAMOS
            rutasUNI.append(rutaMos)
            # Añadimos los estilos a BUTTONUN
            buttonUn.setStyleSheet(
                    "*{" + 
                    "padding: 5px 12px;" + 
                    "background-color: #9fef00;" +
                    "text-align: left; " +
                    "color: #000000;}" +
                    "*:hover{" +
                    "background-color: #dcff97;" + 
                    "}"
                )
            # Añadimos los estilos a BUTTONUNN
            buttonUnn.setStyleSheet(
                    "*{" + 
                    "padding: 5px 12px;" + 
                    "background-color: #9b2f4d;" +
                    "text-align: left; " +
                    "color: #ffffff;}"
                )
            # Añadimos al layout LAYOUTPUSHX el widget BUTTONUN
            layoutPushX.addWidget(buttonUn)
            # Añadimos al layout LAYOUTPUSHXX el widget BUTTONUNN
            layoutPushXX.addWidget(buttonUnn)
            # Obtenemos el peso total de la unidad a través de la función GETSIZEDIR
            totalUnidad = sizesX.getSizeDir(uniGood)
            # Le damos formato a través de la función GETSIZEFORMAT
            totalUnidadFormat = formatSX.getSizeFormat(totalUnidad)
            # Creamos los labels que nos mostrarán la información de los directorios
            labelUnidad = QLabel(str(totalUnidadFormat))
            labelUnidadd = QLabel(str(totalUnidadFormat))
            # Añadimos los labels a sus correspondientes LAYOUTS
            layoutPushX.addWidget(labelUnidad)
            layoutPushXX.addWidget(labelUnidadd)
            # Añadimos la PROGRESSBAR al layout LAYOUTPROGRESSBAR
            layoutProgressBar.addWidget(pbar)
            # Añadimos los diferentes LAYOUTS a LAYOUTGENERAL
            layoutGeneral.addLayout(layoutProgressBar)
            layoutGeneral.addLayout(layoutPushXX)
            # Añadimos a LAYOUTHALL su correspondiente layout
            layoutHAll.addLayout(layoutPushX)
            # Añadimos a LAYOUTSEND el layout LAYOUTPUSHX
            layoutSend.addLayout(layoutPushX)
            # Añadimos al widget WINDOW el layout LAYOUTGENERAL
            window.setLayout(layoutGeneral)
            # Le damos un ancho mínimo al widget WINDOW
            window.setMinimumWidth(windowSizeX.windowSizeWidth() - 20)
            # Añadimos el widget WINDOW al SCROLLAREA
            scrollArea.setWidget(window)
            self.unidadInfoMostrar = rutasUNI
        # En caso que sea LINUX
        elif 'linux' in sys.platform:
            storage = subprocess.getoutput('df -h')
            unidad = storage.split(" ")
        # Devuelve los valores de LAYOUTSEND, PBAR, TOTALUNIDAD
        return layoutSend, pbar, totalUnidad