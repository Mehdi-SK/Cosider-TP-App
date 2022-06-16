from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
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
        self.fermer.hide()
        self.fermer.clicked.connect(self.fermer_right)
        self.resetButton.clicked.connect(self.reset)
        self.searchtype.currentIndexChanged.connect(self.reset)
        self.listemat.clicked.connect(self.showlistmat)
        self.searchButton.clicked.connect(self.rechercher)
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
        selected = self.tableWidget.selectedItems()
        if len(selected) !=0:
            num = int(selected[0].text())
            with Session(engine) as session:
                if self.searchtype.currentIndex() == 0: # Transfert
                    t1 = session.query(Transfert).filter_by(numt=num).one()
                    print(t1.equip_info, "\n---------\n",t1.equip_bureau)
                    if len(t1.equip_info)!=0:
                        listmat = t1.equip_info
                        self.remplirListeMatInfo(listemat=listmat)
                    elif len(t1.equip_bureau) !=0:
                        listmat = t1.equip_bureau
                        
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
            msgbox.setWindowTitle("Erreur")
            msgbox.setText("Selectionner un element")
            msgbox.exec()
    def remplirListeMatInfo(self, listemat):
        liste_columns = ["Code Inventaire", "NSerie", "Catégorie", "Marque", "Type",
                         "Processeur", "Etat", "Type Achat", "Date Acquisition", "Prix HT",
                         "Garantie", "NBon de commande", "NFacture", "Fournisseur","Affecté à"]
        self.nb_col = len(liste_columns)
        self.rightwidget.setColumnCount(self.nb_col)
        self.rightwidget.setHorizontalHeaderLabels(liste_columns)
        taille = len(listemat)
        self.rightwidget.setRowCount(taille)
        x = 0
        for instance in listemat:
            self.rightwidget.setItem(x, 0, QTableWidgetItem(instance.code_inv))
            self.rightwidget.setItem(x, 1, QTableWidgetItem(instance.num_serie))
            self.rightwidget.setItem(x, 2, QTableWidgetItem(instance.code_cat))
            self.rightwidget.setItem(x, 3, QTableWidgetItem(instance.code_marque))
            self.rightwidget.setItem(x, 4, QTableWidgetItem(instance.type))
            if instance.processeur:
                self.rightwidget.setItem(x, 5, QTableWidgetItem(instance.processeur))
                
            # 0 en service, 1 en panne, 2 en stock, 3 archive, 4 transfert
            et = {0:"En service", 1:"En panne", 2:"Stock", 3:"Archive",
                  4:"Transferé"}[instance.code_etat]
            self.rightwidget.setItem(x, 6, QTableWidgetItem(et))
            
            tachat = "Projet" if instance.type_achat==0 else "Siège"
            self.rightwidget.setItem(x, 7, QTableWidgetItem(tachat))
            dateq = instance.date_aq.strftime("%Y-%m-%d")
            self.rightwidget.setItem(x, 8, QTableWidgetItem(dateq))
            self.rightwidget.setItem(x, 9, QTableWidgetItem(str(instance.prix_ht)))
            
            if instance.garantie:
                self.rightwidget.setItem(x, 10, QTableWidgetItem(str(instance.garantie)))
            self.rightwidget.setItem(x, 11, QTableWidgetItem(instance.nbc))
            self.rightwidget.setItem(x, 12, QTableWidgetItem(instance.nfact))
            self.rightwidget.setItem(x, 13, QTableWidgetItem(instance.nomF))
            if instance.mat_emp:
                nomcomplet= instance.employe.nom+ " " + instance.employe.prenom
            else:
                nomcomplet = ""
            self.rightwidget.setItem(x, 14, QTableWidgetItem(nomcomplet))
            
            x += 1
    def rechercher(self):
        d1 = self.date1.date().toPyDate()
        d2 = self.date2.date().toPyDate()
        with Session(engine) as session:
            if self.searchtype.currentIndex() == 0: # transfert
                listeT = session.query(Transfert).filter(Transfert.datet.between(d1, d2)).all()
                self.loadTransferts(listeT)
            elif self.searchtype.currentIndex()==1:
                listeA = session.query(Affectation).filter(Affectation.date_affectation.between(d1, d2)).all()
                self.loadAffectation(listeA)
    def fermer_right(self):
        self.rightwidget.hide()
        self.fermer.hide()
    