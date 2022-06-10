


from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from os import path
from Interfaces.AuthentificationUI import Authentification
from Interfaces.ListeFournisseur import ListeFournisseurs
from Interfaces.EmployeUI import EmployeUI

from Interfaces.ListeMat import ListeMat
from Interfaces.ListeTransfers import ListeTransfers
from Interfaces.ProjetsUI import ProjetsUI
from Interfaces.ServicesUI import ServiceUI
from Interfaces.DepartementUI import DepartmentUI

class MenuPrincipale(QMainWindow):
    def __init__(self, engine, parent=None, adminFlag=0):
        """ Menu principale de l'application, contient la bar de navigation\n
            adminFlag = 1 : admin
        """
        super(MenuPrincipale, self).__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'menuprincipal.ui'), self)
        self.adminFlag = adminFlag
        self.engine = engine
        
        # connection des boutons avec les interface correspondates
        # --------------------------
        
        self.actionmateriel_informatique.triggered.connect(self.openListeMatInfo)
        self.actionmateriel_MGX.triggered.connect(self.openListeMatMgx)
        self.actionListe_des_transfers.triggered.connect(self.openListeTransfers)
        self.actioncarnet_d_adresses.triggered.connect(self.openListeFournisseur)
        self.actioncalculatrice.triggered.connect(self.openCalculatrice)
        
        self.actionemploye.triggered.connect(self.ouvrirMenuEmp)
        # Deconnexion
        self.actiondeconnection.triggered.connect(self.handleDeconnexion)
        self.actionprojet.triggered.connect(self.ouvrirMenuProjets)
        self.actionservice.triggered.connect(self.ouvrirMenuServices)  
        self.actiondepartement.triggered.connect(self.ouvrirMenuDepartements)
        
    def handleDeconnexion(self):
        self.auth = Authentification()
        self.auth.show()
        self.close()
        
    def openListeMatInfo(self):
        self.lminfo = ListeMat(typeFlag=1)
        self.lminfo.setWindowModality(Qt.ApplicationModal)
        self.lminfo.show()
    
    def openListeMatMgx(self):
        self.lmMgx = ListeMat()
        self.lmMgx.setWindowModality(Qt.ApplicationModal)
        self.lmMgx.show()
        
    def openListeTransfers(self):
        self.ltransfers = ListeTransfers()
        self.ltransfers.setWindowModality(Qt.ApplicationModal)
        self.ltransfers.show()
    
    def openListeFournisseur(self):
        self.lfournisseur = ListeFournisseurs()
        self.lfournisseur.setWindowModality(Qt.ApplicationModal)
        self.lfournisseur.show()
        
    def openCalculatrice(self):
        import subprocess
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')
    
    def ouvrirMenuEmp(self):
        self.menu_emp = EmployeUI()
        self.menu_emp.setWindowModality(Qt.ApplicationModal)
        self.menu_emp.show()
    
    def ouvrirMenuProjets(self):
        self.menu_projets = ProjetsUI(adminflag=self.adminFlag)
        self.menu_projets.setWindowModality(Qt.ApplicationModal)
        self.menu_projets.show()
    
    def ouvrirMenuServices(self):
        self.menu_service = ServiceUI(adminFlag=self.adminFlag)
        self.menu_service.setWindowModality(Qt.ApplicationModal)
        self.menu_service.show()
    
    def ouvrirMenuDepartements(self):
        self.menu_dep = DepartmentUI(adminFlag=self.adminFlag)
        self.menu_dep.setWindowModality(Qt.ApplicationModal)
        self.menu_dep.show()