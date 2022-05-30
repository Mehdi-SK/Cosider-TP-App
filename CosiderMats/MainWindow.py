from interfaces.AuthentificationUI import Authentification
from interfaces.MenuPrincipale import MenuPrincipale

class MainWindow():
    def __init__(self):
        self.auth = Authentification()
        
        self.auth.show()
        self.auth.showMenuPrincipalSignal.connect(self.showmenu)
    
    def showmenu(self):
        self.mp = MenuPrincipale()
        self.mp.show()
        self.auth.close()
        