Hello, fellas, I'm building a GUI interface for a sqlite database, using PyQt5 and building it with fbs(in order to create a standalone app). I keep getting this really annoying problem: when launching the script, an empty window appears for around 0.5 sec, then quickly closes, then the main window appears. Normal behaviour would be: just the main window appearing. The main window should also start maximized, but instead the empty window is maximized, and the main window isn't.

I couldn't really find anyone reporting a similar behaviour. I followed this tutorial https://www.learnpyqt.com/courses/start/layouts/, about layout managament, ran their example, and got the same behaviour.


I'll post the relevant code

`class MainWindow(QMainWindow): 

    def __init__(self, ui, books_ui, cur):
        super(MainWindow, self).__init__()
        self.setWindowTitle('OLDI')
        self.showMaximized()
        ...
        pagelayout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        layout = QtWidgets.QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(layout)

        layout.addWidget(Books(self.books_ui, self.cur)) #Placing a break point here revealed that this is the moment the empty window appears
        layout.addWidget(Students())
        layout.addWidget(Borrows())


        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)`

And the Books class:

`class Books(QWidget):
    def __init__(self, ui, cur):
        super(Books, self).__init__()

        uic.loadUi(ui, self)
        
        self.model = TableModel(cur.fetchall())
        self.tableView.setModel(self.model)

        ...`

I'm using fbs's context application to launch the gui
`class OLDIContext(ApplicationContext):
        @cached_property
        def window(self):
            self.ui = self.get_resource(r'UIs\main.ui')
            self.books_ui = self.get_resource(r'UIs\books.ui')
            return MainWindow(self.ui, self.books_ui, self.cur)
            
        @cached_property
        def run_app(self):
            self.window.show()
            return self.app.exec_

if __name__ == '__main__':  
    appctxt = OLDIContext()
    appctxt.run_app()`



