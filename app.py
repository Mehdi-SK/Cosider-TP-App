
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from MainWindow import MainWindow
from Global import DATABASE_CONN
from sqlalchemy import create_engine

engine = create_engine(DATABASE_CONN)
app = QApplication(sys.argv)
stack = MainWindow(engine)

try:
    sys.exit(app.exec_())
except:
    print('Exiting')
