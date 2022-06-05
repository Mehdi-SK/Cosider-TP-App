
from Interfaces.AuthentificationUI import Authentification
from Interfaces.MenuPrincipaleUI import MenuPrincipale

class MainWindow():
    def __init__(self, engine):
        self.engine = engine
        self.auth = Authentification(engine)
        self.auth.show()
        self.auth.showMenuPrincipalSignal.connect(self.showmenu)
    
    def showmenu(self):
        self.mp = MenuPrincipale(self.engine)
        self.mp.show()
        self.auth.close()
        