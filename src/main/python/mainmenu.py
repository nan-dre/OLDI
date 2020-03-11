from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QHeaderView, QStackedLayout, QMainWindow, QWidget, QTabWidget, QPushButton, QLabel, QTableView, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import os
import sqlite3

'''
TODO 
implement ui for students tab
implement ui for borrows
create student add menu
create borrow creation menu
implement import excel tab
implement database selection
database backup
create new db from template
edit book
edit borrow
edit student
'''


class OLDIContext(ApplicationContext):

    @cached_property
    def window(self):
        self.ui = self.get_resource(r'UIs\main.ui')
        self.books_ui = self.get_resource(r'UIs\books.ui')
        self.students_ui = self.get_resource(r'UIs\students.ui')
        self.cur = self.db_connect
        return MainWindow(self.ui, self.books_ui, self.students_ui, self.cur)

    @cached_property
    def db_connect(self):
        try:
            con = sqlite3.connect(self.get_resource('DBs\Biblioteca.db'))
        except Error as e:
            print(e)
        return con.cursor()
        
    @cached_property
    def run_app(self):
        self.window.show()
        return self.app.exec_

class MainWindow(QMainWindow):

    def __init__(self, ui, books_ui, students_ui, cur):
        super(MainWindow, self).__init__()
        #uic.loadUi(ui, self)
        self.cur = cur
        self.books_ui = books_ui
        self.students_ui = students_ui
        

        cur.execute("SELECT * FROM borrows")
        self.borrows_data = cur.fetchall()


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

        layout.addWidget(Books(self.books_ui, self.cur))
        layout.addWidget(Students(self.students_ui, self.cur))
        layout.addWidget(Borrows())


        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        self.setWindowTitle('OLDI')
        self.showMaximized()

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self._data == []:
            return 0
        return len(self._data[0])

 
class Books(QWidget):
    def __init__(self, ui, cur):
        super(Books, self).__init__()

        uic.loadUi(ui, self)

        self.cur = cur
        cur.execute("SELECT * FROM books")
        
        self.model = TableModel(cur.fetchall())
        self.tableView.setModel(self.model)

        self.header = QHeaderView(Qt.Horizontal)
        self.header.setSectionResizeMode(3)

        self.tableView.setHorizontalHeader(self.header)
        
        for genre in self.get_genres():
            self.genre_combobox.addItem(str(genre[0]) + ' ' + genre[1])
        self.genre_combobox.setCurrentIndex(8)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

    def query(self):
        index = self.genre_combobox.currentIndex()
        self.cur.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND genre_id = ?",('%' + self.title_box.text() + '%' , '%' + self.name_box.text() + '%', index))
        data = self.cur.fetchall()
        self.model = TableModel(data)
        self.tableView.setModel(self.model)

    def get_genres(self):
        self.cur.execute('SELECT * from genres')
        return self.cur.fetchall()

class Students(QWidget):

    def __init__(self, ui, cur):
        super(Students, self).__init__()
        self.setAutoFillBackground(True)
        self.cur = cur
        
        uic.loadUi(ui, self)
        self.cur.execute("SELECT * FROM students")

        self.model = TableModel(cur.fetchall())
        self.tableView.setModel(self.model)

        self.header = QHeaderView(Qt.Horizontal)
        self.header.setSectionResizeMode(3)
        self.tableView.setHorizontalHeader(self.header)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())
    
    def query(self):
        self.cur.execute("SELECT * FROM students WHERE first_name LIKE ? AND last_name LIKE ? AND phone LIKE ?", ('%' + self.firstname_box.text() + '%', '%' + self.lastname_box.text() + '%', '%' + self.phone_box.text() + '%'))
        data = self.cur.fetchall()
        self.model = TableModel(data)
        self.tableView.setModel(self.model)

class Borrows(QLabel):

    def __init__(self):
        super(Borrows, self).__init__()
        self.setAutoFillBackground(True)

        self.setText("borrows")   



        

if __name__ == '__main__':  
    appctxt = OLDIContext()
    appctxt.run_app()