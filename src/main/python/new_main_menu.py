from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QCompleter, QDialog, QHeaderView, QStackedLayout, QMainWindow, QWidget, QTabWidget, QPushButton, QLabel, QTableView, QShortcut, QAction
from PyQt5.QtCore import Qt, QDate, QPoint, QModelIndex, QSettings
from PyQt5.QtGui import QKeySequence, QColor
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.platform import name
import sys
import os
import sqlite3
from datetime import date


from import_module import excel_import



class OLDIContext(ApplicationContext):
    @cached_property
    def window(self):
        window = MainWindow()
        window.tabs_layout.addWidget(self.books)
        window.tabs_layout.addWidget(self.students)
        window.tabs_layout.addWidget(self.borrows)
        window.tabs_layout.currentChanged.connect(self.tab_changed)
        window.action_import_books.triggered.connect(self.books_import_dialog)
        return self.window

    def tab_changed(self, index):
        if index == 0:
            self.books.query()
        elif index == 1:
            self.students.query()
        elif index == 2:
            self.borrows.query()
    
    def books_import_dialog(self, s):
        dlg = BooksImport(self.database)
        dlg.exec_()
    
    @cached_property
    def database(self):
        database = Database()
        settings = QSettings("OLDI", "Nandre")
        #settings.setValue("windows_db_path", r'D:\Proiecte\Python\OLDI\src\main\resources\base\DBs\Biblioteca.db')
        if name() == 'Windows':
            db_path = settings.value("windows_db_path")
            if db_path == None:
                self.window.database_select_dialog("s")
            else:
                    database.update(db_path)
        else:
            db_path = settings.value("linux_db_path")
            if db_path == None:
                self.window.database_select_dialog("s")
            else:
                database.update(db_path)
        del settings
        return database
    
    @cached_property
    def books(self):
        books = Books(self.database)
        for genre in self.get_genres():
            self.books.genre_combobox.addItem(str(genre[0]) + ' ' + genre[1])
        self.books.genre_combobox.setCurrentIndex(8)
        return books

    @cached_property
    def students(self):
        students = Students(database)
        return students

    @cached_property
    def borrows(self):
        borrows = Borrows(database)
        return borrows

    @cached_property
    def run_app(self):
        self.window.show()
        return self.app.exec_

    def insert_data(self, widget, columns, data):
        table = TableView(columns)
        self.widget.verticalLayout.addWidget(table) 
        model = TableModel(data, self.columns, widget)
        self.widget.table.setModel(model)

    def get_genres(self):
        self.database.cursor.execute('SELECT * from genres')
        return self.database.cursor.fetchall()
        

class Database():
    def __init__(self):
        # self.windows_default_db_path = windows_default_db_path
        # self. linux_default_db_path = linux_default_db_path
        self.con = None

    def update(self, db_path):
        self.settings = QSettings("OLDI", "Nandre")
        if name() == 'Windows':
            if self.con:
                self.con.close()
                self.con = None
            self.con = sqlite3.connect(db_path)
            self.settings.setValue("windows_db_path", db_path)
        else:
            if self.con:
                self.con.close()
                self.con = None
            self.con = sqlite3.connect(db_path)
            self.settings.setValue("linux_db_path", db_path)
    @property
    def cursor(self):
        if not self.con:
            raise Exception("no db open")
        return self.con.cursor()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(main_ui, self)

        self.pagelayout = self.centralwidget.layout()
        self.tabs_layout = QtWidgets.QStackedLayout()
        self.pagelayout.addLayout(self.tabs_layout)

        self.books_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(0))
        self.students_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(1))
        self.borrows_btn.pressed.connect(lambda: self.tabs_layout.setCurrentIndex(2))
        
        self.action_select_database.triggered.connect(self.database_select_dialog)    
    
    def database_select_dialog(self, s):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self,"Select Database", "","Database Files (*.db)", options=options)
        settings = QSettings("OLDI", "Nandre")
        try:
            if name() == "Windows":
                settings.setValue("windows_db_path", filename)
                self.database.update(filename)

            elif name() == "Linux":
                settings.setValue("linux_db_path", filename)
                self.database.update(filename)
        except NameError as e:
            print(e)

        del settings

   

