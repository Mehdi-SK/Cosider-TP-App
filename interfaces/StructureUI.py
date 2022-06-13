
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from os import path
from GestionStrucutre.Structure import Structure
from sqlalchemy.orm import Session
from database import engine


class DialogAjouter(QDialog):
    update_liste = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_str.ui"), self)
        self.confirmer_button.clicked.connect(self.ajouterStr)
    
    def ajouterStr(self):
        codestr = self.codestr.text().strip().upper()
        nomstr = self.nomstr.toPlainText().strip().title()
        
        if codestr == '' or nomstr =='': # champs vides
            self.showErreur(1)
        else: # champs non vide
            with Session(engine) as session: 
                result = session.query(Structure).filter_by(code_str = codestr)
                if result.count() != 0: # code structure exist deja
                    self.showErreur(2)
                else:
                    try:
                        str1 = Structure(code_str = codestr, nom_str=nomstr)
                        session.add(str1)
                        session.commit()
                        self.showErreur(0)
                        self.update_liste.emit()
                    except Exception as e:
                        self.showErreur(3, e)
            
    def showErreur(self, code, err = None):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setWindowTitle("Information")
        # TODO add icon
        if code == 0:
            msgbox.setText("Structure Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Warning)
        
        elif code == 2:
            msgbox.setText("Structure existe déja")
            msgbox.setIcon(QMessageBox.Warning)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setDetailedText(err)
        
        
        msgbox.exec()


class StructureUI(QWidget):
    def __init__(self, adminFlag, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "structure.ui"), self)
        if adminFlag == 0:
            self.ajouter_button.hide()
            self.supprimer_button.hide()
        # table widget setup
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Code Structure", "Nom de Strucutre"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.initListeStr()
        # slots
        self.ajouter_button.clicked.connect(self.ouvrirDialogAjout)
        self.supprimer_button.clicked.connect(self.supprimer)
    
    def ouvrirDialogAjout(self):
        self.dialog = DialogAjouter()
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.show()
        self.dialog.update_liste.connect(self.initListeStr)
    
    def remplirListeStr(self, listeStr):
        taille = len(listeStr)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listeStr:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_str))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.nom_str))
            x += 1
        
    def initListeStr(self):
        with Session(engine) as session:
            result = session.query(Structure).all()
            self.remplirListeStr(result)
    
    
    def supprimer(self):
        selected = self.tableWidget.selectedItems()
        codesupp = []
        for i in range(0, len(selected), 2):
            codesupp.append(selected[i].text())
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        listecodes = ",\n".join(codesupp)
        msgbox.setText("Voulez vous supprimer ces Structures?: \n"+listecodes
                       +"\n NB: Cela vas supprimer tout les services associés, continuez?")
        msgbox.setWindowTitle("Confirmation")
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnvalue = msgbox.exec()
        if returnvalue == QMessageBox.Ok:
            with Session(bind=engine) as session:
                for code in codesupp:
                    try:
                        session.query(Structure).filter_by(code_str=code).delete()
                        session.commit()
                        self.initListeStr()
                    except Exception as e:
                        msgbox2 = QMessageBox()
                        msgbox2.setWindowTitle("Erreur")
                        msgbox2.setIcon(QMessageBox.Warning)
                        msgbox2.setText("Erreur dans la supression de "+ code)
                        msgbox2.setDetailedText(e)
                        msgbox2.exec()
