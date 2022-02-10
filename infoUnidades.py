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
# PYQT5 - ELEMENTOS GRÁFICOS
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction, QProgressBar,
    QTableView, QHeaderView, QDialogButtonBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QMessageBox
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QFont
# Importamos los ficheros de los que depende el programa
import pandasModel
import extraerUR
import unidades
import windowSizeFunc
import formatS
import sizes
import infoUnidades
import lsDirsFiles
import volver
import showDF

#CLASE INFOUNIDADES
# Sirve para mostrar la información del directorio que se le pase como parámetro
# Calculará el peso de cada archivo, cuandos archivos y directorios hay en cada directorio.
# Nos permitirá filtrar los archivos por diferentes extensiones, ya sea por peso o por extensión
# Nos permite borrar los directorios o archivos seleccionados
class InfoUnidades():
    def __init__(self, directorio_anterior, unidadIN, scrollArea,  pbar, CURRENT_DIRECTORY, unidadInfoMostrar, filtroEx, filtroS):
        super(InfoUnidades, self).__init__()
        # VARIABLES de INFOUNIDADES
        self.pbar = pbar
        self.CURRENT_DIRECTORY = CURRENT_DIRECTORY
        self.unidadInfoMostrar = unidadInfoMostrar
        self.filtroEx = filtroEx
        self.filtroS = filtroS
        self.scrollArea = scrollArea
        self.unidadIN = unidadIN
        self.directorio_anterior = directorio_anterior
    # Función INFOUNIDADES
    def infoUnidades(self, unidad):
            # Creamos un objeto llamado VOLVERX de la clase VOLVER, le pasamos los parámetros necesarios para su correcto funcionamiento
            # Nos servirá para ejecutar las funciones de volver atrás cuando lo necesitemos
            volverX = volver.Volver(self.directorio_anterior, self.unidadIN, self.scrollArea,  self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
            # Creamos un objeto llamado SIZESX de la clase SIZES, le pasamos los parámetros necesarios para su correcto funcionamiento
            sizesX = sizes.Sizes(self.filtroEx, self.filtroS)
            # Creamos un objeto llamado WH de la clase WIDOWSIZEFUNC, no necesita ningún parámetro. Obtenemos el width y el height de la ventana
            wh = windowSizeFunc.WindowSizeFunc()
            # Creamos un layout VERTICAL
            layoutV = QVBoxLayout()
            # Añadimos la BARRA DE PROGRESO (pbar) al layout LAYOUTV
            layoutV.addWidget(self.pbar)
            # Creamos un objeto llamado TAM de tipo QLABEL
            tam = QLabel("Seleccionar tamaño:")
            # Cremos un desplegable para el tamaño
            self.comboBoxSize = QComboBox()
            # Añadimos los estilos al ComboBox
            self.comboBoxSize.setStyleSheet(
                "QComboBox"
                "{"
                "width: 50px;"
                "background-color: white;"
                "color: black;"
                "}"
                "QListView"
                "{"
                "width: 50px;"
                "background-color: white;"
                "color: black;"
                "}"
                )
            # Creamos un array llamado LISTASIZE con los diferentes valores que podrá filtrar por tamaño
            listaSize = ["---", "KB", "MB", "GB", "TB"]
            # Añadimos al COMBOBOX el array con los valores
            self.comboBoxSize.addItems(listaSize)
            # Creamos un objeto llamado EXT de valor QLABEL
            ext = QLabel("Seleccionar extensión:")
            # Creamos un desplegable para seleccionar la extensión
            self.comboBoxEx = QComboBox()
            # Asignamos los estilos al desplegable de las extensiones
            self.comboBoxEx.setStyleSheet(
                "QComboBox"
                "{"
                "width: 50px;"
                "background-color: white;"
                "color: black;"
                "}"
                "QListView"
                "{"
                "width: 50px;"
                "background-color: white;"
                "color: black;"
                "}"
                )
            # Creamos un array con las extensiones que tendrá el desplegable de EXTENSIONES
            listaEx = ["---","JPG","JPEG","PNG","PDF","TXT","TIFF"]
            # Añadimos los elementos que tendrá el desplegable de EXTENSIONES
            self.comboBoxEx.addItems(listaEx)
            # Creamos un botón QPUSHBUTTON que nos servirá para volver al apartado de UNIDADES DE ALMACENAMIENTO
            inicioBtn = QPushButton(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "")
            # Asignamos el ancho máximo de 50 al botón INICIOBTN
            inicioBtn.setMaximumWidth(50)
            # Asignamos el alto máximo de 5o al botón INICIOBTN
            inicioBtn.setMaximumHeight(50)
            # Asignamos los estilos al botón INICIOBTN
            inicioBtn.setStyleSheet(
                "*{"+
                "background-color: #ffffff;" +
                "color: #000000;"
                "}"
            )
            # INICIOBTN -> CLICKED.CONNECT -> Ejecutará la función self.initUnidadesLog al pulsarlo
            inicioBtn.clicked.connect(lambda _: self.initUnidadesLog())
            # ATRASBTN es un objeto de tipo QPUSHBUTTON
            # Sirve para volver un directorio atras
            atrasBtn = QPushButton(QIcon("%s/icons/back.png" % self.CURRENT_DIRECTORY ), "")
            # Asignamos un tamaño máximo de 50 de ancho
            atrasBtn.setMaximumWidth(50)
            # Asignamos un tamaño máximo de 50 de alto
            atrasBtn.setMaximumHeight(50)
            # Asignamos los estilos al objeto ATRASBTN
            atrasBtn.setStyleSheet(
                "*{"+
                "background-color: #ffffff;" +
                "color: #000000;"
                "}"
            )
            # INICIOBTN -> CLICKED.CONNECT -> Ejecutará la función self.initVolver al pulsarlo
            atrasBtn.clicked.connect(lambda _, x=unidad: self.initVolver(x))
            # info = subprocess.getoutput('fsutil volume diskfree %s' % unidad)
            info = ""
            # Creamos un objeto LINEE de tipo QLINEEDIT, es el input donde aparecerá la ruta donde buscar los directorios o archivos a filtrar
            self.lineE = QLineEdit()
            # Añadimos un texto al QLINEEDIT donde nos indica -> Introduce la ruta ...
            self.lineE.setPlaceholderText("Introduce la ruta ...")
            # Añadimos los estilos al QLINEEDIT
            self.lineE.setStyleSheet(
                "text-indent: 7px;" +
                "height: 18px;" +
                "background-color: #ffffff;" + 
                "color: #000000; " +
                "font-family: Roboto; " +
                "font-size: 12px"
            )
            # Creamos un objeto BUTTONS de tipo QPUSHBUTTON
            buttonS = QPushButton("Buscar")
            # BUTTONS -> CLICKED.CONNECT -> Ejecutará la función self.volverQLineEdit al pulsarlo
            buttonS.clicked.connect(self.valorQLineEdit)
            # Añadimos los estilos al objeto BUTTONS
            buttonS.setStyleSheet(
                "height: 18px;" +
                "background-color: #5985cb;" + 
                "color: white; " 
            )
            # Creamos un objeto BUTTOND de tipo QPUSHBUTTON
            buttonD = QPushButton("Borrar")
            # BUTTOND -> CLICKED.CONNECT -> Ejecutará la función self.confirmaciónD
            buttonD.clicked.connect(self.confirmacionD)
            # Añadimos los estilos al elemento BUTTOND
            buttonD.setStyleSheet(
                "height: 18px;" +
                "background-color: #ff0008;" + 
                "color: white; " 
            )
            # Ejecutamos la función GETSIZE y nos devuelve los directorios y los archivos con sus tamaños para pasarselo a PANDAS
            dirs, files = sizesX.getSize(unidad)
            # Pasamos la variable DIRS a pd.DataFrame
            df = pd.DataFrame(dirs, columns = ['DIR', 'SIZE[Bytes]','NUMBER OF FILES'])
            # Ordenamos mediante función SORT_VALUES a través de la columna SIZE['Bytes']
            dfSort = df.sort_values(by=['SIZE[Bytes]'], ascending=False)
            # Pasamos la variable FILES a pd.DataFrame
            dfi = pd.DataFrame(files, columns = ['FILES', 'SIZE[Bytes]','NUMBER OF FILES'])
            # Ordenamos mediante función SORT_VALUES a través de la columna SIZE['Bytes']
            dfiSort = dfi.sort_values(by=['SIZE[Bytes]'], ascending=False)
            #PANDAS MODEL
            # Creamos los modelos de pandas con su valores DFSORT y DFISORT
            self.model = pandasModel.pandasM(dfSort)
            self.modelF = pandasModel.pandasM(dfiSort)
            # Creamos un objeto view de tipo QTABLEVIEW
            self.view = QTableView()
            self.view.setSelectionBehavior(QTableView.SelectRows)
            # Ejecutamos la función ON_SELEC_CHANGE cuando seleccionan una fila en la tabla
            self.view.clicked.connect(self.on_selec_change)
            # Obtenemos el ancho a través de la función WINDOWSIZEWIDTH
            ancho = wh.windowSizeWidth()
            # Obtenemos el alto a través de la función WINDOWSIZEHEIGHT
            alto = wh.windowSizeHeight()
            # Añadimos el modelo a la QTABLEVIEW
            self.view.setModel(self.model)
            # Añadimos el ancho máximo de la tabla
            self.view.setMinimumWidth(ancho - 25)
            # Añadimos el alto mínimo de la tabla
            self.view.setMinimumHeight(int(alto / 2) - 150)
            # Añadimos el ancho de la columna 0
            self.view.setColumnWidth(0, int((ancho / 2)))
            # Añadimos el ancho de la columna 1
            self.view.setColumnWidth(1, int((ancho / 4)))
            # Añadimos el HEADER a la tabla QTABLEVIEW
            header = self.view.horizontalHeader()
            # Añadimos los estilos al HEADER del QTABLEVIEW
            header.setStyleSheet(
                "::section{ " +
                "background-color: #9b2f4d;" +
                "color: #ffffff; }"
            )
            header.setSectionResizeMode(QHeaderView.Interactive)
            header.setStretchLastSection(True)
            # Añadimos los estilos de la tabla QTABLEVIEW
            self.view.setStyleSheet(
                "*{background-color: #ffffff;"+
                "color: #000000; }"
            )
            # Creamos una nueva tabla de tipo QTABLEVIEW para mostrar la información de los ficheros
            self.viewF = QTableView()
            self.viewF.setSelectionBehavior(QTableView.SelectRows)
            # Ejecutamos la función de ON_SELEC_CHANGEF cuando seleccionamos una fila en la tabla de ficheros
            self.viewF.clicked.connect(self.on_selec_changeF)
            # Creamos una variable ANCHOF con la función WINDOWSIZEWIDTH
            anchoF = wh.windowSizeWidth()
            # Creamos una variable ALTOF con la función WINDOWSIZEHEIGHT
            altoF = wh.windowSizeHeight()
            # Añadimos el modelo a la tabla de los archivos
            self.viewF.setModel(self.modelF)
            # Asignamos el ancho mínimo de la tabla de los ficheros
            self.viewF.setMinimumWidth(anchoF - 25)
            # Añadimos el alto mínimo de la tabla de los ficheros
            self.viewF.setMinimumHeight(int(altoF/2) - 150)
            # Añadimos el ancho de la columna 0
            self.viewF.setColumnWidth(0, int((anchoF / 2)))
            # Añadimos el ancho de la columna 1
            self.viewF.setColumnWidth(1, int((anchoF / 4)))
            headerF = self.viewF.horizontalHeader()
            # Añadimos los estilos de la cabecera de la tabla de ficheros
            headerF.setStyleSheet(
                "::section{ " +
                "background-color: #9b2f4d;" +
                "color: #ffffff; }"
            )
            headerF.setSectionResizeMode(QHeaderView.Interactive)
            headerF.setStretchLastSection(True)
            # Añadimos los estilos a la tabla de los ficheros
            self.viewF.setStyleSheet(
                "*{background-color: #ffffff;"+
                "color: #000000; }"
            )
            # Creamos un objeto WINDOW de tipo QWIDGET
            window = QWidget()
            # Creamos un objeto LAYOUT de tipo QVBOXLAYOUT
            layout = QVBoxLayout()
            # Creamos un objeto LAYOUTHSD de tipo QHBOXLAYOUT
            layoutHSD = QHBoxLayout()
            # Creamos un objeto LABELINFO de tipo QLABEL
            labelInfo = QLabel(info)
            # Añadimos a LAYOUT el layout LAYOUTV
            layout.addLayout(layoutV)
            # Añadimos a LAYOUTHSD el widget INICIO BTN
            layoutHSD.addWidget(inicioBtn)
            # Añadimos a LAYOUTHSD el widget ATRASBTN
            layoutHSD.addWidget(atrasBtn)
            # Añadimos a LAYOUTHSD el widget LINEE
            layoutHSD.addWidget(self.lineE)
            # Añadimos a LAYOUTHSD el widget TAM
            layoutHSD.addWidget(tam)
            # Añadimos a LAYOUTHSD el widget COMBOBOXSIZE (Tamaño)
            layoutHSD.addWidget(self.comboBoxSize)
            # Añadimos a LAYOUTHSD el widget EXT
            layoutHSD.addWidget(ext)
            # Añadimos a LAYOUTHSD el widget COMBOBOXEX (Extensión)
            layoutHSD.addWidget(self.comboBoxEx)
            # Añadimos a LAYOUTHSD el widget BUTTONS
            layoutHSD.addWidget(buttonS)
            # Añadimos a LAYOUTHSD el widget BUTTOND
            layoutHSD.addWidget(buttonD)
            labelInfo.setAutoFillBackground(True)
            # Añadimos al LAYOUT el widget LABELINFO
            layout.addWidget(labelInfo)
            # Añadimos a LAYOUT el widget LAYOUTHSD
            layout.addLayout(layoutHSD)
            # Añadimos a LAYOUT el widget VIEW
            layout.addWidget(self.view)
            # Añadimos a LAYOUT el widget VIEWF
            layout.addWidget(self.viewF)
            # Añadimos a WINDOW el layout LAYOUT
            window.setLayout(layout)
            # Indicamos al SCROLLAREA que se alinee a la izquierda
            self.scrollArea.setAlignment(Qt.AlignLeft)
            # Añadimos a SCROLLAEREA el widget WINDOW
            self.scrollArea.setWidget(window)

    # Función initVolverAtras
    #  Ejecuta la función volverAtras para volver atras un directorio
    def initVolverAtras(self, path):
        self.volver = volver.Volver(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        self.volver.volverAtras(path)
    # Función initVolver
    #  Ejecuta la función volver para volver atras desde la interfaz de calcular
    def initVolver(self, path):
        self.volver = volver.Volver(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        self.volver.volver(path)
    # Función initUnidadesLog
    #  Ejecuta la función unidadesLogicas para mostrar el apartado unidadesLogicas
    def initUnidadesLog(self):
        self.unidades = unidades.Unidades(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Creamos un objeto llamado WH de la clase WIDOWSIZEFUNC, no necesita ningún parámetro. Obtenemos el width y el height de la ventana
        wh = windowSizeFunc.WindowSizeFunc()
        ancho = wh.windowSizeWidth()
        alto = wh.windowSizeHeight()
        window = self.unidades.unidadesLogicas()
        self.scrollArea.setAlignment(Qt.AlignLeft)
        self.scrollArea.setWidget(window)
    # Función on_selec_change
    #  Sirve para seleccionar la fila de la tabla directorios que seleccionemos
    def on_selec_change(self):
            index = self.view.currentIndex()
            newIndex = self.view.model().index(index.row(), 0)
            if newIndex is not None:
                self.lineE.setText(newIndex.data())
                self.removeRowX = newIndex
    # Función on_selec_changeF
    #  Sirve par seleccionar la fila de la tabla ficheros que seleccionemos
    def on_selec_changeF(self):
            index = self.viewF.currentIndex()
            newIndex = self.viewF.model().index(index.row(), 0)
            if newIndex is not None:
                self.lineE.setText(newIndex.data())
                self.removeRowX = newIndex

    # Función confirmacionD
    #  A la hora de borrar un directorio o un fichero nos mostrará una alerta indicando que confirmemos si queremos borrar o no los archivos
    def confirmacionD(self):
        # Creamos un objeto de la clase SHOWDF que nos servirá para mostrar el apartado que le indiquemos con el path
        showDFX = showDF.ShowDF(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Creamos un  objeto de tipo QMESSAGEBOX para que nos salte la alerta de confirmación
        msgBox = QMessageBox()
        # Colocamos el icono de borrar en la alerta
        msgBox.setIcon(QMessageBox.Information)
        # Añadimos el texto a la alerta de borrar directorio o fichero
        msgBox.setText("Borrar: %s" % self.lineE.text().strip())
        msgBox.setWindowTitle("Confirmación de borrado")
        # Añadimos los botones OK y CANCEL
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # Almacenamos en la variable returnValue el valor de OK o CANCEL y en caso que seleccionen OK ejecutará la acción
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            paok = ""
            DF = self.lineE.text().strip()
            sp = DF.replace('\\',"/")
            spp = sp.split("/")
            for x in range(len(spp)):
                if spp[x] == '':
                    spp.pop(x)
            
            for x in spp:
                paok += x + "/"
            # Si la ruta seleccionada es un directorio
            if os.path.isdir(paok):
                DFSd = paok.split("/")
                DFSd.pop(-1)
                DFSd.pop(-1)
                DFSsd = ""
                for x in DFSd:
                    DFSsd += x + "/"
                shutil.rmtree(DF)
                window = showDFX.showDF(DFSsd)
                self.scrollArea.setAlignment(Qt.AlignLeft)
                self.scrollArea.setWidget(window)
            # Si la ruta seleccionada es un archivo
            if os.path.isfile(DF):
                
                DFR = DF.replace('\\',"/")
                DFS = DFR.split("/")
                DFS.pop(-1)
                DFSs = ""
                for x in DFS:
                    DFSs += x + "/"
                DFSs[:-1]
                os.remove(DF)
                self.infoUnidades(DFSs)
    # Función VALORQLINEEDIT
    #  Sirve para comprobar los valores seleccionados de los COMBOBOX
    def valorQLineEdit(self):
        showDFX = showDF.ShowDF(self.directorio_anterior, self.unidadIN, self.scrollArea, self.pbar, self.CURRENT_DIRECTORY, self.unidadInfoMostrar, self.filtroEx, self.filtroS)
        # Almacenamos en la variable texto el valor de QLINEEDIT
        texto = self.lineE.text().strip()
        # Detectamos el valor de COMBOBOXSIZE y asignamos el valor de self.filtroS según su valor
        if self.comboBoxSize.currentIndex() == 0:
            self.filtroS = 0
        elif self.comboBoxSize.currentIndex() == 1:
            self.filtroS = 1024
        elif self.comboBoxSize.currentIndex() == 2:
            self.filtroS = 1024**2
        elif self.comboBoxSize.currentIndex() == 3:
            self.filtroS = 1024**3
        elif self.comboBoxSize.currentIndex() == 4:
            self.filtroS = 1024**4
        # Detectamos el valor de COMBOBOXEX y asignamos el valor de self.filtroEx según su valor
        if self.comboBoxEx.currentIndex() == 0:
            self.filtroEx = ""
        elif self.comboBoxEx.currentIndex() == 1:
            self.filtroEx = ".jpg"
        elif self.comboBoxEx.currentIndex() == 2:
            self.filtroEx = ".jpeg"
        elif self.comboBoxEx.currentIndex() == 3:
            self.filtroEx = ".png"
        elif self.comboBoxEx.currentIndex() == 4:
            self.filtroEx = ".pdf"
        elif self.comboBoxEx.currentIndex() == 5:
            self.filtroEx = ".txt"
        elif self.comboBoxEx.currentIndex() == 6:
            self.filtroEx = ".tiff"
        # En caso de que le QLINEEDIT no tenga texto nos mostrará un QMESSAGEBOX indicando que no hemos seleccionado ninguna ruta
        if texto == '':
            msgBox = QMessageBox()
            msgBox.setText("<RUTA> vacía, selecciona el archivo o la carpeta")
            msgBox.exec()
        # En caso que texto no sea ni un directorio ni un archivo nos mostrará un QMESSAGEBOX indicando ruta incorrecta
        elif os.path.isdir(texto) == False and os.path.isfile(texto) == False:
            msgBox = QMessageBox()
            msgBox.setText("Ruta: %s incorrecta" % texto)
            msgBox.exec()
        # En caso que el valor de los COMBOBOX sea 0 resetea el valor de self.filtroS y self.filtroEx
        else:
            if self.comboBoxSize.currentIndex() == 0 and self.comboBoxEx.currentIndex() == 0:
                self.filtroS = 0
                self.filtroEx = ""
                window = showDFX.showDF(texto)
                self.scrollArea.setAlignment(Qt.AlignLeft)
                self.scrollArea.setWidget(window)
            else:
                self.infoUnidades(texto)
        # Reseteamos el valor de los filtros
        self.filtroEx = ""
        self.filtroS = 0