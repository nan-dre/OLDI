from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QDialog, QDialogButtonBox
from import_module import excel_import
import sys

class WarningDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(WarningDialog, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Atentie")
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("verticalLayout")

        self.label = QtWidgets.QLabel()
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setText("Trebuie sa selectati fisierul excel si fisierul bazei de date.")
        self.label.setObjectName("Warning")
        self.layout.addWidget(self.label)    

        QBtn = QDialogButtonBox.Ok
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout.addWidget(self.buttonBox)


        
        
        self.setLayout(self.layout)

class ImportApp(QtWidgets.QWidget):
    def __init__(self, filetype):
        super().__init__()
        self.title = 'Import'
        self.filetype = filetype
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.openFileNameDialog(self.filetype)
        self.close()
    def openFileNameDialog(self, filetype):
        options = QFileDialog.Options()
        fileName = ''
        if filetype == 0: #Excel file
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Excel Files (*.xlsx)", options=options)
        elif filetype == 1: #DB file
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Database Files (*.db)", options=options)
        
        if fileName:
            return fileName
           


class ImportWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.excel_path = ''
        self.db_path = ''
        self.setupUi(self)

    def get_excel(self):
        self.excel_path = ImportApp(0)

    def get_db(self):
        self.db_path = ImportApp(1)

    def execute(self):
        if self.excel_path == '' or self.db_path == '':
            dlg = WarningDialog(self)
            dlg.exec()
        else:
            excel_import(self.db_path, self.excel_path, 8) #program ends here ------------------------------------------------


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

        self.btn1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn1.setObjectName("Select")
        self.btn1.setText("Select Excel")
        self.btn1.clicked.connect(self.get_excel)
        self.verticalLayout.addWidget(self.btn1)

        self.btn2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn2.setObjectName("Select")
        self.btn2.setText("Select Database")
        self.btn2.clicked.connect(self.get_db)
        self.verticalLayout.addWidget(self.btn2)

        self.btn3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn3.setObjectName("Execute")
        self.btn3.setText("Execute")
        self.btn3.clicked.connect(self.execute)
        self.verticalLayout.addWidget(self.btn3)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMaxVisibleItems(20)
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
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImportWindow()
    window.show()
    app.exec()