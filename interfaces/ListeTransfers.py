from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from os import path
from database import engine
from sqlalchemy.orm import Session
from GestionMateriels.Affectation import Affectation
from GestionMateriels.Transfert import Transfert

class ListeTransfers(QWidget):
    def __init__(self, parent=None) -> None:
        super(ListeTransfers, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listetransfer.ui'), self)
        self.loadAllTransfert()
        self.rightwidget.hide()
        self.resetButton.clicked.connect(self.reset)
        self.searchtype.currentIndexChanged.connect(self.reset)
        self.listemat.clicked.connect(self.showlistmat)
    def loadTransferts(self, listeTransferts):
        columnListe = ["Numero", "Date", "Moyen transport", "Chauffeur", "Utilisateur", "Vers"]
        columnCount = len(columnListe)
        self.tableWidget.setColumnCount(columnCount)
        self.tableWidget.setHorizontalHeaderLabels(columnListe)
        
        rowCount = len(listeTransferts)
        self.tableWidget.setRowCount(rowCount)
        x = 0 
        for instance in listeTransferts:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(str(instance.numt)))
            datet = instance.datet.strftime("%Y-%m-%d")
            self.tableWidget.setItem(x, 1, QTableWidgetItem(datet))
            if instance.moyent: self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.moyent))
            if instance.nomC: self.tableWidget.setItem(x, 3, QTableWidgetItem(instance.nomC))
            self.tableWidget.setItem(x, 4, QTableWidgetItem(instance.nom_util))
            self.tableWidget.setItem(x, 5, QTableWidgetItem(instance.projetD))
            x += 1
    def loadAffectation(self, listeAffectations):
        columnListe = ["Numero", "Date", "Employé", "Utilisateur"]
        columnCount = len(columnListe)
        
        self.tableWidget.setColumnCount(columnCount)
        self.tableWidget.setHorizontalHeaderLabels(columnListe)
        
        rowCount = len(listeAffectations)
        self.tableWidget.setRowCount(rowCount)
        x = 0 
        for instance in listeAffectations:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(str(instance.numa)))
            dateaff = instance.date_affectation.strftime("%Y-%m-%d")
            self.tableWidget.setItem(x, 1, QTableWidgetItem(dateaff))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.mat_emp))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(instance.nom_util))
            x +=1
            
    def loadAllTransfert(self):
        with Session(engine) as session:
            listeTransfert = session.query(Transfert).all()
        self.loadTransferts(listeTransfert)
    
    def loadAllAffectations(self):
        with Session(engine) as session:
            listeTransfert = session.query(Affectation).all()
        self.loadAffectation(listeTransfert)
     
    def reset(self):
        if self.searchtype.currentIndex() == 0:
            self.loadAllTransfert()
        elif self.searchtype.currentIndex()==1:
            self.loadAllAffectations()
    def showlistmat(self):
        self.rightwidget.hide() if self.rightwidget.isVisible() else self.rightwidget.show()