from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from GestionStrucutre.Departement import Departement
from GestionStrucutre.Employe import Employe

from sqlalchemy.orm import Session
from database import engine


class ListMatInfoUI(QWidget):
    def __init__(self, parent=None, adminFlag=1):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listeMatInfo.ui'), self)

        # Table Widget
        liste_columns = ["CodeInv", "NumSerie", "Designation", "Cat", "Marque",
                         "Type", "Processeur", "Etat", "TAchat", "DateAcq", "PrixHt",
                         "Garantie", "NBC", "NFact", "Proprietaire"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        
