from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from GestionStrucutre.Service import Service
from sqlalchemy.orm import Session
from GestionStrucutre.Structure import Structure
from database import engine

class DialogAjouter(QDialog):
    update_liste = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_service.ui"), self)
        with Session(engine) as session:
            liste_str = session.query(Structure.code_str).all()
            for structure in liste_str:
                self.str_combo.addItem(structure[0])
        self.confirmer_button.clicked.connect(self.ajouterService)
    
    def ajouterService(self):
        codes = self.codes.text().strip().upper()
        noms = self.noms.toPlainText().strip().title()
        cstr = self.str_combo.currentText()
        if codes == '' or noms =='': # champs vides
            self.showErreur(1)
        else: # champs non vide
            with Session(engine) as session: 
                result = session.query(Service).filter_by(code_service = codes)
                if result.count() != 0: # code service exist deja
                    self.showErreur(2)
                else:
                    try:
                        serv1 = Service(code_service = codes, nom_service=noms, code_str=cstr)
                        session.add(serv1)
                        session.commit()
                        self.showErreur(0)
                        self.update_liste.emit()
                    except Exception as e:
                        self.showErreur(3, e)
            
    def showErreur(self, code, err=None):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setWindowTitle("Informations")
        if code == 0:
            msgbox.setText("Service Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 2:
            msgbox.setText("Service existe déja")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setDetailedText(err)
        
        
        msgbox.exec()
        

class ServiceUI(QWidget):
    def __init__(self, adminFlag, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "services.ui"), self)
        if adminFlag == 0:
            self.ajouter_button.hide()
            self.supprimer_button.hide()
        # table widget setup
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Code Service", "Nom de service", "Structure"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.initListeServices()
        # slots
        self.ajouter_button.clicked.connect(self.ouvrirDialogAjout)
        self.supprimer_button.clicked.connect(self.supprimer)
        
    def ouvrirDialogAjout(self):
        self.dialog = DialogAjouter()
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.show()
        self.dialog.update_liste.connect(self.initListeServices)
    
    def remplirListeService(self, listeServices):
        taille = len(listeServices)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listeServices:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_service))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.nom_service))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.code_str))
            x += 1
            
    def initListeServices(self):
        with Session(engine) as session:
            result = session.query(Service).all()
            self.remplirListeService(result)
    
    def supprimer(self):
        selected = self.tableWidget.selectedItems()
        codesupp = []
        for i in range(0, len(selected), 3):
            codesupp.append(selected[i].text())
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        listecodes = ",\n".join(codesupp)
        msgbox.setText("Voulez vous supprimer ces services?: \n"+listecodes)
        msgbox.setWindowTitle("Confirmation")
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnvalue = msgbox.exec()
        if returnvalue == QMessageBox.Ok:
            with Session(bind=engine) as session:
                for code in codesupp:
                    try:
                        session.query(Service).filter_by(code_service=code).delete()
                        session.commit()
                        self.initListeServices()
                    except Exception as e:
                        print(e)
                        msgbox2 = QMessageBox()
                        msgbox2.setIcon(QMessageBox.Warning)
                        msgbox2.setWindowTitle("Informations")
                        msgbox2.setText("Erreur dans la supression de "+ code)
                        msgbox2.setDetailedText(e)
                        msgbox2.exec()