#------------------MODELS AND VIEWS--------------------

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, columns, widget):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = columns
        self.widget = widget
        
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columns[section]
            if orientation == Qt.Vertical:
                return section + 1
                

    def data(self, index, role):
        if self.widget == 'borrows':
            if role == Qt.BackgroundRole:
                due_date = QDate.fromString(self._data[index.row()][2] , 'yyyy-MM-dd')
                current_date = QDate.fromString(str(date.today()), 'yyyy-MM-dd')
                status = self._data[index.row()][5]
                difference = current_date.daysTo(due_date)
                if status == 1:
                    return QColor("#2ecc71") # green
                else:
                    if difference < 0:
                        return QColor("#e74c3c") # red
                    elif difference >= 0:
                        return QColor("#f1c40f") # yellow
        if self.widget == "books":
            if role == Qt.BackgroundRole:
                status = self._data[index.row()][7]
                if status == 'libera':
                    return QColor("#2ecc71") # green
                else: # borrowed
                    return QColor("#e74c3c") # red

                    
            
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
        horizontal_header = QHeaderView(Qt.Horizontal)
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
        self.setHorizontalHeader(horizontal_header)

        vertical_header = QHeaderView(Qt.Vertical)
        self.setVerticalHeader(vertical_header)

#------------------WIDGETS------------------------------

class Books(QWidget):
    def __init__(self, database):
        super(Books, self).__init__()
        uic.loadUi(books_ui, self)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

    # def open_dialog(self, index):
    #     book_id = self.model.index(index.row(), 0).data()
    #     dlg = BookDialog(self.cur, book_id, self.book_dialog_ui)
    #     dlg.exec_()


    def query(self):
        index = self.genre_combobox.currentIndex()
        cur = self.database.cursor
        cur.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ? AND genre_id = ?",('%' + self.title_box.text() + '%' , '%' + self.name_box.text() + '%', index))
        data = cur.fetchall()
        self.insert_data(data)

    

    

class Students(QWidget):

    def __init__(self, database, students_ui, student_dialog, add_borrow_dialog):
        super(Students, self).__init__()

        self.database = database
        self.con = database.con
        self.cur = database.cursor
        self.student_dialog = student_dialog
        self.add_borrow_dialog = add_borrow_dialog
        uic.loadUi(students_ui, self)

        
    
        self.cur.execute("SELECT * FROM students")
        data = self.cur.fetchall()
        self.columns = list(map(lambda x: x[0], self.cur.description))

        self.table = TableView(self.columns)
        self.verticalLayout.addWidget(self.table)
        self.insert_data(data)

        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(lambda: self.query())
        self.search_button.pressed.connect(lambda: self.query())

        self.table.doubleClicked.connect(self.open_dialog)
    
    def query(self):
        cur = self.database.cursor
        cur.execute("SELECT * FROM students WHERE first_name LIKE ? AND last_name LIKE ? AND phone LIKE ?", ('%' + self.firstname_box.text() + '%', '%' + self.lastname_box.text() + '%', '%' + self.phone_box.text() + '%'))
        data = cur.fetchall()
        self.insert_data(data)
    
    def open_dialog(self, index):
        student_id = self.model.index(index.row(), 0).data()
        dlg = StudentDialog(self.database, student_id, self.student_dialog, self.add_borrow_dialog)
        dlg.exec_()

    def insert_data(self, data):

        self.model = TableModel(data, self.columns, "students")
        self.table.setModel(self.model)

