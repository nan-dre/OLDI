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

make join between books and borrows table
make gui look better
- color code borrows
- table stretch over space
- bigger fonts
- stylesheets maybe

create student add menu
implement import excel tab
implement database selection
database backup
create new db from template
edit book
edit student
'''


class OLDIContext(ApplicationContext):

    @cached_property
    def window(self):
        ui = self.get_resource(r'UIs\main.ui')
        books_ui = self.get_resource(r'UIs\books.ui')
        students_ui = self.get_resource(r'UIs\students.ui')
        borrows_ui = self.get_resource(r'UIs\borrows.ui')
        add_borrow_ui = self.get_resource(r'UIs\add_borrow.ui')
        student_dialog = self.get_resource(r'UIs\student_dialog.ui')
        borrow_dialog_ui = self.get_resource(r'UIs\borrow_dialog.ui')
        borrow_edit_dialog_ui = self.get_resource(r'UIs\borrow_edit_dialog.ui')
        cur = self.db_connect
        books_ui_list = books_ui
        students_ui_list = (students_ui, student_dialog, add_borrow_ui)
        borrows_ui_list = (borrows_ui, borrow_dialog_ui, borrow_edit_dialog_ui)

        #return MainWindow(con, cur, ui, books_ui, students_ui, borrows_ui, add_borrow_ui, student_dialog, borrow_dialog_ui)
        return MainWindow(self.con, cur, ui, books_ui_list, students_ui_list, borrows_ui_list)

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

    def __init__(self, con, cur, ui, books_ui_list, students_ui_list, borrows_ui_list):
        super(MainWindow, self).__init__()
        uic.loadUi(ui, self)
        
        self.con = con
        self.cur = cur
        self.books_ui = books_ui_list
        self.students_ui = students_ui_list[0]
        self.student_dialog = students_ui_list[1]
        self.add_borrow_dialog = students_ui_list[2]
        self.borrows_ui = borrows_ui_list[0]
        self.borrow_dialog_ui = borrows_ui_list[1]

        self.pagelayout = self.centralwidget.layout()
        self.tabs_layout = QtWidgets.QStackedLayout()
        self.pagelayout.addLayout(self.tabs_layout)

        self.books_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(0))
        self.students_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(1))
        self.borrows_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(2))

        self.tabs_layout.addWidget(Books(self.cur, self.books_ui))
        self.tabs_layout.addWidget(Students(self.con, self.cur, self.students_ui, self.student_dialog, self.add_borrow_dialog))
        self.tabs_layout.addWidget(Borrows(self.con, self.cur, self.borrows_ui, self.borrow_dialog_ui))



class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, columns):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = columns
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columns[section]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self._data == []:
            return 0
        return len(self._data[0])

class TableView(QTableView):
    def __init__(self, columns):
        super(TableView, self).__init__()
        self.columns = columns
        header = QHeaderView(Qt.Horizontal)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setHorizontalHeader(header)
    
    

 
class Books(QWidget):
    def __init__(self, cur, ui):
        super(Books, self).__init__()
        uic.loadUi(ui, self)

        self.cur = cur
        
        self.cur.execute("SELECT * FROM books")
        data = cur.fetchall()
        self.columns = list(map(lambda x: x[0], self.cur.description))
        
        self.table = TableView(self.columns)
        self.verticalLayout.addWidget(self.table)
        
        self.insert_data(data)


        for genre in self.get_genres():
            self.genre_combobox.addItem(str(genre[0]) + ' ' + genre[1])
        self.genre_combobox.setCurrentIndex(8)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

    # def open_dialog(self, index):
    #     book_id = self.model.index(index.row(), 0).data()
    #     dlg = BookDialog(self.cur, book_id, self.book_dialog_ui)
    #     dlg.exec_()


    def query(self):
        index = self.genre_combobox.currentIndex()
        self.cur.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND genre_id = ?",('%' + self.title_box.text() + '%' , '%' + self.name_box.text() + '%', index))
        data = self.cur.fetchall()
        self.insert_data(data)

    def get_genres(self):
        self.cur.execute('SELECT * from genres')
        return self.cur.fetchall()

    def insert_data(self, data):

        self.model = TableModel(data, self.columns)
        self.table.setModel(self.model)



class Students(QWidget):

    def __init__(self, con, cur, students_ui, student_dialog, add_borrow_dialog):
        super(Students, self).__init__()

        
        self.con = con
        self.cur = cur
        self.student_dialog = student_dialog
        self.add_borrow_dialog = add_borrow_dialog
        uic.loadUi(students_ui, self)

        
    
        self.cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        self.columns = list(map(lambda x: x[0], self.cur.description))

        self.table = TableView(self.columns)
        self.verticalLayout.addWidget(self.table)
        self.insert_data(data)

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
        dlg = StudentDialog(self.con, self.cur, student_id, self.student_dialog, self.add_borrow_dialog)
        dlg.exec_()

    def insert_data(self, data):

        self.model = TableModel(data, self.columns)
        self.table.setModel(self.model)

class Borrows(QWidget):

    def __init__(self, con, cur, borrows_ui, borrow_dialog_ui):
        super(Borrows, self).__init__()

        self.con = con
        self.cur = cur
        self.borrow_dialog_ui = borrow_dialog_ui
        uic.loadUi(borrows_ui, self)
        self.cur.execute("SELECT * FROM borrows")
        data = cur.fetchall()

        self.columns = list(map(lambda x: x[0], self.cur.description))

        self.table = TableView(self.columns)
        self.verticalLayout.addWidget(self.table)

        self.insert_data(data)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        today_date = QDate.fromString(str(date.today()), 'yyyy-MM-dd')
        self.date_edit.setDate(today_date)

        self.table.doubleClicked.connect(self.on_cell_double_click)
    
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
        
        self.model = TableModel(data, self.columns)
        self.table.setModel(self.model)

    def borrow_return(self, borrow_id):
        self.cur.execute("UPDATE borrows SET status = ? WHERE borrow_id = ?", (1, borrow_id))
        self.cur.execute("SELECT book_id FROM borrows WHERE borrow_id =  ?", (borrow_id,))
        book_id = self.cur.fetchone()[0]
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", ("libera", book_id))
        self.con.commit()

    def on_cell_double_click(self, index):
        borrow_id = self.model.index(index.row(), 0).data()
        if(index.column() == 4): # status column
            self.borrow_return(borrow_id)
        else: 
            dlg = BorrowDialog(self.con, self.cur, borrow_id, self.borrow_dialog_ui)
            dlg.exec_()

# class BookDialog(QDialog):
#     def __init__(self, cur, book_id, ui):
#         super(BookDialog, self).__init__()
#         self.cur = cur
#         self.book_id = book_id
#         uic.loadUi(ui, self)



class StudentDialog(QDialog):
    def __init__(self, con, cur, student_id, ui, add_borrow_dialog):
        super(StudentDialog, self).__init__()
        self.con = con
        self.cur = cur
        self.student_id = student_id
        self.add_borrow_dialog = add_borrow_dialog
        uic.loadUi(ui, self)

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
        self.cur.execute("INSERT INTO borrows (date, student_id, book_id, status) VALUES(?,?,?,?)", (date.toString('yyyy-MM-dd'), int(student_id), int(book_id), 0))
        borrow_id = self.cur.lastrowid
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", (borrow_id, book_id))
        self.con.commit()
        self.close()

class BorrowDialog(QDialog):
    def __init__(self, con, cur, borrow_id, ui):
        super(BorrowDialog, self).__init__()
        self.con = con
        self.cur = cur
        self.borrow_id = borrow_id
        uic.loadUi(ui, self)

        
        
        self.cur.execute("SELECT date, student_id, book_id, status FROM borrows WHERE borrow_id = ?", str(self.borrow_id))
        borrow_data = self.cur.fetchone()

        self.date = QDate.fromString(borrow_data[0], 'yyyy-MM-dd')
        self.student_id = borrow_data[1]
        self.book_id = borrow_data[2]
        self.status = borrow_data[3]

        self.id_label.setText(str(borrow_id))
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setDate(self.date)
        self.student_box.setValue(self.student_id)
        self.book_box.setValue(self.book_id)
        if self.status == 0:
            self.status_box.setCurrentIndex(0)
        elif self.status == 1:
            self.status_box.setCurrentIndex(1)
        elif self.status == -1:
            self.status_box.setCurrentIndex(2)

        self.ok_button.pressed.connect(self.accept)
        self.cancel_button.pressed.connect(self.reject)

    def accept(self):
        index = self.status_box.currentIndex()
        if index == 0:
            status = 0
        if index == 1:
            status = 1
        if index == 2:
            status = -1
        
        borrow_id = str(self.id_label.text())
        book_id = self.book_box.value()
        old_book_id = self.book_id
        student_id = self.student_box.value()
        date = self.date_edit.date().toString('yyyy-MM-dd')
        data = (date, student_id, book_id, status, borrow_id)
        self.cur.execute("UPDATE borrows SET date = ?, student_id = ?, book_id = ?, status = ? WHERE borrow_id = ?", data) # update borrow
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", ("libera", old_book_id)) # update old book
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", (borrow_id, book_id)) # update new book
        
        self.con.commit()
        self.close()

if __name__ == '__main__':  
    appctxt = OLDIContext()
    appctxt.run_app()