from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal
from os import path
from GestionStrucutre.Projet import Projet

from database import engine
from sqlalchemy.orm import Session


class AjouterProjet(QDialog):
    update_liste = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_projet.ui"), self)
        self.setWindowTitle("Ajouter un projet")
        self.confirmer_button.clicked.connect(self.ajouter)
        
    def getInformations(self):
        """Retourne les informations dans les champs"""
        return (self.codep.text().upper(), self.nomp.toPlainText().strip().title(), self.addp.text().strip().title())
    
    def ajouter(self): 
        """Controller d'ajout"""
        infos = self.getInformations()
        if infos[0]=='' or infos[1]=='':
            self.show_info(1)
        else:
            projet1 = Projet(code_projet=infos[0], nom_projet=infos[1], adresse=infos[2])
            with Session(bind=engine) as session:
                exist = session.query(Projet).filter_by(code_projet=projet1.code_projet).first()
                if not exist:
                    try:
                        session.add(projet1)
                        session.commit()
                        self.show_info()
                        self.update_liste.emit()
                    except:
                        self.show_info(1)
                else:
                    self.show_info(2)

    def show_info(self, type_erreur=0):
        """Fonction qui affiche les erreurs qui peuvent apparaitre pendant l'ajout"""
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        if type_erreur == 0:
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Projet ajouté.")
            msgbox.buttonClicked.connect(self.close)
        elif type_erreur == 1:
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("Informations invalide!")
            msgbox.buttonClicked.connect(msgbox.close)
        else:
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setText("Projet avec ce code exist deja")
            msgbox.buttonClicked.connect(msgbox.close)
        msgbox.exec()
    
            
class ProjetsUI(QWidget):
    def __init__(self, parent=None, adminflag=0):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "projets.ui"), self)
        if adminflag == 0:
            self.supprimer_button.hide()
            self.ajouter_button.hide()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Code Projet", "Nom de projet", "Adresse"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.initListeProjets()
        self.ajouter_button.clicked.connect(self.ouvrirAjout)
        self.supprimer_button.clicked.connect(self.handleSupression)
        self.rechercher_button.clicked.connect(self.filtrer)

    def ouvrirAjout(self):
        self.pageAjout = AjouterProjet()
        self.pageAjout.show()
        self.pageAjout.update_liste.connect(self.initListeProjets)
    
    def remplirListe(self, listeProjets):
        nb = len(listeProjets)
        self.tableWidget.setRowCount(nb)
        x = 0
        for instance in listeProjets:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_projet))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.nom_projet))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.adresse))
            x += 1
    def initListeProjets(self):
        with Session(bind=engine) as session:
            listeProjets = session.query(Projet).all()
            self.remplirListe(listeProjets=listeProjets)       
    
    def handleSupression(self):
        selected = self.tableWidget.selectedItems()
        codepSupp = [] # liste des codes projets concerne par supression
        for i in range(0, len(selected), 3):
            codepSupp.append(selected[i].text())
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        listep = ",".join(codepSupp)
        if len(listep) == 0:
            msgbox.setText("Choisir le(s) projet(s) à supprimer")
            msgbox.setStandardButtons(QMessageBox.Ok)
        else:
            msgbox.setText("Voulez vous supprimer ces projets\n"+listep)
            msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnvalue = msgbox.exec()
        
        if len(listep)!=0 and returnvalue == QMessageBox.Ok:
            with Session(bind=engine) as session:
                for code in codepSupp:
                    try:
                        session.query(Projet).filter_by(code_projet=code).delete()
                        session.commit()
                        self.initListeProjets()
                    except:
                        msgbox2 = QMessageBox()
                        msgbox2.setIcon(QMessageBox.Warning)
                        msgbox2.setText("Erreur dans la supression")
                        msgbox2.exec()

    def filtrer(self):
        codeRecherche = self.input.text().strip()
        if codeRecherche != '':
            with Session(bind=engine) as session:
                resultat = session.query(Projet).filter_by(code_projet = codeRecherche).all()
                if len(resultat) > 0:
                    self.remplirListe(resultat)
                else:
                    msgbox = QMessageBox()
                    msgbox.setText("Aucun resultat trouvé")
                    msgbox.exec()
        else:
            self.initListeProjets()