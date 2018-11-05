# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:31:24 2018

@author: BurakBey
"""

import cv2
 
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
    

class ExampleContent(QWidget):
    def __init__(self, parent,fileName):
        self.fileName = fileName
        self.parent = parent
               
        QWidget.__init__(self, parent)
        self.initUI(fileName)
        
    def initUI(self,fileName):        

        groupBox1 = QGroupBox('Input File')
        self.vBox1 = QVBoxLayout()
        groupBox1.setLayout(self.vBox1)
        self.setLayout(self.vBox1)
        self.setGeometry(0,0,0,0)
        
    def inputImage(self,fN,val):
        lab= QLabel()
        qp = QPixmap(fN)
        
        lab.setPixmap(qp)
        self.vBox1.addWidget(lab)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = "Histogram Matching"
        self.top = 50
        self.left = 50
        self.width = 1800
        self.height = 1200
        self.inImage = None
        self.inputFile = ''
        self.initWindow()
        self.inputFilled = False
        self.InputChannels = np.zeros((256,1,3), dtype='int32')

        
    def initWindow(self):
         
        #1st menu elements
        exitAct = QAction(QIcon('exit.png'), '&Exit' , self)
        importAct = QAction('&Open Input' , self)
        saveAct = QAction('&Save' , self)
        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        importAct.setStatusTip('Open Input')
        saveAct.setStatusTip('Save')
        
        exitAct.triggered.connect(self.closeApp)
        importAct.triggered.connect(self.importInput)
        saveAct.triggered.connect(self.saveAction)
        #2nd menu elements
        avFilters = QMenu('Average Filters',self)
        gauFilters = QMenu('Gaussian Filters',self)
        medFilters = QMenu('Median Filters',self)
        
        
        
        #1st submenu of filters
        #ampersands gave us a shortcut, with alt + underscored character
        avThreeX = QAction('&3x3', self)
        avThreeX.triggered.connect(self.avThreeXAction)
        
        avFiveX = QAction('&5x5', self)
        avFiveX.triggered.connect(self.avFiveXAction)
        
        avSevenX = QAction('&7x7', self)
        avSevenX.triggered.connect(self.avSevenXAction)
        
        avNineX = QAction('&9x9', self)
        avNineX.triggered.connect(self.avNineXAction)
        
        avElevenX = QAction('&11x11', self)
        avElevenX.triggered.connect(self.avElevenXAction)
        
        avThirteenX = QAction('&13x13', self)
        avThirteenX.triggered.connect(self.avThirteenXAction)
        
        avFifteenX = QAction('15x15', self)
        avFifteenX.triggered.connect(self.avFifteenXAction)
        
        avFilters.addAction(avThreeX)
        avFilters.addAction(avFiveX)
        avFilters.addAction(avSevenX)
        avFilters.addAction(avNineX)
        avFilters.addAction(avElevenX)
        avFilters.addAction(avThirteenX)
        avFilters.addAction(avFifteenX)
        
        #2nd submenu of filters

        gauThreeX = QAction('&3x3', self)
        gauThreeX.triggered.connect(self.gauThreeXAction)
        
        gauFiveX = QAction('&5x5', self)
        gauFiveX.triggered.connect(self.gauFiveXAction)
        
        gauSevenX = QAction('&7x7', self)
        gauSevenX.triggered.connect(self.gauSevenXAction)
        
        gauNineX = QAction('&9x9', self)
        gauNineX.triggered.connect(self.gauNineXAction)
        
        gauElevenX = QAction('&11x11', self)
        gauElevenX.triggered.connect(self.gauElevenXAction)
        
        gauThirteenX = QAction('&13x13', self)
        gauThirteenX.triggered.connect(self.gauThirteenXAction)
        
        gauFifteenX = QAction('15x15', self)
        gauFifteenX.triggered.connect(self.gauFifteenXAction)
        
        gauFilters.addAction(gauThreeX)
        gauFilters.addAction(gauFiveX)
        gauFilters.addAction(gauSevenX)
        gauFilters.addAction(gauNineX)
        gauFilters.addAction(gauElevenX)
        gauFilters.addAction(gauThirteenX)
        gauFilters.addAction(gauFifteenX)
        
        #3rd submenu of filters

        medThreeX = QAction('&3x3', self)
        medThreeX.triggered.connect(self.medThreeXAction)
        
        medFiveX = QAction('&5x5', self)
        medFiveX.triggered.connect(self.medFiveXAction)
        
        medSevenX = QAction('&7x7', self)
        medSevenX.triggered.connect(self.medSevenXAction)
        
        medNineX = QAction('&9x9', self)
        medNineX.triggered.connect(self.medNineXAction)
        
        medElevenX = QAction('&11x11', self)
        medElevenX.triggered.connect(self.medElevenXAction)
        
        medThirteenX = QAction('&13x13', self)
        medThirteenX.triggered.connect(self.medThirteenXAction)
        
        medFifteenX = QAction('15x15', self)
        medFifteenX.triggered.connect(self.medFifteenXAction)
        
        medFilters.addAction(medThreeX)
        medFilters.addAction(medFiveX)
        medFilters.addAction(medSevenX)
        medFilters.addAction(medNineX)
        medFilters.addAction(medElevenX)
        medFilters.addAction(medThirteenX)
        medFilters.addAction(medFifteenX)

        #3rd menu elements
        rotateMenu = QMenu('Rotate',self)
        scaleMenu = QMenu('Scale',self)
        translateMenu = QMenu('Translate',self)
        
        #1st submenu of geometric transforms
        rotateRight = QAction('&Rotate 10 Degree Right', self)
        rotateRight.triggered.connect(self.rotateRightAction)
        
        rotateLeft = QAction('&Rotate 10 Degree Left', self)
        rotateLeft.triggered.connect(self.rotateLeftAction)
        
        rotateMenu.addAction(rotateRight)
        rotateMenu.addAction(rotateLeft)
        
        #2nd submenu of geometric transforms
        
        scaleUp = QAction('&2x', self)
        scaleUp.triggered.connect(self.scaleUpAction)
        
        scaleDown = QAction('&1/2x', self)
        scaleDown.triggered.connect(self.scaleDownAction)
        
        scaleMenu.addAction(scaleUp)
        scaleMenu.addAction(scaleDown)
        
        #3rd submenu of geometric transforms
        
        translateRight = QAction('&Right', self)
        translateRight.triggered.connect(self.translateRightAction)
        
        translateLeft = QAction('&Left', self)
        translateLeft.triggered.connect(self.translateLeftAction)
        
        translateMenu.addAction(translateRight)
        translateMenu.addAction(translateLeft)
        
        self.statusBar()
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(importAct)
        fileMenu.addAction(saveAct)
        
        fileMenu = menubar.addMenu('&Filters')
        fileMenu.addMenu(avFilters)
        fileMenu.addMenu(gauFilters)
        fileMenu.addMenu(medFilters)
        
        fileMenu = menubar.addMenu('&Geometric Transforms')
        fileMenu.addMenu(rotateMenu)
        fileMenu.addMenu(scaleMenu)
        fileMenu.addMenu(translateMenu)

        self.content = ExampleContent(self, '')
        self.setCentralWidget(self.content)
        
        
        self.setWindowTitle(self.title)
        self.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
        self.setGeometry( self.top, self.left, self.width, self.height)
        self.show()

    
    def closeApp(self):
        sys.exit()
    
    def saveAction(self):
        self.inImage = cv2.cvtColor(self.inImage,cv2.COLOR_BGR2RGB)
        cv2.imwrite('output.png' , self.inImage)
    
    def importInput(self):
        fileName = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Png Files (*.png)")
        self.inputFile = fileName[0]
        self.inImage = cv2.imread(fileName[0])
        self.inImage = cv2.cvtColor(self.inImage,cv2.COLOR_BGR2RGB)
        self.content.inputImage(self.inputFile,self.InputChannels)

    def avThreeXAction(self):
        self.FilterAction('avg',3)
    def avFiveXAction(self):
        self.FilterAction('avg',5)
    def avSevenXAction(self):
        self.FilterAction('avg',7)
    def avNineXAction(self):
        self.FilterAction('avg',9)    
    def avElevenXAction(self):
        self.FilterAction('avg',11)
    def avThirteenXAction(self):
        self.FilterAction('avg',13)
    def avFifteenXAction(self):
        self.FilterAction('avg',15)
    
    def gauThreeXAction(self):
        self.FilterAction('gau',3)
    def gauFiveXAction(self):
        self.FilterAction('gau',5)
    def gauSevenXAction(self):
        self.FilterAction('gau',7)
    def gauNineXAction(self):
        self.FilterAction('gau',9)    
    def gauElevenXAction(self):
        self.FilterAction('gau',11)
    def gauThirteenXAction(self):
        self.FilterAction('gau',13)
    def gauFifteenXAction(self):
        self.FilterAction('gau',15)
        
    def medThreeXAction(self):
        self.FilterAction('med',3)
    def medFiveXAction(self):
        self.FilterAction('med',5)
    def medSevenXAction(self):
        self.FilterAction('med',7)
    def medNineXAction(self):
        self.FilterAction('med',9)    
    def medElevenXAction(self):
        self.FilterAction('med',11)
    def medThirteenXAction(self):
        self.FilterAction('med',13)
    def medFifteenXAction(self):
        self.FilterAction('med',15)
        
    def rotateRightAction(self):
        self.RotateAction('right')
    def rotateLeftAction(self):
        self.RotateAction('left')
    
    def scaleUpAction(self):
        self.ScaleAction(2)
    def scaleDownAction(self):
        self.ScaleAction(1/2)
    
    def translateRightAction(self):
        self.TranslateAction('right')
    
    def translateLeftAction(self):
        self.TranslateAction('left')
    
    def FilterAction(self,method,size):
        print(method)
        print(size)
        
    def RotateAction(self,type):
        print(type)
    def ScaleAction(self,coef):
        print(coef)
    def TranslateAction(self,type):
        print(type)
    
if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    cv2.destroyAllWindows()
    sys.exit(App.exec())
    