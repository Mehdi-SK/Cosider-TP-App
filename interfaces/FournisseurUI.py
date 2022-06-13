
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from GestionMateriels.Fournisseur import Fournisseur

from sqlalchemy.orm import Session
from database import engine
# TODO add regular expressions

class DialogAjouter(QDialog):
    update_liste_fr = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_fournisseur.ui"), self)
        self.confirmer_button.clicked.connect(self.ajouterFournisseur)
    def ajouterFournisseur(self):
        nom = self.nom.text().upper().strip()
        email = self.mail.text().strip()
        numT = self.tel.text().strip()
        loc = self.loc.text().strip().title()
        
        if len(nom)==0:
            self.erreurLabel.setText("Nom de fournisseur est vide*")
        else:
            with Session(engine) as session:
                check = session.query(Fournisseur).filter_by(nomf=nom).count()
                if check != 0:
                    self.erreurLabel.setText("Nom de fournisseur existe deja!")
                else:
                    f1 = Fournisseur(nomf=nom,
                                     numT=numT,
                                     email=email,
                                     loc=loc)
                    try:
                        session.add(f1)
                        session.commit()
                        self.update_liste_fr.emit()
                        self.showErreur(0)
                    except:
                        self.showErreur(1)
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Fournisseur Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        
        elif code == 1:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        msgbox.exec()













class DialogModifier(QDialog):
    update_liste_fr = pyqtSignal()
    def __init__(self, result, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "modifier_fournisseur.ui"), self)
        self.result = result
        self.confirmer_button.clicked.connect(self.modifierFr)
        self.initModification()
    
    def initModification(self):
        self.nom.setText(self.result.nomf)
        self.tel.setText(self.result.numT)
        self.mail.setText(self.result.email)
        self.loc.setText(self.result.loc)
        
        
    def modifierFr(self):
        nomf = self.nom.text()
        email = self.mail.text().strip()
        numT = self.tel.text().strip()
        loc = self.loc.text().strip().title()
        with Session(engine) as session:
            try:
                session.query(Fournisseur).filter_by(nomf=nomf).update({"numT":numT,
                                                                        "email":email,
                                                                        "loc":loc})
                session.commit()
                msg = QMessageBox()
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText("Fournisseur modifié")
                msg.setIcon(QMessageBox.Information)
                msg.buttonClicked.connect(self.close)
                msg.exec()
                self.update_liste_fr.emit()
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText("Informations invaldies")
                msg.setIcon(QMessageBox.Information)
                msg.exec()
                
                
                
                
                
                
                
                
                
class FournisseurUI(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'fournisseurs.ui'), self)
        liste_columns = ["Fournisseur", "Tel", "E-Mail", "Localisation"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.init_liste_fr()
        self.ajouter_button.clicked.connect(self.ouvrirMenuAjout)
        self.modifier_button.clicked.connect(self.modifier)
    
    def ouvrirMenuAjout(self):
        self.menua = DialogAjouter()
        self.menua.show()
        self.menua.update_liste_fr.connect(self.init_liste_fr)
    
    def remplirListe(self, listefr):
        taille = len(listefr)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listefr:
            print(instance)
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.nomf))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.numT))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.email))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(instance.loc))
            x += 1
    def init_liste_fr(self):
        with Session(engine) as session:
            result = session.query(Fournisseur).all()
        self.remplirListe(result)
    
    def modifier(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 4:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner un seul fournisseur à modifier")
            msgbox.exec()
        else:
            with Session(engine) as session:
                result = session.query(Fournisseur).filter_by(nomf=selected[0].text()).all()
            
            self.dialog_modifier = DialogModifier(result[0])
            self.dialog_modifier.show()
            self.dialog_modifier.update_liste_fr.connect(self.init_liste_fr)