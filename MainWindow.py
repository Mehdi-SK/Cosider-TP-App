
from Interfaces.AuthentificationUI import Authentification
from Interfaces.MenuPrincipaleUI import MenuPrincipale
class MainWindow():
    def __init__(self):
        self.auth = Authentification()
        self.auth.show()
        self.auth.showMenuPrincipalSignal.connect(self.showmenu)
    def showmenu(self, adminF):
        self.mp = MenuPrincipale(adminFlag=adminF)
        self.mp.show()
        self.auth.close()
        