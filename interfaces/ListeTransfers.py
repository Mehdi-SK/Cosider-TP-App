from PyQt5.uic import loadUi
import PyQt5.QtWidgets as qtw
from os import path

class ListeTransfers(qtw.QWidget):
    def __init__(self, parent=None) -> None:
        super(ListeTransfers, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listetransfer.ui'), self)
        