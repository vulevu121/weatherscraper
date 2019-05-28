# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WeatherScraperUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 511)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.browseSaveFolderButton = QtWidgets.QPushButton(self.tab)
        self.browseSaveFolderButton.setObjectName("browseSaveFolderButton")
        self.gridLayout.addWidget(self.browseSaveFolderButton, 2, 2, 1, 1)
        self.saveFolderLineEdit = QtWidgets.QLineEdit(self.tab)
        self.saveFolderLineEdit.setObjectName("saveFolderLineEdit")
        self.gridLayout.addWidget(self.saveFolderLineEdit, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startButton = QtWidgets.QPushButton(self.tab)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.saveHtmlButton = QtWidgets.QPushButton(self.tab)
        self.saveHtmlButton.setObjectName("saveHtmlButton")
        self.horizontalLayout.addWidget(self.saveHtmlButton)
        self.stopButton = QtWidgets.QPushButton(self.tab)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.csvFileLineEdit = QtWidgets.QLineEdit(self.tab)
        self.csvFileLineEdit.setObjectName("csvFileLineEdit")
        self.gridLayout.addWidget(self.csvFileLineEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.browseCsvFileButton = QtWidgets.QPushButton(self.tab)
        self.browseCsvFileButton.setObjectName("browseCsvFileButton")
        self.gridLayout.addWidget(self.browseCsvFileButton, 1, 2, 1, 1)
        self.ballParkJsonLineEdit = QtWidgets.QLineEdit(self.tab)
        self.ballParkJsonLineEdit.setObjectName("ballParkJsonLineEdit")
        self.gridLayout.addWidget(self.ballParkJsonLineEdit, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.browseBallParkJsonButton = QtWidgets.QPushButton(self.tab)
        self.browseBallParkJsonButton.setObjectName("browseBallParkJsonButton")
        self.gridLayout.addWidget(self.browseBallParkJsonButton, 0, 2, 1, 1)
        self.timerSpinBox = QtWidgets.QSpinBox(self.tab)
        self.timerSpinBox.setProperty("value", 10)
        self.timerSpinBox.setObjectName("timerSpinBox")
        self.gridLayout.addWidget(self.timerSpinBox, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.urlLineEdit = QtWidgets.QLineEdit(self.tab)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.horizontalLayout_2.addWidget(self.urlLineEdit)
        self.goButton = QtWidgets.QPushButton(self.tab)
        self.goButton.setObjectName("goButton")
        self.horizontalLayout_2.addWidget(self.goButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.parseButton = QtWidgets.QPushButton(self.tab_2)
        self.parseButton.setObjectName("parseButton")
        self.verticalLayout_4.addWidget(self.parseButton)
        self.parseFileEdit = QtWidgets.QLineEdit(self.tab_2)
        self.parseFileEdit.setObjectName("parseFileEdit")
        self.verticalLayout_4.addWidget(self.parseFileEdit)
        self.parseEdit = QtWidgets.QPlainTextEdit(self.tab_2)
        self.parseEdit.setObjectName("parseEdit")
        self.verticalLayout_4.addWidget(self.parseEdit)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Pitch File"))
        self.browseSaveFolderButton.setText(_translate("MainWindow", "..."))
        self.saveFolderLineEdit.setPlaceholderText(_translate("MainWindow", "Select the folder to save HTML files to..."))
        self.startButton.setToolTip(_translate("MainWindow", "Start pulling HTML files"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.saveHtmlButton.setToolTip(_translate("MainWindow", "Save HTML file to specified path"))
        self.saveHtmlButton.setText(_translate("MainWindow", "Save HTML"))
        self.stopButton.setToolTip(_translate("MainWindow", "Stop thread from pulling HTML files"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.csvFileLineEdit.setPlaceholderText(_translate("MainWindow", "Select pitch csv file..."))
        self.label_2.setText(_translate("MainWindow", "Output Folder"))
        self.browseCsvFileButton.setText(_translate("MainWindow", "..."))
        self.ballParkJsonLineEdit.setPlaceholderText(_translate("MainWindow", "Select ball park data in JSON..."))
        self.label_3.setText(_translate("MainWindow", "Ballpark Data"))
        self.browseBallParkJsonButton.setText(_translate("MainWindow", "..."))
        self.timerSpinBox.setToolTip(_translate("MainWindow", "Loading interval between pages (s)"))
        self.urlLineEdit.setPlaceholderText(_translate("MainWindow", "Website URL"))
        self.goButton.setText(_translate("MainWindow", "Go"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Get HTML"))
        self.parseButton.setText(_translate("MainWindow", "Parse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Parse"))


import WeatherScraper_rc
