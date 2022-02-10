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
#PYQT5 - Elemento gráficos
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction, QProgressBar,
    QTableView, QHeaderView, QDialogButtonBox, QComboBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QMessageBox
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QFont
import pandasModel
import extraerUR
import lsDirsFiles
# Clase SIZES
class Sizes():
    # Necesita dos parámetros para funcionar correctamente
    def __init__(self, filtroEx, filtroS):
        super(Sizes, self).__init__()
        self.filtroEx = filtroEx
        self.filtroS = filtroS

    # Función GETSIZE
    def getSize(self, start_path):
        # Creamos un objeto llamado LSDIRSFILESX
        lsDirsFilesX = lsDirsFiles.LsDirsFiles()
        # VARIABLES, ARRAYS
        data = []
        dataF = []
        numDirs = 0
        count = 0
        numFiles = ""
        sizes = 0
        e = 0
        # Bucle for escaneando la ruta que le hemos pasado
        for entry in os.scandir(start_path):
            # Añadimos el valor de la variable self.filtroEX a la variable EXTENSIONS
            extensions = [self.filtroEx]
            # En caso que sea un directorio ejecutamos la función GETSIZEDIRS
            if os.path.isdir(entry):
                # En caso que FILTROEX este vacío
                if self.filtroEx == "":
                        total, numFiles = self.getSizeDirs(entry.path)
                # En el caso que FILTROEX no este vacío
                else:
                    total, numFiles = self.getSizeDirs(entry.path)
            # En caso que sea un fichero añadimos al array DATA los datos RUTAOK, TOTAL, NUMFILES
            if os.path.isdir(entry):
                nombre = entry.path
                rutaOK = nombre.replace('\\',"/")
                data += [[rutaOK, total, numFiles]]
            numFiles = ""
        e = 0
        # Alcenamos en la variable FILES los archivos que hay en el path a través de la función LSFILES
        files = lsDirsFilesX.lsFiles(start_path)
        # Ejecutamos el bucle for para recorrer todos los ficheros
        for file in files:
                # En caso que el filtro esté en el nombre del archivo obtendremos el peso del archivo a través de PATH().STAT().ST_SIZE
                if self.filtroEx in file:
                    sizes = Path(file).stat().st_size
                    numFiles = 1
                    # En caso que el peso del archivo sea mayor o igual a self.filtroS se añade al arary DATAF los valores FILEOK, SIZES y  NUMFILES
                    if sizes >= self.filtroS:
                        nombre = file
                        fileOK = nombre.replace('\\',"/")
                        dataF += [[ fileOK, sizes, numFiles]]
        # Devuelve los arrays DATA y DATAF
        return data, dataF
    # Función GETSIZEDIRS
    def getSizeDirs(self, directory):
        # VARIABLES
        total = 0
        totalF = 0
        numFiles = 0
        numDirs = 0
        totalDF = 0
        # Ejectuamos un TRY - CATCH
        try:
            # Escaneamos el directorio a través de SCANDIR
            for entry in os.scandir(directory):
                #VARIABLES
                numFilesC = 0
                numDirsC = 0
                totalDirs = 0
                totalFiles = 0
                # En caso que SELF.FILTROEX sea ""
                if self.filtroEx == "":
                    # En caso que ENTRY sea un archivo sumanos 1 a NUMFILES, y sumamos el peso del archivo a TOTAL
                    if entry.is_file():
                        numFiles += 1
                        total += entry.stat().st_size
                    # En caso que ENTRY sea un directorio sumamos 1 a NUMDIRS, y sumamos el peso del directorio a TOTAL
                    elif entry.is_dir():
                        numDirs += 1
                        total += self.getSizeDir(entry.path)
                # En caso que SELF.FILTROEX sea diferente a "" y SELF.FILTROS sea diferente a 0
                elif self.filtroEx != "" and self.filtroS != 0:
                    # En caso que sea un fichero almacenamos el ENTRY.PATH en la variable nombre
                    if entry.is_file():
                        nombre = entry.path
                        # En caso que el SELF.FILTROEX esté en NOMBRE obtenemos el peso del archivo y lo almacenamo en TOTALF
                        if self.filtroEx in nombre:
                            totalF = totalF + entry.stat().st_size
                            # En caso que TOTALF sea mayor a SELF.FILTROS sumamos TOTALF a TOTAL
                            if totalF > self.filtroS:
                                total += totalF
                    # En caso que ENTRY sea un directorio obtenemos su peso mediante la función GETSIZEDIR y la almacenamo en la variable total
                    elif entry.is_dir():
                        total += self.getSizeDir(entry.path)
                        # Sumamos 1 al NUMDIRS
                        numDirs += 1
                # En el resto de casos
                else:
                    # En caso que ENTRY sea un archivo almacenamoe el valor de ENTRY.PATH en nombre
                    if entry.is_file():
                        nombre = entry.path
                        # En el caso que el valor e SELF.FILTROEX esté en NOMBRE sumamos a la variable total el peso del archivo
                        if self.filtroEx in nombre:
                            total += entry.stat().st_size
                    # En caso que ENTRY esa un directorio sumamos el peso del directorio a la variable TOTAL
                    elif entry.is_dir():
                        total += self.getSizeDir(entry.path)
                        # Sumamos 1 a NUMDIRS
                        numDirs += 1
                # Creamos un STRING con el valor de NUMDIRS y NUMFILES
                totalDF = "Carpetas: " + str(numDirs) + " Archivos: " + str(numFiles)
        # En caso que no sea un error de directorio
        except NotADirectoryError:
            return os.path.getsize(directory)
        # En caso de error de Permisos
        except PermissionError:
            return 0
        # Retornamos las variables TOTAL y TOTALDF
        return total, totalDF

    # Función GETSIZEDIRS
    # Sirve para devolver únicamente le peso de un directorio
    def getSizeDir(self, directory):
        # VARIABLES
        total = 0
        totalF = 0
        numFiles = 0
        # Ejecutamos un TRY - CATCH
        try:
            # En caso que sea un archivo
            if os.path.isfile(directory):
                # En el caso que FILTROEX sea igual a "" obtenemos el peso del archivo a través de la función GETSIZEFILE y lo sumamos a total
                if self.filtroEx == "":
                    total += self.getSizeFile(directory)
                # En el resto de casos
                else:
                    # Almacenamos el directorio en la variable NOMBRE
                    nombre = directory
                    # En el caso que el valor de SELF.FILTROEX esté en NOMBRE
                    if self.filtroEx in nombre:
                        # Sumamos a TOTALF el valor del peso del archivo a través de la función GETSIZEFILE
                        totalF = totalF + self.getSizeFile(nombre)
                        # En caos que TOTALF sea mayor a el valor de SELF.FILTROS asignamos el valor de TOTALF a TOTAL
                        if totalF > self.filtroS:
                            total = totalF
            # En el resto de casos que no sean un archivo
            else:
                # Ejecutamos un bucle for para escanear el directorio
                for entry in os.scandir(directory):
                    # En el caso que SELF.FILTROEX = ""
                    if self.filtroEx == "":
                        # En el caso que ENTRY sea un archivo obtenemos el peso del archivo y lo sumamos a la variable TOTAL
                        if entry.is_file():
                            total = total + entry.stat().st_size
                        # En el caso que ENTRY sea un directorio obtenemos el peso del directorio a través de la función GETSIZEDIR y sumamos el peso a TOTAL
                        elif entry.is_dir():
                            total = total + self.getSizeDir(entry.path)
                    # En el caso que SELF.FILTRO sea diferente a "" y SELF.FILTROS sea diferente a 0
                    elif self.filtroEx != "" and self.filtroS != 0:
                        # En caso que sea un archivo
                        if entry.is_file():
                            nombre = entry.path
                            # En el caso que SELF.FILTROEX esté en NOMBRE
                            if self.filtroEx in nombre:
                                # Sumamos el valor de archivo que obtenemos a través de la función GETSIZEFILE a la variable TOTALF
                                totalF = totalF + self.getSizeFile(nombre)
                                # En caso que TOTALF sea mayor al filtro SELF.FILTROS TOTAL pasa valer el valor de TOTALF
                                if totalF > self.filtroS:
                                    total = totalF
                        # En caso que sea un directorio
                        elif entry.is_dir():
                            # Sumamos el peso del diretorio obtenido a través de la función GETSIZEDIR y lo sumamos a TOTALD
                            totalD = totalD + self.getSizeDir(entry.path)
                            # En caso que TOTALD sea mayor a SELF.FILTROS asignamos el valor de TOTALD a TOTAL
                            if totalD > self.filtroS:
                                total = totalD
                    # En el resto de casos
                    else:
                        # En el caso que ENTRY sea un fichero
                        if entry.is_file():
                            nombre = entry.path
                            # Si SELF.FILTROEX está en NOMBRE
                            if self.filtroEx in nombre:
                                # Obtenemos el peso del archivo mediante ENTRY.STAT().ST_SIZE y lo sumamos a TOTAL
                                total = total + entry.stat().st_size
                        # En caso que sea ENTRY un directorio calculamos el peso del directorio a través de la función GETSIZEDIR y sumamo su peso a TOTAL
                        elif entry.is_dir():
                            total = total + self.getSizeDir(entry.path)
        # En caso que no sea ERROR de directorio
        except NotADirectoryError:
            return os.path.getsize(directory)
        # En caso que no sea ERROR de permisos
        except PermissionError:
            return 0
        # Retornamos el valor de TOTAL
        return total
    # Función GETNUMFILES
    # Obtenemos el número de archivos en un directorio
    def getNumFiles(self, directory):
        # VARIABLES
        total = 0
        totalF = 0
        numFiles = 0
        numDirs = 0
        totalFB = 0
        totalDirsB = 0
        # Escanemos el directorio
        for entry in os.scandir(directory):
            # En caso que SELF.FILTROEX sea igual a ""
            if self.filtroEx == "":
                # En caso que sea un archivo sumamos uno a NUMFILES
                if entry.is_file():
                    numFiles += 1
                # En caso que sea un directorio sumamos 1 a NUMDIRS
                elif entry.is_dir():
                    numDirs += 1
                    # Eejecutamos la funicón GETNUMDIRS y almacenmos el numero de directorios en NUMDIRSF
                    numDirsF = self.getNumDirs(entry.path)
                    # Sumamos NUMDIRSF a NUMDIRS
                    numDirs += numDirsF
            # En caso que SELF.FILTROEX sea diferente a "" o  SELF.FILTROS sea diferente a 0
            elif self.filtroEx != "" and self.filtroS != 0:
                # En caso que sa un archivo
                if entry.is_file():
                    nombre = entry.path
                    # En caso que el valor de SELF.FILTROEX esté en NOMBRE
                    if self.filtroEx in nombre:
                        # Obtenemos el peso del fichero y lo sumamos a TOTALF
                        totalF = totalF + entry.stat().st_size
                        # En caso que TOTALF seas mayor a SELF.FILTROS añadimos 1 a NUMFILES
                        if totalF > self.filtroS:
                            numFiles += 1
                # En caso que sea un directorio
                elif entry.is_dir():
                    # Sumamos 1 a NUMDIRS
                    numDirs += 1
                    # Obtenemos el númeor de archiov en el directorio a través e GETNUMDIRS
                    numDirsF = self.getNumDirs(entry.path)
                    # Sumamos NUMDIRSF a NUMDIRS
                    numDirs += numDirsF
            # En el resto de casos
            else:
                # En el caso que ENTRY sea un archivo
                if entry.is_file():
                    nombre = entry.path
                    # En caso que SELF.FILTROEX esté en NOMBRE sumamos 1 a NUMFILES
                    if self.filtroEx in nombre:
                        numFiles += 1
                # En caso que ENTY sea un directorio sumamos 1 a NUMDIRS
                elif entry.is_dir():
                    numDirs += 1
                    # Obtenemos el númeor de directorios a través de GETNUMDIRS y lo almacenamos en NUMDIRSF
                    numDirsF = self.getNumDirs(entry.path)
                    # Sumamos NUMDIRSF a NUMDIRS
                    numDirs += numDirsF
        # Creamos una variable STRING con los valores de NUMDIRS y NUMFILES
        totalNumFiles = "Carpetas: " + str(numDirs) + " Archivos: " + str(numFiles)
        # Retornamos el numero total de archivos
        return totalNumFiles
    # Función de GETNUMDIRS
    # Sirve para obtener el número de directorios
    def getNumDirs(self, directory):
        numDirs = 0
        # Ejecutamos un bucle for para que escanee el directorio
        for entry in os.scandir(directory):
            # En caso que SELF.FILTROEX sea igual a "" y sea un directorio sumamos 1 a NUMDIRS
            if self.filtroEx == "":
                if entry.is_dir():
                    numDirs += 1
            # En cso que SELF.FILTROEX sea diferente a "" y sea SELF.FILTROS diferente a 0
            elif self.filtroEx != "" and self.filtroS != 0:
                # En caso que ENTY sea un directorio sumamos a NUMDIRS 1
                if entry.is_dir():
                    numDirs += 1
            # En el resto de casos
            else:
                # Si ENTRY es un directorio sumamos 1 a NUMDIRS
                if entry.is_dir():
                    numDirs += 1
        # Retornamos el número de directorios
        return numDirs

    # Función GETSIZEFILES
    # Sirve para obtener el peso del archivo
    def getSizeFile(self, file):
        total = 0
        try:
            total = Path(file).stat().st_size
        except PermissionError:
            return 0
        return total