class Borrows(QWidget):

    def __init__(self, database, borrows_ui, borrow_dialog_ui):
        super(Borrows, self).__init__()

        self.database = database
        self.con = database.con
        self.cur = database.cursor
        self.borrow_dialog_ui = borrow_dialog_ui
        uic.loadUi(borrows_ui, self)
        self.cur.execute("SELECT * FROM borrows")
        data = self.cur.fetchall()

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
        self.cur = self.database.cursor
        student_id = self.student_box.text()
        book_id = self.book_box.text()
        date = '%' + str(self.date_edit.date().toPyDate()) + '%'
        filt = self.filter_box.currentIndex()
        
        if filt == 0:
            if self.date_check_box.isChecked():
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
        
        elif filt == 1:
            if self.date_check_box.isChecked():
                if student_id == '' and book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE date LIKE ? AND status = ?", (date, 0))
                elif student_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE book_id = ? AND date LIKE ? AND status = ?", (book_id, date, 0))
                elif book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE student_id = ? AND date LIKE ? AND status = ?", (student_id, date, 0))
            
            else:
                if student_id == '' and book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE status = ?", (0,))
                elif student_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE book_id = ? AND status = ?", (book_id, 0))
                elif book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE student_id = ? AND status = ?", (student_id, 0))
        elif filt == 2:
            if self.date_check_box.isChecked():
                if student_id == '' and book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE date LIKE ? AND status = ?", (date, 1))
                elif student_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE book_id = ? AND date LIKE ? AND status = ?", (book_id, date, 1))
                elif book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE student_id = ? AND date LIKE ? AND status = ?", (student_id, date, 1))
            
            else:
                if student_id == '' and book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE status = ?", (1,))
                elif student_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE book_id = ? AND status = ?", (book_id, 1))
                elif book_id == '':
                    self.cur.execute("SELECT * FROM borrows WHERE student_id = ? AND status = ?", (student_id, 1))

        data = self.cur.fetchall()
        self.insert_data(data)

    def insert_data(self, data):
        self.model = TableModel(data, self.columns, "borrows") 
        self.table.setModel(self.model)


    def borrow_return(self, borrow_id):
        self.cur = self.database.cursor
        self.con = self.database.con
        self.cur.execute("UPDATE borrows SET status = ? WHERE borrow_id = ?", (1, borrow_id))
        self.cur.execute("SELECT book_id FROM borrows WHERE borrow_id =  ?", (borrow_id,))
        book_id = self.cur.fetchone()[0]
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", ("libera", book_id))
        self.con.commit()
        self.query()

    def on_cell_double_click(self, index):
        borrow_id = self.model.index(index.row(), 0).data()
        #if(index.column() == 4): # status column
        self.borrow_return(borrow_id)
        # else: 
        #     dlg = BorrowDialog(self.database, borrow_id, self.borrow_dialog_ui)
        #     dlg.exec_()

#------------------DIALOGS--------------------------------

class StudentDialog(QDialog):
    def __init__(self, database, student_id, ui, add_borrow_dialog):
        super(StudentDialog, self).__init__()
        self.con = database.con
        self.cur = database.cursor
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
        dlg = AddBorrow(self.database, self.student_id, self.add_borrow_dialog)
        dlg.exec()

class AddBorrow(QDialog):
    def __init__(self, database, student_id, ui):
        super(AddBorrow, self).__init__()
        self.con = database.con
        self.cur = database.cursor
        self.database = database
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
        self.cur = self.database.cursor
        date = self.date_edit.date()
        due_date = date.addMonths(1)
        student_id = self.student_id
        book_id = self.book_box.text()
        self.cur.execute("INSERT INTO borrows (date, due_date, student_id, book_id, status) VALUES(?,?,?,?,?)", (date.toString('yyyy-MM-dd'), due_date.toString('yyyy-MM-dd'), int(student_id), int(book_id), 0))
        borrow_id = self.cur.lastrowid
        self.cur.execute("UPDATE books SET status = ? WHERE book_id = ?", (borrow_id, book_id))
        self.con.commit()
        self.close()

class BorrowDialog(QDialog):
    def __init__(self, database, borrow_id, ui):
        super(BorrowDialog, self).__init__()
        self.database = database
        self.con = database.con
        self.cur = database.cursor
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
        self.cur = self.database.cursor
        
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

