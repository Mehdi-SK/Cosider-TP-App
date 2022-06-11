from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from GestionStrucutre.Departement import Departement
from GestionStrucutre.Service import Service
from sqlalchemy.orm import Session
from database import engine

class DialogAjouter(QDialog):
    
    update_liste_dep = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_dep.ui"), self)
        self.confirmer_button.clicked.connect(self.ajouterDep)
        
        with Session(engine) as session:
            liste_services = session.query(Service.code_service).all()
            for service in liste_services:
                self.combo_service.addItem(service[0])
        
    def ajouterDep(self):
        coded = self.codedep.text().strip().upper()
        nomd = self.nomdep.toPlainText().strip().title()
        codes = self.combo_service.currentText()
        if len(coded)==0 or len(nomd)==0: #champs vide
            self.showErreur(1)
        else:
            with Session(engine) as session:
                check = session.query(Departement).filter_by(code_dep=coded)
                if check.count() != 0:
                    self.showErreur(2)
                else:
                    try:
                        dep = Departement(code_dep=coded, nom_dep=nomd, code_service=codes)
                        session.add(dep)
                        session.commit()
                        self.showErreur(0)
                        self.update_liste_dep.emit()
                    except:
                        self.showErreur(3)
                
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Département Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 2:
            msgbox.setText("Département existe déja")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        
        
        msgbox.exec()
        
class DepartmentUI(QWidget):
    def __init__(self, adminFlag, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "departements.ui"), self)
        if adminFlag == 0:
            self.ajouter_button.hide()
            self.supprimer_button.hide()
        
        self.nb_col = 3
        # table widget setup
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(["Code Dep", "Nom de dep", "Code Service"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.initListeDep()
        
        self.ajouter_button.clicked.connect(self.ouvrirDialogAjout)
        self.supprimer_button.clicked.connect(self.supprimer)
    
    def ouvrirDialogAjout(self):
        self.menu_ajouter = DialogAjouter()
        self.menu_ajouter.setWindowModality(Qt.ApplicationModal)
        self.menu_ajouter.show()
        self.menu_ajouter.update_liste_dep.connect(self.initListeDep)
    
    def remplirListeDep(self, listeDep):
        taille = len(listeDep)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listeDep:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_dep))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.nom_dep))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.code_service))
            x += 1
    
    def initListeDep(self):
        with Session(engine) as session:
            result = session.query(Departement).all()
            self.remplirListeDep(result)
    
    def supprimer(self):
        selected = self.tableWidget.selectedItems()
        codesupp = []
        for i in range(0, len(selected), self.nb_col):
            codesupp.append(selected[i].text())
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        listecodes = ",".join(codesupp)
        msgbox.setText("Voulez vous supprimer ces departements?\n"+listecodes)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnvalue = msgbox.exec()
        if returnvalue == QMessageBox.Ok:
            with Session(bind=engine) as session:
                for code in codesupp:
                    try:
                        session.query(Departement).filter_by(code_dep=code).delete()
                        session.commit()
                        self.initListeDep()
                    except Exception as e:
                        msgbox2 = QMessageBox()
                        msgbox2.setIcon(QMessageBox.Warning)
                        print(e)
                        msgbox2.setText("Erreur dans la supression de "+ code)
                        msgbox2.exec()