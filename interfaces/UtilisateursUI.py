from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from GestionAuthentification.Utilisateur import Utilisateur
from GestionStrucutre.Employe import Employe
from sqlalchemy.orm import Session
from database import engine

class DialogAjout(QDialog):
    update_liste_utils = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_utilisateur.ui"), self)
        self.confirmer_button.clicked.connect(self.ajouterUtil)
    def ajouterUtil(self):
        username = self.login.text().strip()
        mdp = self.mdp.text().strip()
        admin = 1 if self.admin_check.isChecked() else 0
        if len(username) == 0 or len(mdp)==0:
            self.showErreur(1)
        else:
            with Session(engine) as session:
                check = session.query(Utilisateur).filter_by(login=username)
                if check.count() !=0:
                    self.showErreur(2)
                else:
                    u1 = Utilisateur(login=username, mot_de_passe=mdp, admin_flag=admin)
                    try:
                        session.add(u1)
                        session.commit()
                        self.update_liste_utils.emit()
                        self.showErreur(0)
                    except Exception as e:
                        print(e)
                        self.showErreur(3)
    
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Utilisateur Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 2:
            msgbox.setText("Nom utilisateur existe déja")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        msgbox.exec()   

            
class UtilisateursUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "departements.ui"), self)
        liste_columns = ["Nom Utilisateur", "Mot de passe"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        
        self.initListeUtils()
        
        self.ajouter_button.clicked.connect(self.ouvrirDialogAjout)
        self.supprimer_button.clicked.connect(self.supprimer)
    def remplirListeUtils(self, listeEmp):
        taille = len(listeEmp)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listeEmp:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.login))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.mot_de_passe))
            x += 1
    
    def initListeUtils(self):
        with Session(engine) as session:
           
            result = session.query(Utilisateur).all()
            self.remplirListeUtils(result)
    
    def ouvrirDialogAjout(self):
        self.menu_ajouter = DialogAjout()
        self.menu_ajouter.show()
        self.menu_ajouter.update_liste_utils.connect(self.initListeUtils)
    
    def supprimer(self):
        selected = self.tableWidget.selectedItems()
        codesupp = []
        for i in range(0, len(selected), self.nb_col):
            codesupp.append(selected[i].text())
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        listecodes = ",".join(codesupp)
        msgbox.setText("Voulez vous supprimer ces utilisateurs?\n"+listecodes)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnvalue = msgbox.exec()
        if returnvalue == QMessageBox.Ok:
            with Session(bind=engine) as session:
                for code in codesupp:
                    print(code)
                    print(type(code))
                    try:
                        if code == "admin" or code == "Admin":
                            msgbox3 = QMessageBox()
                            msgbox3.setIcon(QMessageBox.Warning)
                            msgbox3.setText("Vous pouvez pas supprimer cet utilisateur:"+ code)
                            msgbox3.exec()
                        else:
                            session.query(Utilisateur).filter_by(login=code).delete()
                            session.commit()
                            self.initListeUtils()
                    except Exception as e:
                        msgbox2 = QMessageBox()
                        msgbox2.setIcon(QMessageBox.Warning)
                        print(e)
                        msgbox2.setText("Erreur dans la supression de "+ code)
                        msgbox2.exec()