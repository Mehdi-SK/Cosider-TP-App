
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from os import path
from GestionAuthentification.Utilisateur import Utilisateur
from sqlalchemy.orm import Session
from database import engine
class Authentification(QWidget):
    showMenuPrincipalSignal = pyqtSignal(int)

    def __init__(self, mainwindow,parent=None):
        
        super(Authentification, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), "authentification.ui"), self)
        self.connect_button.clicked.connect(self.verifier)
        self.mainWindow = mainwindow
              
    def verifier(self):
        """ called when button is clicked, checks for username and password """
        user = self.username_field.text().strip()
        pwd = self.password_field.text().strip()
        if len(user) == 0 or len(pwd) == 0:
            self.error_label.setText('Veuillez remplir tout les champs')
            # REMOVE THIS ONE
            self.connecter(1)
            # REMOVE THIS ONE
        else:                 
            with Session(engine) as session:
                result = session.query(Utilisateur).filter(Utilisateur.login==user,
                                                    Utilisateur.mot_de_passe==pwd)
                if result.count()>0:
                    self.connecter(result[0].admin_flag)
                else:
                    self.error_label.setText('Mot de passe ou utilisateur incorrecte')

    def connecter(self, admin):
        self.mainWindow.afterConnexion(admin)
        self.close()