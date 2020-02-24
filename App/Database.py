import sys
from PyQt5.QtWidgets import QApplication, QWidget


app = QApplication(sys.argv)

window = QWidget()
window.show() # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()