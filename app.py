import sys
import subprocess
import os
import re
import math
import ctypes
import threading
import pandas as pd
from pathlib import Path
from os.path import join, getsize, abspath
from os import scandir
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QLineEdit,
    QStatusBar, QPushButton, QGridLayout, QAction,
    QTableView, QHeaderView, QDialogButtonBox,
    QHBoxLayout, QVBoxLayout, QScrollArea, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette
from modules.pandasModel import pandasModel
from modules.hilos import HiloGetSizeDirs, HiloGetSizeFile

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.setWindowTitle("Check Size")
        self.setWindowIcon(QIcon("icons/py-file-icon.png"))
        button_units = QAction(QIcon("icons/storage-device.png"), "&Unidades", self)
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
                buttonUn = QPushButton(QIcon("icons/storage-device.png"), uniGood)
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
        layoutUnitsH = QHBoxLayout()
        widthWin = self.windowSizeWidth()
        dirs = self.lsDirsFiles(pathDF)
        numDirs = 0
        numFiles = 0
        for x in dirs:
            if os.path.isdir(x):
                numDirs += 1
        for x in dirs:
            if os.path.isfile(x):
                numFiles += 1
        
        buttonCalculate = QPushButton(QIcon("icons/calculator.png"), "Calcular")
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
                buttonUn = QPushButton(QIcon("icons/folder-red.png"), x)
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
                buttonUn = QPushButton(QIcon("icons/file-red.png"), x)
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
                buttonUn.clicked.connect(lambda _, x=x: self.infoUnidades(x))
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

        
        windowDF.setLayout(layoutUnitsDF)
        windowDF.setMinimumWidth(int(widthWin * 0.75))
        self.scrollArea.setWidget(windowDF)
        self.setCentralWidget(self.scrollArea)
    
    def infoUnidades(self, unidad):
        free = subprocess.getoutput('fsutil volume diskfree %s' % unidad)
        uniEx = re.findall(r"\d*\,\d*", free)
        tmUni = uniEx[1]
        tmUni = tmUni.replace(",",".")
        tmUni = float(tmUni)
        tmLib = uniEx[0]
        tmLibf = tmLib.replace(",",".")
        tmLibf = float(tmLibf)
        txt = tmUni - tmLibf
        
        info = "Espacio utilizado: %.2f" % txt + " GB | "
        info = info + "Tamaño unidad: %.2f" % tmUni + " GB | "
        info = info + "Espacio libre: %.2f" % tmLibf + " GB "
        
        lineE = QLineEdit()
        lineE.setStyleSheet(
            "height: 18px;" +
            "background-color: #ffffff;" + 
            "color: #000000; "
        )
        buttonS = QPushButton("Buscar")
        buttonS.setStyleSheet(
            "height: 18px;" +
            "background-color: #5985cb;" + 
            "color: white; " 
        )
        buttonD = QPushButton("Borrar")
        buttonD.setStyleSheet(
            "height: 18px;" +
            "background-color: #ff0008;" + 
            "color: white; " 
        )

        dirs, ndirs = self.getSize(unidad)
        df = pd.DataFrame(dirs, columns = ['DIR', 'SIZE(Bytes)','NUMBER OF FILES'])
        dfSort = df.sort_values(by=['SIZE(Bytes)'], ascending=False)
        model = pandasModel(dfSort)
        view = QTableView()
        ancho = self.windowSizeWidth()
        alto = self.windowSizeHeight()
        view.setModel(model)
        view.setMinimumWidth(ancho - 125)
        view.setMinimumHeight(alto - 400)
        view.setColumnWidth(0, int((ancho / 2)))
        view.setColumnWidth(1, int((ancho / 4)))
        header = view.horizontalHeader()
        header.setStyleSheet(
            "::section{ " +
            "background-color: #9b2f4d;" +
            "color: #ffffff; }"
        )
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        view.setStyleSheet(
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
        layoutHSD.addWidget(lineE)
        layoutHSD.addWidget(buttonS)
        layoutHSD.addWidget(buttonD)
        labelInfo.setAutoFillBackground(True)
        layout.addWidget(labelInfo)
        layout.addLayout(layoutHSD)
        layout.addWidget(view)
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
        return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file() or arch.is_dir()]

    def getSize(self, start_path):
        data = []
        numDirs = 0
        for root, dirs, files in os.walk(start_path):
            dirs = root
            sizes = sum(getsize(join(root, name)) for name in files)
            numFiles = len(files)
            data += [[dirs, sizes, numFiles]]
            numDirs += 1
        return data, numDirs
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
        
    

app = QApplication(sys.argv)
w = MainWindow()
w.setStyleSheet(
    "background-color: #1A2332;"
)
w.show()
app.exec_()