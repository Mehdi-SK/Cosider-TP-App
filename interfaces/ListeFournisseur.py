import PyQt5.QtWidgets as qtw
from os import path
from PyQt5.uic import loadUi

class ListeFournisseurs(qtw.QWidget):
    def __init__(self, parent=None) -> None:
        super(ListeFournisseurs, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'fournisseurs.ui'), self)
        
        