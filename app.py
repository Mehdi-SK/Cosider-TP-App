
import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
from database import engine



app = QApplication(sys.argv)
window = MainWindow(engine)

try:
    sys.exit(app.exec_())
except:
    print('Exiting')
