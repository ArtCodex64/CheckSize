import sys, time
import subprocess
import os
import re
import math
import ctypes
import threading
import pandas as pd
import shutil
from pathlib import Path
from os.path import join, getsize, abspath
from os import scandir
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction,
    QTableView, QHeaderView, QDialogButtonBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel, QMessageBox
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette
from modules.pandasModel import pandasModel
from modules.hilos import HiloGetSizeDirs, HiloGetSizeFile
from modules.extraerUR import extractU

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
        self.setWindowTitle("Check Size")
        self.setWindowIcon(QIcon(os.path.join(self.CURRENT_DIRECTORY, "icons/py-file-icon.png")))
        self.directorio_anterior = "Y:/"
        button_units = QAction(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "&Unidades", self)
        button_units.setStatusTip("Listar unidades de almacenamiento")
        button_units.triggered.connect(self.unidadesLogicas)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()
        menu.setStyleSheet(
            "background-color: #ffffff;" + 
            "color: #000000;"
        )
        

        lsUnits = menu.addMenu("&Archivos")
        lsUnits.addAction(button_units)
        self.resize(1020, 600)
        self.showMaximized()

    def unidadesLogicas(self):
        
        window = QWidget()
        layoutUnits = QGridLayout()
        if 'win' in sys.platform:
            storage = subprocess.getoutput('fsutil fsinfo drives')
            unidades = storage.split(" ")
            unidades.pop(0)
            unidades.pop(-1)

            num = math.ceil(len(unidades)/ 5)
            e = 0
            i = 0

            for x in unidades:
                uniGood = x.replace('\\',"/")
                buttonUn = QPushButton(QIcon("%s/icons/storage-device.png"  % self.CURRENT_DIRECTORY ), uniGood)
                buttonUn.setStyleSheet(
                    "*{" + 
                    "padding: 5px 12px;" + 
                    "background-color: #9fef00;" + 
                    "color: #000000;}" +
                    "*:hover{" +
                    "background-color: #dcff97;" + 
                    "}"
                )
                buttonUn.clicked.connect(lambda _, uniGood=uniGood: self.showDF(uniGood))
                layoutUnits.addWidget(buttonUn, e, i)
                i += 1
                if(i == 7):
                    e += 1
                    i = 0

        elif 'linux' in sys.platform:
            storage = subprocess.getoutput('df -h')
            unidad = storage.split(" ")

        window.setLayout(layoutUnits)
        self.scrollArea.setAlignment(Qt.AlignLeft)
        self.scrollArea.setWidget(window)
        self.setCentralWidget(self.scrollArea)

    def showDF(self, pathDF):
        windowDF = QWidget()
        layoutUnitsDF = QVBoxLayout()
        layoutUnitsV = QVBoxLayout()
        layoutUnitsH = QHBoxLayout()
        layoutUnitsInfo = QHBoxLayout()
        inicioBtn = QPushButton(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "")
        inicioBtn.setMaximumWidth(50)
        inicioBtn.setMaximumHeight(50)
        inicioBtn.setStyleSheet(
            "*{"+
            "background-color: #ffffff;" +
            "color: #000000;"
            "}"
        )
        inicioBtn.clicked.connect(lambda _, x=pathDF: self.unidadesLogicas())
        layoutUnitsInfo.addWidget(inicioBtn)
        atrasBtn = QPushButton(QIcon("%s/icons/back.png" % self.CURRENT_DIRECTORY ), "")
        atrasBtn.setMaximumWidth(50)
        atrasBtn.setMaximumHeight(50)
        atrasBtn.setStyleSheet(
            "*{"+
            "background-color: #ffffff;" +
            "color: #000000;"
            "}"
        )
        atrasBtn.clicked.connect(lambda _, x=pathDF: self.volverAtras(x))
        layoutUnitsInfo.addWidget(atrasBtn)
        widthWin = self.windowSizeWidth()
        info = ""
        
        if len(pathDF) == 3:
            info = subprocess.getoutput('fsutil volume diskfree %s' % pathDF)


        label = QLabel(info)
        layoutUnitsInfo.addWidget(label)

        dirs = self.lsDirsFiles(pathDF)
        for i in range(len(dirs)):
            dirs[i].replace('\\', "/")
            
        numDirs = 0
        numFiles = 0
        for x in dirs:
            if os.path.isdir(x):
                numDirs += 1
        for x in dirs:
            if os.path.isfile(x):
                numFiles += 1
        buttonCalculate = QPushButton(QIcon("%s/icons/calculator.png"  % self.CURRENT_DIRECTORY ), "Calcular")
        buttonCalculate.setMaximumWidth(200)
        buttonCalculate.setMaximumHeight(50)
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
        buttonCalculate.clicked.connect(lambda _, pathDF=pathDF: self.infoUnidades(pathDF))
        layoutUnitsDF.addWidget(buttonCalculate)

        arrayDirs = []
        arrayFiles = []
        for x in dirs:
            if os.path.isdir(x):
                sizeDir = self.getSizeDirs(x)
                sizeFormat = self.getSizeFormat(sizeDir)
                label = QLabel(sizeFormat)
                buttonUn = QPushButton(QIcon("%s/icons/folder-red.png" % self.CURRENT_DIRECTORY ), x)
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
                buttonUn.clicked.connect(lambda _, x=x:self.showDF(x))
                arrayDirs.append([buttonUn, label])
            elif os.path.isfile(x):
                sizeFile = self.getSizeFile(x)
                sizeFormat = self.getSizeFormat(sizeFile)
                label = QLabel(str(sizeFormat))
                buttonUn = QPushButton(QIcon("%s/icons/file-red.png" % self.CURRENT_DIRECTORY ), x)
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
                arrayFiles.append([buttonUn, label])

        for x in arrayDirs:
            layoutUnitsH = QHBoxLayout()
            layoutUnitsH.addWidget(x[0])
            layoutUnitsH.addWidget(x[1])
            layoutUnitsDF.addLayout(layoutUnitsH)

        for x in arrayFiles:
            layoutUnitsH = QHBoxLayout()
            layoutUnitsH.addWidget(x[0])
            layoutUnitsH.addWidget(x[1])
            layoutUnitsDF.addLayout(layoutUnitsH)

        layoutUnitsV.addLayout(layoutUnitsInfo)
        layoutUnitsV.addLayout(layoutUnitsDF)
        windowDF.setLayout(layoutUnitsV)
        windowDF.setMinimumWidth(int(widthWin * 0.75))
        self.scrollArea.setWidget(windowDF)
        self.setCentralWidget(self.scrollArea)
        self.scrollArea.setAlignment(Qt.AlignLeft)
    
    def infoUnidades(self, unidad):
        inicioBtn = QPushButton(QIcon("%s/icons/storage-device.png" % self.CURRENT_DIRECTORY ), "")
        inicioBtn.setMaximumWidth(50)
        inicioBtn.setMaximumHeight(50)
        inicioBtn.setStyleSheet(
            "*{"+
            "background-color: #ffffff;" +
            "color: #000000;"
            "}"
        )
        inicioBtn.clicked.connect(lambda _, x=unidad: self.unidadesLogicas())
        atrasBtn = QPushButton(QIcon("%s/icons/back.png" % self.CURRENT_DIRECTORY ), "")
        atrasBtn.setMaximumWidth(50)
        atrasBtn.setMaximumHeight(50)
        atrasBtn.setStyleSheet(
            "*{"+
            "background-color: #ffffff;" +
            "color: #000000;"
            "}"
        )
        atrasBtn.clicked.connect(lambda _, x=unidad: self.volverAtras(x))
        info = subprocess.getoutput('fsutil volume diskfree %s' % unidad)
        
        self.lineE = QLineEdit()
        self.lineE.setPlaceholderText("Introduce la ruta ...")
        self.lineE.setStyleSheet(
            "height: 18px;" +
            "background-color: #ffffff;" + 
            "color: #000000; "
        )
        buttonS = QPushButton("Buscar")
        
        buttonS.clicked.connect(self.valorQLineEdit)
        buttonS.setStyleSheet(
            "height: 18px;" +
            "background-color: #5985cb;" + 
            "color: white; " 
        )
        buttonD = QPushButton("Borrar")
        buttonD.clicked.connect(self.confirmacionD)
        buttonD.setStyleSheet(
            "height: 18px;" +
            "background-color: #ff0008;" + 
            "color: white; " 
        )

        dirs, files = self.getSize(unidad)
        df = pd.DataFrame(dirs, columns = ['DIR', 'SIZE','NUMBER OF FILES'])
        dfSort = df.sort_values(by=['SIZE'], ascending=False)
        dfi = pd.DataFrame(files, columns = ['FILES', 'SIZE','NUMBER OF FILES'])
        dfiSort = dfi.sort_values(by=['SIZE'], ascending=False)
        self.model = pandasModel(dfSort)
        self.modelF = pandasModel(dfiSort)
        #
        self.view = QTableView()
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.clicked.connect(self.on_selec_change)
        ancho = self.windowSizeWidth()
        alto = self.windowSizeHeight()
        self.view.setModel(self.model)
        self.view.setMinimumWidth(ancho - 125)
        self.view.setMinimumHeight(int(alto / 2) - 150)
        self.view.setColumnWidth(0, int((ancho / 2)))
        self.view.setColumnWidth(1, int((ancho / 4)))
        header = self.view.horizontalHeader()
        header.setStyleSheet(
            "::section{ " +
            "background-color: #9b2f4d;" +
            "color: #ffffff; }"
        )
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        self.view.setStyleSheet(
            "*{background-color: #ffffff;"+
            "color: #000000; }"
        )
        #
        self.viewF = QTableView()
        self.viewF.setSelectionBehavior(QTableView.SelectRows)
        self.viewF.clicked.connect(self.on_selec_changeF)
        anchoF = self.windowSizeWidth()
        altoF = self.windowSizeHeight()
        self.viewF.setModel(self.modelF)
        self.viewF.setMinimumWidth(anchoF - 125)
        self.viewF.setMinimumHeight(int(altoF/2) - 150)
        self.viewF.setColumnWidth(0, int((anchoF / 2)))
        self.viewF.setColumnWidth(1, int((anchoF / 4)))
        headerF = self.viewF.horizontalHeader()
        headerF.setStyleSheet(
            "::section{ " +
            "background-color: #9b2f4d;" +
            "color: #ffffff; }"
        )
        headerF.setSectionResizeMode(QHeaderView.Interactive)
        headerF.setStretchLastSection(True)
        self.viewF.setStyleSheet(
            "*{background-color: #ffffff;"+
            "color: #000000; }"
        )
        window = QWidget()
        layout = QVBoxLayout()
        layoutHSD = QHBoxLayout()
        labelInfo = QLabel(info)
        labelInfo.setStyleSheet(
            "{ color: green; }"
        )
        layoutHSD.addWidget(inicioBtn)
        layoutHSD.addWidget(atrasBtn)
        layoutHSD.addWidget(self.lineE)
        layoutHSD.addWidget(buttonS)
        layoutHSD.addWidget(buttonD)
        labelInfo.setAutoFillBackground(True)
        layout.addWidget(labelInfo)
        layout.addLayout(layoutHSD)
        layout.addWidget(self.view)
        layout.addWidget(self.viewF)
        window.setLayout(layout)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setWidget(window)
        self.setCentralWidget(self.scrollArea)

    def windowSizeWidth(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        ancho = user32.GetSystemMetrics(0)
        return ancho

    def windowSizeHeight(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        alto = user32.GetSystemMetrics(1)
        return alto


    def lsDirsFiles(self, ruta):
        if ruta != '':
            return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file() or arch.is_dir()]
        else:
            return ""
    
    def lsFiles(self, ruta):
        if ruta != '':
            return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file()]
        else:
            return ""
        

    def getSize(self, start_path):
        data = []
        dataF = []
        numDirs = 0
        for root, dirs, files in os.walk(start_path):
            dirs = root
            sizes = sum(getsize(join(root, name)) for name in files)
            sizeFormat = self.getSizeFormat(sizes)
            numFiles = len(files)
            data += [[dirs, sizeFormat, numFiles]]
            numDirs += 1
        e = 0
        files = self.lsFiles(start_path)
        for file in files:
            if file:
                sizes = Path(file).stat().st_size
                sizeFormat = self.getSizeFormat(sizes)
                numFiles = 1
                dataF += [[ file, sizeFormat, numFiles]]
            else:
                dataF = [["Nulo","0","0"]]

        return data, dataF

    def getSizeDirs(self, directory):
        total = 0
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.getSizeDirs(entry.path)
        except NotADirectoryError:
            return os.path.getsize(directory)
        except PermissionError:
            return 0
        return total
    def getSizeFile(self, file):
        total = 0
        try:
            total = Path(file).stat().st_size
        except PermissionError:
            return 0
        return total
    def getSizeFormat(self, b, factor=1024, suffix="B"):
        for unit in [ "", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}-{unit}{suffix}"
            b /= factor
        return f"{b:.2f}-{suffix}"
    def valorQLineEdit(self):
        texto = self.lineE.text().strip()
        self.showDF(texto)
    
    @QtCore.pyqtSlot()
    def on_selec_change(self):
            index = self.view.currentIndex()
            newIndex = self.view.model().index(index.row(), 0)
            if newIndex is not None:
                self.lineE.setText(newIndex.data())
                self.removeRowX = newIndex
    @QtCore.pyqtSlot()
    def on_selec_changeF(self):
            index = self.viewF.currentIndex()
            newIndex = self.viewF.model().index(index.row(), 0)
            if newIndex is not None:
                self.lineE.setText(newIndex.data())
                self.removeRowX = newIndex


    def confirmacionD(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Borrar: %s" % self.lineE.text().strip())
        msgBox.setWindowTitle("Confirmación de borrado")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            paok = ""
            DF = self.lineE.text().strip()
            sp = DF.replace('\\',"/")
            spp = sp.split("/")
            for x in range(len(spp)):
                if spp[x] == '':
                    spp.pop(x)
            
            print(spp)
            for x in spp:
                paok += x + "/"

            if os.path.isdir(paok):
                DFSd = paok.split("/")
                print(DFSd)
                DFSd.pop(-1)
                DFSd.pop(-1)
                DFSsd = ""
                for x in DFSd:
                    DFSsd += x + "/"
                shutil.rmtree(DF)
                self.showDF(DFSsd)
                
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
                
    def volver(self, path):
        self.showDF(path)

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    def volverAtras(self, path):
        if len(path) == 3:
            self.unidadesLogicas()
        else:
            pathB = path.replace('\\', "/")
            directorios = pathB.split("/")
            das = self.directorio_anterior.split("/")
            num = pathB.count("/")
            if num >= 2:
                if das[-1] == directorios[-1]:
                    directorios.pop(-1)
            
                if path[len(path)-1] != "/":
                    directorios.pop(-1)

                directorios.pop(-1)
                txtDirec = ""
                for i in range(len(directorios)):
                        txtDirec += directorios[i]+"/"
                
                self.directorio_anterior = txtDirec
                self.showDF(txtDirec)
            elif num == 1:
                letter = das[0] + "/"
                self.showDF(letter)
            else:
                self.unidadesLogicas()

            


app = QApplication(sys.argv)
w = MainWindow()
#if w.is_admin():
w.setStyleSheet(
    "background-color: #1A2332;"
)
w.show()
app.exec_()
#else:
#    print("Ejecuta el programa como administrador")