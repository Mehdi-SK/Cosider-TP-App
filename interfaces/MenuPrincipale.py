from functools import partial
from multiprocessing import AuthenticationError

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QMainWindow
from os import path
from interfaces.AuthentificationUI import Authentification
from interfaces.ListeFournisseur import ListeFournisseurs


from interfaces.ListeMat import ListeMat
from interfaces.ListeTransfers import ListeTransfers


class MenuPrincipale(QMainWindow):
    def __init__(self, parent=None, adminFlag=0) -> None:
        """ Menu principale de l'application, contient la bar de navigation\n
            adminFlag = 1 : admin
        """
        super(MenuPrincipale, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'menuprincipal.ui'), self)
        
        
        # connection des boutons avec les interface correspondates
        # --------------------------
        
        self.actionmateriel_informatique.triggered.connect(self.openListeMatInfo)
        self.actionmateriel_MGX.triggered.connect(self.openListeMatMgx)
        self.actionListe_des_transfers.triggered.connect(self.openListeTransfers)
        self.actioncarnet_d_adresses.triggered.connect(self.openListeFournisseur)
        self.actioncalculatrice.triggered.connect(self.openCalculatrice)
        
        # Deconnexion
        self.actiondeconnection.triggered.connect(self.handleDeconnexion)
        
    def handleDeconnexion(self):
        self.auth = Authentification()
        self.auth.show()
        self.close()
        
    def openListeMatInfo(self):
        self.lminfo = ListeMat(typeFlag=1)
        self.lminfo.show()
    
    def openListeMatMgx(self):
        self.lmMgx = ListeMat()
        self.lmMgx.show()
        
    def openListeTransfers(self):
        self.ltransfers = ListeTransfers()
        self.ltransfers.show()
    
    def openListeFournisseur(self):
        self.lfournisseur = ListeFournisseurs()
        self.lfournisseur.show()
        
    def openCalculatrice(self):
        import subprocess
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')