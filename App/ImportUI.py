# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Library_database.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(466, 518)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMaxVisibleItems(15)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 466, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Import Excel"))
        self.pushButton.setText(_translate("MainWindow", "Choose File"))
        self.comboBox.setCurrentText(_translate("MainWindow", "LIMBA SI LITERATURA. LINGVISTICA"))
        self.comboBox.setItemText(0, _translate("MainWindow", "GENERALITATI"))
        self.comboBox.setItemText(1, _translate("MainWindow", "FILOSOFIE"))
        self.comboBox.setItemText(2, _translate("MainWindow", "RELIGIE. MITOLOGIE"))
        self.comboBox.setItemText(3, _translate("MainWindow", "STIINTE SOCIALE"))
        self.comboBox.setItemText(4, _translate("MainWindow", "CLASA LIBERA"))
        self.comboBox.setItemText(5, _translate("MainWindow", "STIINTE NATURALE"))
        self.comboBox.setItemText(6, _translate("MainWindow", "STIINTE APLICATE"))
        self.comboBox.setItemText(7, _translate("MainWindow", "ARTA. DISTRACTIE. SPORT"))
        self.comboBox.setItemText(8, _translate("MainWindow", "LIMBA SI LITERATURA. LINGVISTICA"))
        self.comboBox.setItemText(9, _translate("MainWindow", "ISTORIE. GEOGRAFIE"))
        self.comboBox.setItemText(10, _translate("MainWindow", "MANUALE"))
    
    

