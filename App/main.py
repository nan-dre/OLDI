import sys
from PyQt5 import QtWidgets, uic

from ImportUI import Ui_MainWindow
from import_module import excel_import


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.retranslateUi(self)
app = QtWidgets.QApplication(sys.argv)

#excel_import(r'C:\Users\elev.LABS.000\Downloads\OLDI-master\App\Test1.db', r'C:\Users\elev.LABS.000\Downloads\OLDI-master\Data\20books.xlsx', 8)
window = MainWindow()
window.show()
app.exec()