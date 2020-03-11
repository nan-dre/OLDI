from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QStackedLayout, QMainWindow, QWidget, QTabWidget, QPushButton, QLabel
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys  # We need sys so that we can pass argv to QApplication
import os
import sqlite3


class OLDIContext(ApplicationContext):

    @cached_property
    def window(self):
        self.ui = self.get_resource('UIs\main.ui')
        self.cur = db_connect()
        return MainWindow(self.ui, self.cur)

        
    @cached_property
    def run_app(self):
        self.window.show()
        return self.app.exec_

class Students(QLabel):

    def __init__(self):
        super(Students, self).__init__()
        self.setAutoFillBackground(True)

        self.setText("students")
        


class Books(QLabel):

    def __init__(self):
        super(Books, self).__init__()
        self.setAutoFillBackground(True)

        self.setText("books")


class Borrows(QLabel):

    def __init__(self):
        super(Borrows, self).__init__()
        self.setAutoFillBackground(True)

        self.setText("borrows")   

class MainWindow(QMainWindow):

    def __init__(self, ui, cur):
        super(MainWindow, self).__init__()
        #uic.loadUi(ui, self)
        self.setWindowTitle('OLDI')

        pagelayout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        layout = QtWidgets.QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(layout)


        books_btn = QPushButton('Carti')
        students_btn = QPushButton('Elevi')  
        borrows_btn = QPushButton('Inchirieri')

        button_layout.addWidget(books_btn)
        button_layout.addWidget(students_btn)
        button_layout.addWidget(borrows_btn)

        books_btn.pressed.connect(lambda: layout.setCurrentIndex(0))
        students_btn.pressed.connect(lambda: layout.setCurrentIndex(1))
        borrows_btn.pressed.connect(lambda: layout.setCurrentIndex(2))
        

        layout.addWidget(Students())
        layout.addWidget(Books())
        layout.addWidget(Borrows())


        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        

if __name__ == '__main__':  
    appctxt = OLDIContext()
    appctxt.run_app()