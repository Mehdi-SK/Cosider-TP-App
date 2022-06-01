from unittest import result
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from os import path
from GestionAuthentification.Utilisateur import Utilisateur
from sqlalchemy.orm import sessionmaker

class Authentification(QWidget):
    showMenuPrincipalSignal = pyqtSignal()

    def __init__(self, engine, parent=None):
        self.engine = engine
        super(Authentification, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), "authentification.ui"), self)
        self.connect_button.clicked.connect(self.connecter)
                
    def connecter(self):
        """ called when button is clicked, checks for username and password """
        Session = sessionmaker(bind=self.engine)
        user = self.username_field.text()
        pwd = self.password_field.text()
        if len(user) == 0 or len(pwd) == 0:
            self.error_label.setText('Veuillez remplir tout les champs')
        else:
            with Session() as session:
                result = session.query(Utilisateur).filter(Utilisateur.login==user,
                                                    Utilisateur.mot_de_passe==pwd)
                if result.count()>0:
                    print(*result) 
                    self.showMenuPrincipalSignal.emit()
                    print("Affichage menu principale")
                else:
                    self.error_label.setText('Mot de passe ou utilisateur incorrecte')
        
            
