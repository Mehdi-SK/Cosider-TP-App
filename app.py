
import sys
from PyQt5.QtWidgets import QApplication
from Interfaces.MenuPrincipaleUI import MenuPrincipale
from database import engine



app = QApplication(sys.argv)
window = MenuPrincipale()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')
