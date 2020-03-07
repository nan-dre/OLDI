from PyQt5 import QtWidgets, uic
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, ui, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi(ui, self)

if __name__ == '__main__':      
    
    appctxt = ApplicationContext()
    ui = appctxt.get_resource('UIs\mainmenu.ui')
    
    main = MainWindow(ui)
    main.show()
    
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)