class BooksImport(QDialog):
    def __init__(self, database):
        super(BooksImport, self).__init__()
        uic.loadUi(books_import_dialog_ui, self)
        self.con = database.con
        self.cur = database.cursor
        self.setWindowTitle("Import elevi")

        for genre in self.get_genres():
            self.genre_combobox.addItem(str(genre[0]) + ' ' + genre[1])
        self.genre_combobox.setCurrentIndex(8)
        
        self.select_db_button.pressed.connect(lambda: self.open_file_dialog('.db'))
        self.select_excel_button.pressed.connect(lambda: self.open_file_dialog('.xlsx'))
        self.cancel_button.pressed.connect(self.reject)
        self.ok_button.pressed.connect(self.execute)

        self.db_line_edit.textChanged.connect(self.activate_ok)
        self.excel_line_edit.textChanged.connect(self.activate_ok)

    def open_file_dialog(self, filetype):
        options = QFileDialog.Options()
        if filetype == '.xlsx':
            filename, _ = QFileDialog.getOpenFileName(self,"Import Excel", "","Excel Files (*.xlsx)", options=options)
            self.excel_line_edit.setText(filename)
        elif filetype == '.db':
            filename, _ = QFileDialog.getOpenFileName(self,"Import Database", "","Database Files (*.db)", options=options)
            self.db_line_edit.setText(filename)

    def activate_ok(self):
        self.db_path = self.db_line_edit.text()
        self.excel_path = self.excel_line_edit.text()

        if self.db_path and self.excel_path:
            self.ok_button.setEnabled(1)

    def get_genres(self):
        self.cur.execute('SELECT * from genres')
        return self.cur.fetchall()

    def execute(self):
        excel_import(self.db_path, self.excel_path, self.genre_combobox.currentIndex())
        self.accept()

class RestartDialog(QDialog):

    def __init__(self, ui):
        super(RestartDialog, self).__init__()
        uic.loadUi(ui, self)
        print(ui)
     

#------------------MAIN--------------------------------------

if __name__ == '__main__':  
    appctxt = OLDIContext()
    if name() == 'Windows': # Windows file dir \
            main_ui = appctxt.get_resource(r'UIs\main.ui')
            books_ui = appctxt.get_resource(r'UIs\books.ui')
            students_ui = appctxt.get_resource(r'UIs\students.ui')
            borrows_ui = appctxt.get_resource(r'UIs\borrows.ui')
            add_borrow_dialog = appctxt.get_resource(r'UIs\add_borrow.ui')
            student_dialog = appctxt.get_resource(r'UIs\student_dialog.ui')
            borrow_dialog_ui = appctxt.get_resource(r'UIs\borrow_dialog.ui')
            borrow_edit_dialog_ui = appctxt.get_resource(r'UIs\borrow_edit_dialog.ui')
            books_import_dialog_ui = appctxt.get_resource(r'UIs\books_import_dialog.ui')
            restart_dialog_ui = appctxt.get_resource(r'UIs\restart_dialog.ui')
    else: #Linux file dir /
            main_ui = appctxt.get_resource(r'UIs/main.ui')
            books_ui = appctxt.get_resource(r'UIs/books.ui')
            students_ui = appctxt.get_resource(r'UIs/students.ui')
            borrows_ui = appctxt.get_resource(r'UIs/borrows.ui')
            add_borrow_dialog = appctxt.get_resource(r'UIs/add_borrow.ui')
            student_dialog = appctxt.get_resource(r'UIs/student_dialog.ui')
            borrow_dialog_ui = appctxt.get_resource(r'UIs/borrow_dialog.ui')
            borrow_edit_dialog_ui = appctxt.get_resource(r'UIs/borrow_edit_dialog.ui')
            books_import_dialog_ui = appctxt.get_resource(r'UIs/books_import_dialog.ui')
            restart_dialog_ui = appctxt.get_resource(r'UIs/restart_dialog.ui')
    appctxt.run_app()