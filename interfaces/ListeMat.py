from PyQt5.uic import loadUi
import PyQt5.QtWidgets as qtw
from os import path

class ListeMat(qtw.QWidget):
    def __init__(self, parent=None, typeFlag=0, adminFlag=0):
        """ 
        typeFlag:  
            0 -> MGX\n
            1 -> Informatique
        adminFlag:
            0 -> Not admin
            1 -> admin
        """
        super(ListeMat, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listeMat.ui'), self)
        if typeFlag==1:
            self.setWindowTitle('Liste des materiels informatiques')
            