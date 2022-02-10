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
# Módulos y librerias necesarias para el correcto funcionamiento
import pandasModel
import extraerUR
import showDF
import unidadesLogicasSize
import formatS
import windowSizeFunc
import lsDirsFiles
import windowSizeFunc
#Clase UNIDADES
# Sirve para mostrar las UNIDADESLOGICAS y para mostrar el peso de al unidad Y
class Unidades(QWidget):
    # Necesita recibir estos parámetros para su correcto funcionamiento
    def __init__(self, directorio_anterior, unidadIn, scrollArea, pbar, CURRENT_DIRECTORY, unidadInfoMostrar, filtroEx, filtroS):
        super(Unidades, self).__init__()
        self.setFixedHeight(300)
        self.pbar = pbar
        self.CURRENT_DIRECTORY = CURRENT_DIRECTORY
        self.unidadInfoMostrar = unidadInfoMostrar
        self.filtroEx = filtroEx
        self.filtroS = filtroS
        self.scrollArea = scrollArea
        self.unidadIN = unidadIn
        self.directorio_anterior = directorio_anterior
        self.windowSize = windowSizeFunc.WindowSizeFunc()
    # Función UNIDADESLOGICAS
    #  Lista las unidades lógicas
    def unidadesLogicas(self):
        # Elemento SCROLLAREA
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setAlignment(Qt.AlignLeft)
        # Creamos un objeto LAYOUTPROGRESSBAR de tipo QVBOXLAYOUT
        layoutVProgressBar = QVBoxLayout()
        # Creamos un objeto EXTRAER de la clase EXTRAERUR
        self.extraer = extraerUR.extraerUR()
        # Añadimos a LAYOUTVPROGRESSBAR el widget PBAR
        layoutVProgressBar.addWidget(self.pbar)
        # Creamos un objeto WINDOW de tipo QWIDGET
        window = QWidget()
        # Creamos un objeto llamado LAYOUTGENERAL de tipo QVBOXLAYOUT
        layoutGeneral = QVBoxLayout()
        # Creamos un objeto llamado LAYOUTUNITS de tipo QGRIDLAYOUT
        layoutUnits = QGridLayout()
        # Añadimos a LAYOUTGENERAL el layout LAYOUTVPROGRESSBAR
        layoutGeneral.addLayout(layoutVProgressBar)
        # En caso que sea WINDOWS
        if 'win' in sys.platform:
            # Creamos un objeto llamado SUBX de la clase EXTRAERUR
            self.subx = extraerUR.extraerUR()
            # Obtenemos las unidades y rutas a través de la función EXTRAER
            unidades,rutas = self.subx.extraer()
        #############################################################################
        # OBTENER LAS UNIDADES A TRAVÉS DE FSUTIL FSINFO DRIVES
            #storage = subprocess.getoutput('fsutil fsinfo drives')
            #unidades = storage.split(" ")
            #unidades.pop(0)
            #unidades.pop(-1)
        ##############################################################################
            num = math.ceil(len(unidades)/ 5)
            e = 0
            i = 0
            o = 0
            rutasUNI = []
            # Recorremos UNIDADES a través de un bucle FOR
            for x in unidades:
                # Damos forma a la ruta de las unidades
                uniGood = x + "/"
                ruta = rutas[o].replace("\\", "")
                # Creamos el nombre de la unidad con el carácter de la unidad más su nombre
                rutaMos = uniGood + " " + ruta
                # Creamos un objeto BUTTONUN de tipo QPUSHBUTTON
                buttonUn = QPushButton(QIcon("%s/icons/storage-device.png"  % self.CURRENT_DIRECTORY ), rutaMos)
                # Añadimos a RUTASUNI la ruta RUTAMOS
                rutasUNI.append(rutaMos)
                o += 1
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
                # BUTTONUN -> CLICKED.CONNECT -> Ejecutamos la funcón self.initShowDF cualdo pulsemos el botón
                buttonUn.clicked.connect(lambda _, uniGood=uniGood: self.initShowDF(uniGood))
                # Añadimos a LAYOUTUNITS el widget BUTTONUN
                layoutUnits.addWidget(buttonUn, e, i)
                i += 1
                if(i == 7):
                    e += 1
                    i = 0
            # Añadimos a SELF.UNIDADINFOMOSTRAR el valor de RUTASUNI
            self.unidadInfoMostrar = rutasUNI
        # En el caso que sea LINUX
        elif 'linux' in sys.platform:
            storage = subprocess.getoutput('df -h')
            unidad = storage.split(" ")
        # Añadimos a LAYOUTGENERAL el layout LAYOUTUNITS
        layoutGeneral.addLayout(layoutUnits)
        # Añadimos a WINDOW el layout LAYOUTGENERAL
        window.setLayout(layoutGeneral)
        # Retornamos el objeto WINDOW
        return window

    # Función PROGRESSBARULS
    #  Función para mostrar la PROGRESSBAR
    def progressBarULS(self):
        # Añadimos el background al SCROLLAREA
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setAlignment(Qt.AlignLeft)
        # Creamos un objeto LAYOUTUNITSV de tipo QHBOXLAYOUT
        self.layoutUnitsV = QHBoxLayout()
        # Creamos un objeto WINDOW de tipo QWIDGET
        window = QWidget()
        # Creamos un objeto de tipo QPUSHBUTTON
        cargar = QPushButton("Cargar")
        # Añadimos los estilos al QPUSHBUTTON
        cargar.setStyleSheet(
            "*{"+
            "width: 120px; " +
            "background-color: #006cac; " +
            "color: white; " +
            "}"
        )
        # CARGAR -> CLICKED.CONNECT -> Ejecutamos la función infoUnidadesMostrar al pulsar el botón
        cargar.clicked.connect(lambda _, x=self.pbar, y=self.scrollArea, z=window, w=self.layoutUnitsV: self.infoUnidadesMostrar(x,y,z,w))
        # Creamos un objeto LAYOUTUNITSV de tipo QVBOXLAYOUT
        layoutUnitsV = QVBoxLayout()
        # Centramos la PROGRESSBAR al centro
        self.pbar.setAlignment(Qt.AlignCenter)
        # Obtenemos el ancho de la pantalla con la función WINDOWSIZEWIDTH
        widthWin = self.windowSize.windowSizeWidth()
        # Añadimos a LAYOUTUNITSV el widget PBAR
        layoutUnitsV.addWidget(self.pbar)
        # Añadimos a LAYOUTUNITSV el widget CARGAR
        layoutUnitsV.addWidget(cargar)
        # Le damos un tamañao mínimo de ancho al objeto WINDOW
        window.setMinimumWidth(self.windowSize.windowSizeWidth() - 20)
        # Añadimos a el objeto WINDOW el layout LAYOUTUNITSV
        window.setLayout(layoutUnitsV)
        # Añadimos al SCROLLAREA el widget WINDOW
        self.scrollArea.setWidget(window)
    # Función INFOUNIDADESMOSTRAR
    #  Sirve para mostra el peso de la unidad Y
    def infoUnidadesMostrar(self, pbar, scrollArea, window, layoutPush):
        # Creamos un objeto con nombre LSDIRSFILESX de la clase LSDIRSFILES
        lsDirsFilesX = lsDirsFiles.LsDirsFiles()
        # Creamos un objeto SUBX de la clase EXTRAERUR
        self.subx = extraerUR.extraerUR()
        # Creamos un objeto FORMATOSX de la clase FORMAT
        formatSX = formatS.Format()
        # Creamos un objeto WINDOWNEW de tipo QWIDGET
        self.windowNew = QWidget()
        # Obtenemos las unidades a través de la función EXTRAER
        unidades,rutas = self.subx.extraer()
        # Creamos un objeto de nombre LAYOUTALLINFO de tipo QVBOXLAYOUT
        layoutAllInfo = QVBoxLayout()
        # Creamos un objeto de nombre LAYOUTPROGRESSBAR de tipo QVBOXLAYOUT
        layoutProgressBar = QVBoxLayout()
        # Creamos un objeto de nombre LAYOUTGENERAL de tipo QVBOXLAYOUT
        layoutGeneral = QVBoxLayout()
        # Creamos un objeto de nombre LAYOUTALL de tipo QVBOXLAYOUT
        layoutAll = QVBoxLayout()
        # VARIABLES
        total = 0
        num = 0
        dirsFiles = []
        # Indicamos únicamente la ruta Y
        dirsFiles = lsDirsFilesX.lsDirsFiles("Y:/")

        # Si el número de archivos y directorioes es menor o igual a 100 dividimos 101 por el número de archivos y directorios para
        # obtener el número por el cual multiplicar la variable x para que la PROGRESSBAR cargue correctamente en función de los archivos que tenga
        if len(dirsFiles) == 0:
                porcentOK = 1
                rangeVar = 1
        elif len(dirsFiles) <= 101:
            porcent = 101/len(dirsFiles)
            porcentOK = math.floor(porcent)
            rangeVar = 101
        # Si el número de archivos y directorioes es menor o igual a 100 dividimos 1001 por el número de archivos y directorios para
        # obtener el número por el cual multiplicar la variable x para que la PROGRESSBAR cargue correctamente en función de los archivos que tenga
        elif len(dirsFiles) > 101 and len(dirsFiles) <= 1001:
            porcent = 1001/len(dirsFiles)
            porcentOK = math.floor(porcent)
            rangeVar = 1001
        # Si el número de archivos y directorioes es menor o igual a 100 dividimos 1001 por el número de archivos y directorios para
        # obtener el número por el cual multiplicar la variable x para que la PROGRESSBAR cargue correctamente en función de los archivos que tenga
        elif len(dirsFiles) > 1001:
            porcent = 1001/len(dirsFiles)
            porcentOK = math.floor(porcent)
            rangeVar = 10001
        # Ejecutamos un bucle for para
        for x in range(rangeVar):
            time.sleep(0.05)
            #self.pbar.setValue(x)
            pbar.setValue(x*porcentOK)
            if x == len(dirsFiles):
                break
            # Creamos un objeto llamdo UNIDADESLOGSI de la clase UNIDADELOGICASSIZE
            unidadesLogSi = unidadesLogicasSize.UnidadesLogicasSize(dirsFiles[x], self.filtroEx, self.filtroS, self.CURRENT_DIRECTORY)
            # Ejecutamos lafunción UNIDADESLOGICASSIZE y almacenamos su resultados en las variables UNIDADESSIZE, PBARG, TOTALUNIDAD
            unidadesSize, pbarG, totalUnidad = unidadesLogSi.unidadesLogicasSize(window, layoutAllInfo, scrollArea, pbar)
            # Añadimos a LAYOUTGENERAL el layout UNIDADESSIZE
            layoutGeneral.addLayout(unidadesSize)
            # Sumamos a TOTAL el valor de TOTALUNIDAD
            total += totalUnidad
        # Ponemos el valor de la PBAR a 0
        pbar.setValue(0)
        # Formateamos el valor de TOTAL
        totalF = formatSX.getSizeFormat(total)
        # Creamos un objeto llamado UNIDADSIZE de tipo QLABEL
        unidadSize = QLabel("PESO TOTAL DE LA UNIDAD Y:/ " + str(totalF))
        # Añadimos los estilos al objeto UNIDADSIZE
        unidadSize.setStyleSheet(
            "*{" +
            "font-size: 18px; " + 
            "}"
        )
        # Añadimos a LAYOUTPROGRESSBAR el widget PBARG
        layoutProgressBar.addWidget(pbarG)
        # Añadimos a LAYOUTALL el layout LAYOUTPROGRESSBAR
        layoutAll.addLayout(layoutProgressBar)
        # Añadimos a LAYOUTALL el widget UNIDADSIZE
        layoutAll.addWidget(unidadSize)
        # Añadimos a LAYOUTALL el widget LAYOUTALLINFO
        layoutAll.addLayout(layoutAllInfo)
        # Añadimos a el widget WINDOWNEW el layout LAYOUTALL
        self.windowNew.setLayout(layoutAll)
        # Le asignamos un ancho minimo al objeto WINDOWNEW
        self.windowNew.setMinimumWidth(self.windowSize.windowSizeWidth() - 20)
        # Asignamos al SCROLLAREA el widget WINDOWNEW
        self.scrollArea.setWidget(self.windowNew)
        # Alineamos el SCROLLAREA a la izquierda
        self.scrollArea.setAlignment(Qt.AlignLeft)
    # Función INITSHOWDF
    #  Añadimos el widget que devuelve al SCROLLAREA
    def initShowDF(self, path):
        #UNIDADES LÓGICAS
        self.show = showDF.ShowDF(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Almacenamos el widget en el objeto WINDOWSDF
        windowSDF = self.show.showDF(path)
        self.scrollArea.setAlignment(Qt.AlignLeft)
        # Asignamos a SCROLLAREA el widget WINDOWSDF
        self.scrollArea.setWidget(windowSDF)
