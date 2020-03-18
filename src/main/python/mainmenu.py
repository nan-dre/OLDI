from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidget, QCompleter, QDialog, QHeaderView, QStackedLayout, QMainWindow, QWidget, QTabWidget, QPushButton, QLabel, QTableView, QShortcut
from PyQt5.QtCore import Qt, QDate, QPoint, QModelIndex
from PyQt5.QtGui import QKeySequence
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import os
import sqlite3
from datetime import date

'''
TODO 
implement ui for students tab - check
implement ui for borrows - check
create student dialog - make dialog ui

change query function for borrow

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
        self.borrows_ui = self.get_resource(r'UIs\borrows.ui')
        self.add_borrow_ui = self.get_resource(r'UIs\add_borrow.ui')
        self.student_dialog = self.get_resource(r'UIs\student_dialog.ui')
        self.borrow_dialog = self.get_resource(r'UIs\borrow_dialog.ui')
        self.cur = self.db_connect
        return MainWindow(self.con, self.cur, self.ui, self.books_ui, self.students_ui, self.borrows_ui, self.add_borrow_ui, self.student_dialog, self.borrow_dialog)

    @cached_property
    def db_connect(self):
        try:
            self.con = sqlite3.connect(self.get_resource('DBs\Biblioteca.db'))
        except Error as e:
            print(e)
        return self.con.cursor()
        
    @cached_property
    def run_app(self):
        self.window.show()
        return self.app.exec_

class MainWindow(QMainWindow):

    def __init__(self, con, cur, ui, books_ui, students_ui, borrows_ui, add_borrow_dialog, student_dialog, borrow_dialog):
        super(MainWindow, self).__init__()
        uic.loadUi(ui, self)

        self.setWindowTitle('OLDI')
        
        self.con = con
        self.cur = cur
        self.books_ui = books_ui
        self.students_ui = students_ui
        self.borrows_ui = borrows_ui
        self.add_borrow_dialog = add_borrow_dialog
        self.student_dialog = student_dialog
        self.borrow_dialog = borrow_dialog

        self.pagelayout = self.centralwidget.layout()
        self.tabs_layout = QtWidgets.QStackedLayout()
        self.pagelayout.addLayout(self.tabs_layout)

        self.books_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(0))
        self.students_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(1))
        self.borrows_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(2))

        self.tabs_layout.addWidget(Books(self.cur, self.books_ui))
        self.tabs_layout.addWidget(Students(self.con, self.cur, self.students_ui, self.student_dialog, self.add_borrow_dialog))
        self.tabs_layout.addWidget(Borrows(self.con, self.cur, self.borrows_ui, self.borrow_dialog))



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
    def __init__(self, cur, ui):
        super(Books, self).__init__()
        uic.loadUi(ui, self)

        self.table = QTableView()
        self.verticalLayout.addWidget(self.table)

        self.cur = cur
        
        self.cur.execute("SELECT * FROM books")
        data = cur.fetchall()
        self.insert_data(data)


        header = QHeaderView(Qt.Horizontal)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setHorizontalHeader(header)

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
        self.insert_data(data)

    def get_genres(self):
        self.cur.execute('SELECT * from genres')
        return self.cur.fetchall()

    def insert_data(self, data):
        # self.table.clearContents()
        # self.table.setColumnCount(len(data[0]))
        # self.table.setRowCount(len(data))
        # for n, row in enumerate(data):
        #     for i, cell in enumerate(row):
        #         self.table.setItem(n, i, QtWidgets.QTableWidgetItem(str(cell)))

        self.model = TableModel(data)
        self.table.setModel(self.model)



class Students(QWidget):

    def __init__(self, con, cur, students_ui, student_dialog, add_borrow_dialog):
        super(Students, self).__init__()

        
        self.con = con
        self.cur = cur
        self.student_dialog = student_dialog
        self.add_borrow_dialog = add_borrow_dialog
        uic.loadUi(students_ui, self)

        self.table = QTableView()
        self.verticalLayout.addWidget(self.table)
    
        self.cur.execute("SELECT * FROM students")
        data = cur.fetchall()

        self.insert_data(data)

        header = QHeaderView(Qt.Horizontal)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setHorizontalHeader(header)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

        self.table.doubleClicked.connect(self.open_dialog)
    
    def query(self):
        self.cur.execute("SELECT * FROM students WHERE first_name LIKE ? AND last_name LIKE ? AND phone LIKE ?", ('%' + self.firstname_box.text() + '%', '%' + self.lastname_box.text() + '%', '%' + self.phone_box.text() + '%'))
        data = self.cur.fetchall()
        self.insert_data(data)
    
    def open_dialog(self, index):
        student_id = self.model.index(index.row(), 0).data()
        print(student_id)
        dlg = StudentDialog(self.con, self.cur, student_id, self.student_dialog, self.add_borrow_dialog)
        dlg.exec_()

    def insert_data(self, data):
        # self.table.setColumnCount(len(data[0]))
        # self.table.setRowCount(len(data))
        # for n, row in enumerate(data):
        #     for i, cell in enumerate(row):
        #         self.table.setItem(n, i, QtWidgets.QTableWidgetItem(str(cell)))

        self.model = TableModel(data)
        self.table.setModel(self.model)

class Borrows(QWidget):

    def __init__(self, con, cur, borrows_ui, borrow_dialog):
        super(Borrows, self).__init__()

        
        self.cur = cur
        self.borrow_dialog = borrow_dialog
        uic.loadUi(borrows_ui, self)
        self.cur.execute("SELECT * FROM borrows")
        data = cur.fetchall()

        self.table = QTableView()
        self.verticalLayout.addWidget(self.table)

        self.insert_data(data)

        header = QHeaderView(Qt.Horizontal)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setHorizontalHeader(header)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        today_date = QDate.fromString(str(date.today()), 'yyyy-MM-dd')
        self.date_edit.setDate(today_date)

        self.table.doubleClicked.connect(self.open_dialog)
    
    def query(self):
        student_id = self.student_box.text()
        book_id = self.book_box.text()
        date = '%' + str(self.date_edit.date().toPyDate()) + '%'

        if self.check_box.isChecked():
            if student_id == '' and book_id == '':
                self.cur.execute("SELECT * FROM borrows WHERE date LIKE ?", (date,))
            elif student_id == '':
                self.cur.execute("SELECT * FROM borrows WHERE book_id = ? AND date LIKE ?", (book_id, date))
            elif book_id == '':
                self.cur.execute("SELECT * FROM borrows WHERE student_id = ? AND date LIKE ?", (student_id, date))
        
        else:
            if student_id == '' and book_id == '':
                self.cur.execute("SELECT * FROM borrows")
            elif student_id == '':
                self.cur.execute("SELECT * FROM borrows WHERE book_id = ?", book_id)
            elif book_id == '':
                self.cur.execute("SELECT * FROM borrows WHERE student_id = ?", student_id)

        data = self.cur.fetchall()
        self.insert_data(data)

    def insert_data(self, data):
        # self.table.setColumnCount(len(data[0]))
        # self.table.setRowCount(len(data))
        # for n, row in enumerate(data):
        #     for i, cell in enumerate(row):
        #         self.table.setItem(n, i, QtWidgets.QTableWidgetItem(str(cell)))
        self.model = TableModel(data)
        self.table.setModel(self.model)

    def open_dialog(self, index):
        pass
        borrow_id = self.model.index(index.row(), 0).data()
        print(borrow_id)
        dlg = BorrowDialog(self.borrow_dialog)
        dlg.exec_()


class StudentDialog(QDialog):
    def __init__(self, con, cur, student_id, ui, add_borrow_dialog):
        super(StudentDialog, self).__init__()
        self.con = con
        self.cur = cur
        self.student_id = student_id
        self.add_borrow_dialog = add_borrow_dialog
        uic.loadUi(ui, self)
        self.setWindowTitle("Elev")

        self.cur.execute("SELECT first_name, last_name, class_number, class_letter, phone, email FROM students WHERE student_id = ?", (int(student_id),))
        data = cur.fetchone()
        self.name_label.setText('<h1>' + ' '.join((data[0], data[1])) + '</h1>')
        self.class_label.setText('<h2>' + ' '.join((str(data[2]), data[3])) + '<h2>')
        self.phone_label.setText(data[4])
        self.email_label.setText(data[5])

        self.borrow_button.pressed.connect(self.add_borrow)

    def add_borrow(self):
        dlg = AddBorrow(self.con, self.cur, self.student_id, self.add_borrow_dialog)
        dlg.exec()

class AddBorrow(QDialog):
    def __init__(self, con, cur, student_id, ui):
        super(AddBorrow, self).__init__()
        self.con = con
        self.cur = cur
        self.student_id = student_id
        uic.loadUi(ui, self)
        self.setWindowTitle("Inchiriere")

        self.cur.execute("SELECT first_name, last_name FROM students WHERE student_id = ?", (self.student_id,))
        name = ' '.join(cur.fetchone())
        self.name_label.setText(name)
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        today_date = QDate.fromString(str(date.today()), 'yyyy-MM-dd')
        self.date_edit.setDate(today_date)

        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)


    def accept(self):
        date = self.date_edit.date()
        student_id = self.student_id
        book_id = self.book_box.text()
        self.cur.execute("INSERT INTO borrows (date, student_id, book_id, status) VALUES(?,?,?,?)", (date.toString('yyyy-MM-dd'), int(student_id), int(book_id), "inchiriata"))
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", (student_id, book_id))
        self.con.commit()
        self.close()

class BorrowDialog(QDialog):
    def __init__(self, ui):
        super(BorrowDialog, self).__init__()
        uic.loadUi(ui, self)

if __name__ == '__main__':  
    appctxt = OLDIContext()
    appctxt.run_app()