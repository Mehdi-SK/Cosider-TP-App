from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from os import path
from GestionAuthentification.Utilisateur import Utilisateur
from sqlalchemy.orm import sessionmaker

class Authentification(QWidget):
    showMenuPrincipalSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(Authentification, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), "authentification.ui"), self)
        self.connect_button.clicked.connect(self.connecter)
                
    def connecter(self):
        """ called when button is clicked, checks for username and password """
        
        # user = self.username_field.text()
        # pwd = self.password_field.text()
        # if len(user) == 0 or len(pwd) == 0:
        #     self.error_label.setText('Veuillez remplir tout les champs')
        # elif user != '1234' or pwd != '1234':
        #     self.error_label.setText('Mot de passe ou utilisateur incorrecte')
        # else:
        self.showMenuPrincipalSignal.emit()
        
            
