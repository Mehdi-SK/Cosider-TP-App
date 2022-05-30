import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from MainWindow import MainWindow


app = QApplication(sys.argv)
stack = MainWindow()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')
