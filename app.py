import sys
import subprocess
import os
import re
import math
from xml.dom.expatbuilder import parseString
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, 
    QLabel, QToolBar, QStatusBar, QPushButton, QGridLayout, QAction,
    QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

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
        self.resize(840, 600)

    def unidadesLogicas(self):
        window = QWidget()
        layoutUnits = QGridLayout()
        if 'win' in sys.platform:
            storage = subprocess.getoutput('fsutil fsinfo drives')
            unidades = storage.split(" ")
            unidades.pop(0)
            unidades.pop(-1)
            unidades.append("Z:/")
            unidades.append("Y:/")
            unidades.append("A:/")
            unidades.append("B:/")
            unidades.append("D:/")
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
                buttonUn.clicked.connect(lambda uniGood=uniGood: self.infoUnidades(uniGood))
                layoutUnits.addWidget(buttonUn, e, i)
                i += 1
                if(i == 5):
                    e += 1
                    i = 0
            
            #window.setFixedHeight(40 * num)

        elif 'linux' in sys.platform:
            storage = subprocess.getoutput('df -h')
            unidad = storage.split(" ")

        window.setLayout(layoutUnits)
        self.setCentralWidget(window)

    def infoUnidades(self, unidad):
        print(unidad)
        free = subprocess.getoutput('fsutil volume diskfree %s' % unidad)
        label = QLabel(free)
        window = QWidget()
        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        window.setLayout(layout)
        self.setCentralWidget(window)
        #uniEx = re.findall(r"\d*\,\d*", free)
        #tmUni = uniEx[0]
        #tmUni = tmUni.replace(",",".")
        #tmUni = float(tmUni)
        #tmLib = uniEx[1]
        #tmLibf = tmLib.replace(",",".")
        #tmLibf = float(tmLibf)
        #txt = tmUni - tmLibf
        #print(
        #    "Espacio utilizado: %.2f" % txt + " GB \n" +
        #    "Tamaño unidad: %.2f" % tmUni + " GB \n" +
        #    "Espacio libre: %.2f" % tmLibf + " GB \n"  
        #)


        

        



app = QApplication(sys.argv)
w = MainWindow()
w.setStyleSheet(
    "background-color: #1A2332;;"
)
w.show()
app.exec_()