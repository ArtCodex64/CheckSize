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
# Módulos y librerias necesarias para el correcto funcionamiento de la clase
import pandasModel
import extraerUR
import unidades
import windowSizeFunc
import formatS
import sizes
import infoUnidades
import lsDirsFiles
import volver

# Clase SHOWDF
#  Sirve para mostrar los directorios y los ficheros con su correspondiente tamaño.
#  Nos permite y moviendonos por los diferentes directorios tanto para adelante como para atras.
#  Tenemos un botón CALCULAR donde nos permitirá interactuar con los archivos y directorios que seleccionemos
class ShowDF(QWidget):
    # Necesita que se le pase varios parámetros para su correcto funcionamiento
    def __init__(self, directorio_anterior, unidadIN, scrollArea,  pbar, CURRENT_DIRECTORY, unidadInfoMostrar, filtroEx, filtroS):
        super(ShowDF, self).__init__()
        #VARIABLES
        self.pbar = pbar
        self.CURRENT_DIRECTORY = CURRENT_DIRECTORY
        self.unidadInfoMostrar = unidadInfoMostrar
        self.filtroEx = filtroEx
        self.filtroS = filtroS
        self.scrollArea = scrollArea
        self.unidadIN = unidadIN
        self.directorio_anterior = directorio_anterior
    # Función SHOWDF
    #  Le pasamos la ruta y nos mostrará los archivos y directorios con su correspondiente peso
    def showDF(self, pathDF):
            # Le damos un color de fondo a SCROLLAREA
            self.scrollArea.setBackgroundRole(QPalette.Dark)
            # Alineamos el SCROLLAREA a la izquierda
            self.scrollArea.setAlignment(Qt.AlignLeft)
            # Creamos un objeto WINSIZEFUNC de la clase WINDOWSIZEFUNC
            self.winSizeFunc = windowSizeFunc.WindowSizeFunc()
            # Creamos un objeto FORMAT de la clase FORMAT
            self.format = formatS.Format()
            # Creamos un objeto SIZES de la clase SIZES
            self.sizes = sizes.Sizes(self.filtroEx, self.filtroS)
            # Creamos un objeto UNIDADES de la clase UNIDADES
            self.unidades = unidades.Unidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
            # Creamos un objeto INFOUN de la clase INFOUNIDADES
            self.infoUn = infoUnidades.InfoUnidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
            # Creamos un objeto LSDIRSFILESX de la clase LSDIRSFILES
            self.lsDirsFilesX = lsDirsFiles.LsDirsFiles()
            # Ejecutamos un bucle for para almacenar los valores de UNIDADINFOMOSTRAR en UNIDADIN
            for x in range(len(self.unidadInfoMostrar)):
                if pathDF in self.unidadInfoMostrar[x]:
                    self.unidadIN = self.unidadInfoMostrar[x]

            z = slice(0,2)
            unidadL = self.unidadIN[z]
            widthWin = self.winSizeFunc.windowSizeWidth()
            # Creamos un LABELUIF de tipo QPUSHBUTTON
            labelUIF = QPushButton(self.unidadIN)
            # Ejecutamos la función self.showDF al pulsar en LABELUIF
            labelUIF.clicked.connect(lambda _, x=unidadL: self.initShowDF(x))
            # Añadimos un ancho mínimo de 500
            labelUIF.setMinimumWidth(500)
            # Añadimos un alto mínimo de 34
            labelUIF.setMinimumHeight(34)
            # Añadimos los estilos de LABELUIF
            labelUIF.setStyleSheet(
                "*{" +
                "background-color: #8ec641;" +
                "color: #111927;" +
                "font-weight: bold;" +
                "font-size: 18px;" +
                "text-align: left; " +
                "padding-left: 7px; "
                "}"
            )
            # Creamos un objeto WINDOWDF de tipo QWIDGET
            windowDF = QWidget()
            # Creamos un objeto LAYOUTUNITSDF de tipo QVBOXLAYOUT
            layoutUnitsDF = QVBoxLayout()
            # Creamos un objeto LAYOUTUNITSV de tiop QVBOXLAYOUT
            layoutUnitsV = QVBoxLayout()
            # Creamos un objeto LAYOUTUNITSH de tipo QHBOXLAYOUT
            layoutUnitsH = QHBoxLayout()
            # Creamos un objeto LAYOUTUNITSHUIC de tipo QHBOXLAYOUT
            layoutUnitsHUIC = QHBoxLayout()
            # Creamos un objeto LAYOUTUNITSINFO de tipo QHBOXLAYOUT
            layoutUnitsInfo = QHBoxLayout()
            # Creamos un objeto de tipo QPUSHBUTTON
            inicioBtn = QPushButton(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "")
            # Añadimos un ancho máximo de 50
            inicioBtn.setMaximumWidth(50)
            # Añadimos un alto máximo de 50
            inicioBtn.setMaximumHeight(50)
            # Añadimos los estilos al objeto INICIOBTN
            inicioBtn.setStyleSheet(
                "*{"+
                "background-color: #ffffff;" +
                "color: #000000;"
                "}"
            )
            # INICIOBTN -> CLICKED.CONNECT -> Ejecutará la función self.initUndadesLog al pulsar el botón
            inicioBtn.clicked.connect(lambda _, x=pathDF: self.initUnidadesLog())
            # Añadimos a LAYOUTUNITSINFO el widget INICIOBTN
            layoutUnitsInfo.addWidget(inicioBtn)
            # Creamos un objeto ATRASBTN de tipo QPUSHBUTTON
            atrasBtn = QPushButton(QIcon("%s/icons/back.png" % self.CURRENT_DIRECTORY ), "")
            # Añadimos un ancho de 50 al objeto ATRASBTN
            atrasBtn.setMaximumWidth(50)
            # Añadimos un alto de 50 al objeto ATRASBTN
            atrasBtn.setMaximumHeight(50)
            # Añadimos los estilos al objeto ATRASBTN
            atrasBtn.setStyleSheet(
                "*{"+
                "background-color: #ffffff;" +
                "color: #000000;"
                "}"
            )
            # ATRASBTN -> CLICKED.CONNECT -> Ejecutará la función self.initVolverAtras al pulsar el botón
            atrasBtn.clicked.connect(lambda _, x=pathDF: self.initVolverAtras(x))
            # Añadimos a LAYOUTUNITSINFO el widget ATRASBTN
            if len(pathDF) > 3:
                layoutUnitsInfo.addWidget(atrasBtn)
            info = ""
            
            # En caso que el tamaño del PATH sea de 3 ejecutamos el siguiente comando y lo mostramos
            if len(pathDF) == 3:
                info = subprocess.getoutput('fsutil volume diskfree %s' % pathDF)

            # Creamos un objeto llamado LABEL de tipo QLABEL
            label = QLabel(info)
            # Añadimos a LAYOUTUNITSINFO el widget LABEL
            layoutUnitsInfo.addWidget(label)
            # Ejecutamos la función LSDIRSFILES y almacenamos su valor en la variable DIRS
            dirs = self.lsDirsFilesX.lsDirsFiles(pathDF)
            # Reemplazamos los carácteres \\ por /
            for i in range(len(dirs)):
                dirs[i].replace('\\', "/")
                
            numDirs = 0
            numFiles = 0
            # Contamos el número de directorios
            for x in dirs:
                if os.path.isdir(x):
                    numDirs += 1
            # Contamos el número de ficheros
            for x in dirs:
                if os.path.isfile(x):
                    numFiles += 1
            # Creamos un objeto llamado BUTTONCALCULATE de tipo QPUSHBUTTON
            buttonCalculate = QPushButton(QIcon("%s/icons/calculator.png"  % self.CURRENT_DIRECTORY ), "Calcular")
            # Añadimos un ancho máximo de 200 al objeto BUTTONCALCULATE
            buttonCalculate.setMaximumWidth(200)
            # Añadimos un alto máximo de 34 al objeto BUTTONCALCULATE
            buttonCalculate.setMaximumHeight(34)
            # Añadimos los estilos del objeto BUTTONCALCULATE
            buttonCalculate.setStyleSheet(
                        "*{" + 
                        "padding: 5px 12px;" + 
                        "background-color: #9b2f4d;" + 
                        "color: #ffffff;" +
                        "text-align: left; }" + 
                        "*:hover{" +
                        "background-color: #f31451;" +
                        "color: #000000;" +
                        "}"
                    )
            # BUTTONCALCULATE -> CLICKED.CONNECT -> Ejecutarás la función self.infoUn.infoUnidades al pulsar el botón
            buttonCalculate.clicked.connect(lambda _, pathDF=pathDF: self.infoUn.infoUnidades(pathDF))
            # Alinemos el layout LAYOUTUNITSHUIC a la IZQUIERDA
            layoutUnitsHUIC.setAlignment(Qt.AlignLeft)
            # Añadimos a LAYOUTUNITSHUIC el objeto LABELUIF
            layoutUnitsHUIC.addWidget(labelUIF)
            # Añadimos a LAYOUTUNITSHUIC el objeto BUTTONCALCULATE
            layoutUnitsHUIC.addWidget(buttonCalculate)
            # Creamos un arrayDirs
            arrayDirs = []
            # Creamos un arrayFiles
            arrayFiles = []
            text = " "
            u = 0
            uu = 0
            # Si el número de archivos y directorioes es menor o igual a 100 dividimos 101 por el número de archivos y directorios para
            # obtener el número por el cual multiplicar la variable x para que la PROGRESSBAR cargue correctamente en función de los archivos que tenga
            if len(dirs) == 0:
                porcentOK = 1
                rangeVar = 1
            elif len(dirs) <= 101:
                porcent = 101/len(dirs)
                porcentOK = math.floor(porcent)
                rangeVar = 101
            # Si el número de archivos y directorioes es menor o igual a 100 dividimos 1001 por el número de archivos y directorios para
            # obtener el número por el cual multiplicar la variable x para que la PROGRESSBAR cargue correctamente en función de los archivos que tenga
            elif len(dirs) > 101 and len(dirs) <= 1001:
                porcent = 1001/len(dirs)
                porcentOK = math.floor(porcent)
                rangeVar = 1001
            # Si el número de archivos y directorioes es menor o igual a 100 dividimos 1001 por el número de archivos y directorios para
            # obtener el número por el cual multiplicar la variable x para que la PROGRESSBAR cargue correctamente en función de los archivos que tenga
            elif len(dirs) > 1001:
                porcent = 1001/len(dirs)
                porcentOK = math.floor(porcent)
                rangeVar = 10001
            # Ejecutamos un bucle for para
            for x in range(rangeVar):
                time.sleep(0.05)
                # Actualizamos la PROGRESSBAR
                self.pbar.setValue(x*porcentOK)
                # Cuando x llegue al número de archivos y directorios sale del bucle
                if x == len(dirs):
                    break
                # En caso que dirs[x] sea un directorio
                if os.path.isdir(dirs[x]):
                    # Obtiene el peso del directorio y el número de archivos a través de la función GETSIZEDIRS
                    sizeDir, numFiles = self.sizes.getSizeDirs(dirs[x])
                    # Formatea el peso del directorio a su unidad más cercana (Bytes, KB, MB, GB, ...)
                    sizeFormat = self.format.getSizeFormat(sizeDir)
                    # Creamos un objeto llamado LABEL de tipo QLABEL
                    label = QLabel(sizeFormat)
                    # Creamos un objeto llamado BUTTONUN de tipo QPUSHBUTTON
                    buttonUn = QPushButton(QIcon("%s/icons/folder-red.png" % self.CURRENT_DIRECTORY ), dirs[x])
                    # Agregamos los estilos a BUTTONUN
                    buttonUn.setStyleSheet(
                        "*{" + 
                        "padding: 5px 12px;" + 
                        "background-color: #141D2B;" + 
                        "color: #9fef00;" +
                        "text-align: left; }" + 
                        "*:hover{" +
                        "background-color: #dcff97;" +
                        "color: #000000;" +
                        "}"
                    )
                    # BUTTONUN -> CLICKED.CONNECT -> Ejectua la función self.initShowDF cualdo pulsemo el botón
                    buttonUn.clicked.connect(lambda _, x=x:self.initShowDF(dirs[x]))
                    # Añadimos el objeto BUTTONUN al array ARRAYDIRS
                    arrayDirs.append([buttonUn, label])
                # En caso que dirs[x] sea un archivo
                elif os.path.isfile(dirs[x]):
                    # Obtenemos el peso del archivo a través de la función GETSIZEFILE y lo almacenamos en la variable SIZEFILE
                    sizeFile = self.sizes.getSizeFile(dirs[x])
                    # Formatea el peso del archivo a su unidad más cercana (Bytes, KB, MB, GB, ...)
                    sizeFormat = self.format.getSizeFormat(sizeFile)
                    # Creamos un objeto llamado LABEL de tipo QLABEL
                    label = QLabel(str(sizeFormat))
                    # Creamos un objeto llamado BUTTONUN de tipo QPUSHBUTTON
                    buttonUn = QPushButton(QIcon("%s/icons/file-red.png" % self.CURRENT_DIRECTORY ), dirs[x])
                    # Añadimos los estilos al QPUSHBUTTON
                    buttonUn.setStyleSheet(
                        "*{" + 
                        "padding: 5px 12px;" + 
                        "background-color: #141D2B;" + 
                        "color: #9fef00; " +
                        "text-align: left; }" + 
                        "*:hover{" +
                        "background-color: #dcff97;" + 
                        "color: #000000; " +
                        "}"
                    )
                    # Añadimos el objeto BUTTONUN al array ARRAYFILES
                    arrayFiles.append([buttonUn, label])
            # Ejecutamos un bucle for para añadir los BOTONES (directorios) al LAYOUTUNITSH
            for x in arrayDirs:
                layoutUnitsH = QHBoxLayout()
                layoutUnitsH.addWidget(x[0])
                layoutUnitsH.addWidget(x[1])
                layoutUnitsDF.addLayout(layoutUnitsH)
            # Ejecutamos un bucle for para añadir los BOTONES (ficheros) al LAYOUTUNITSH
            for x in arrayFiles:
                layoutUnitsH = QHBoxLayout()
                layoutUnitsH.addWidget(x[0])
                layoutUnitsH.addWidget(x[1])
                layoutUnitsDF.addLayout(layoutUnitsH)
            # Ponemos el valor de la PROGRESSBAR a 0
            self.pbar.setValue(0)
            # Añadimos la PROGRESSBAR a LAYOUTUNITSV
            layoutUnitsV.addWidget(self.pbar)
            # Añadimos LAYOUTUNITSINFO a LAYOUTUNITSV
            layoutUnitsV.addLayout(layoutUnitsInfo)
            # Añadimos LAYOUTUNITSHUIC a LAYOUTUNITSV
            layoutUnitsV.addLayout(layoutUnitsHUIC)
            # Añadimos LAYOUTUNITSDF a LAYOUTUNITSV
            layoutUnitsV.addLayout(layoutUnitsDF)
            # Añadimos LAYOUTUNITSV a WINDOWDF
            windowDF.setLayout(layoutUnitsV)
            # Le damos un ancho mínimo a WINDOWDF
            windowDF.setMinimumWidth(int(widthWin-10))
            # Retornamos el objeto WINDOWDF
            return windowDF
    # Función INITSHOWDF
    def initShowDF(self, path):
        # Creamos un objeto SHOW para que nos devuelva un QWIDGET y podamos asignarselo al SCROLLAREA
        show = ShowDF(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        windowSDF = show.showDF(path)
        # Alinaemoa el SCROLLAREA a la IZQUIERDA
        self.scrollArea.setAlignment(Qt.AlignLeft)
        # Asignamos el objeto SHOW al SCROLLAREA
        self.scrollArea.setWidget(windowSDF)
    # Función INITVOLVERATRAS
    def initVolverAtras(self, path):
        # Creamos un objeto VOLVER para ejecutar la función VOLVERATRAS que nos permitirá volver un directorio atras
        self.volver = volver.Volver(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Ejecutamos la función VOLVERATRAS y le pasamos la ruta
        self.volver.volverAtras(path)
    # Función INITUNIDADESLOG
    def initUnidadesLog(self):
        # Creamos un objeto UNIDADES para poder ejecutar la función UNIDADESLOGICAS que nos devolverá un elemento QWIDGET
        self.unidades = unidades.Unidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Ejecutamos la función UNIDADESLOGICAS y almacenamos el elemento QWIDGET que nos devuelve en el objeto WINDOW
        window = self.unidades.unidadesLogicas()
        # Alineamos SCROLLAREA a la IZQUIERDA
        self.scrollArea.setAlignment(Qt.AlignLeft)
        # Añadimos el objeto WINDOW al SCROLLAREA
        self.scrollArea.setWidget(window)
