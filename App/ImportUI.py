from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from import_module import excel_import
import sys

class ImportApp(QtWidgets.QWidget):
    def __init__(self, filetype):
        super().__init__()
        self.title = 'Import'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.openFileNameDialog(filetype)
        
        self.show()
    def openFileNameDialog(self, filetype):
        options = QFileDialog.Options()
        if filetype == 0: #Excel file
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Excel Files (*.xlsx)", options=options)
        elif filetype == 1: #DB file
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Database Files (*.db)", options=options)
        if fileName:
            return fileName
           


class ImportWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def get_excel(self):
        return ImportApp(0)
    def get_db(self):
        return ImportApp(1)
    def setupUi(self, ImportWindow):
        ImportWindow.setObjectName("ImportWindow")
        ImportWindow.resize(466, 518)
        self.centralwidget = QtWidgets.QWidget(ImportWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setText("Import Excel")
        self.label.setObjectName("Import_Excel")
        self.verticalLayout.addWidget(self.label)

        self.btn2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn2.setObjectName("Select")
        self.btn2.setText("Select Database")
        self.btn2.clicked.connect(self.get_db)
        self.verticalLayout.addWidget(self.btn2)

        self.btn1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn1.setObjectName("Select")
        self.btn1.setText("Select Excel")
        self.btn1.clicked.connect(self.get_excel)
        self.verticalLayout.addWidget(self.btn1)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMaxVisibleItems(15)
        self.comboBox.setObjectName("combobox")
        self.comboBox.insertItem(0,"GENERALITATI")
        self.comboBox.insertItem(1,"FILOSOFIE")
        self.comboBox.insertItem(2,"RELIGIE. MITOLOGIE")
        self.comboBox.insertItem(3,"STIINTE SOCIALE")
        self.comboBox.insertItem(4,"CLASA LIBERA")
        self.comboBox.insertItem(5,"STIINTE NATURALE")
        self.comboBox.insertItem(6,"STIINTE APLICATE")
        self.comboBox.insertItem(7,"ARTA. DISTRACTIE. SPORT")
        self.comboBox.insertItem(8,"LIMBA SI LITERATURA. LINGVISTICA")
        self.comboBox.insertItem(9,"ISTORIE. GEOGRAFIE")
        self.comboBox.insertItem(10,"MANUALE")
        self.comboBox.setCurrentIndex(8)
        self.verticalLayout.addWidget(self.comboBox)

        ImportWindow.setCentralWidget(self.centralwidget)
        ImportWindow.setWindowTitle("OLDI v0.1")

        self.menubar = QtWidgets.QMenuBar(ImportWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 466, 21))
        self.menubar.setObjectName("menubar")
        ImportWindow.setMenuBar(self.menubar)
        
        QtCore.QMetaObject.connectSlotsByName(ImportWindow)
        excel_import(self.get_db(), self.get_excel(), 8)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImportWindow()
    window.show()
    app.exec()