
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt
from os import path
from GestionStrucutre.Departement import Departement
from GestionStrucutre.Employe import Employe

from sqlalchemy.orm import Session
from database import engine


class DialogAjout(QDialog):
    update_liste_emp = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_emp.ui"), self)
        self.confirmer_button.clicked.connect(self.ajouterEmp)
        
        with Session(engine) as session:
            liste_dep = session.query(Departement.code_dep).all()
        for dep in liste_dep:
            self.combo_dep.addItem(dep[0])
    def ajouterEmp(self):
        mat = self.mat.text().strip().upper()
        nomEmp = self.nom.text().strip().upper()
        prenomEmp = self.prenom.text().strip().title()
        posteEmp = self.poste.text().strip().title()
        choix_genre = self.combo_genre.currentText()
        genreEmp = choix_genre == "Femme"
        dep = self.combo_dep.currentText()

        if len(mat)==0 or len(nomEmp)==0 or len(prenomEmp)==0 or len(posteEmp)==0:
            self.showErreur(1)
        else:
            with Session(engine) as session:
                check = session.query(Employe).filter_by(matricule=mat).count()
                if check != 0:
                    self.showErreur(2)
                else:
                    emp = Employe(matricule=mat, nom=nomEmp, prenom=prenomEmp,
                                      poste=posteEmp, genre=genreEmp, code_dep=dep)
                    try:
                        with Session(engine) as session:
                            session.add(emp)
                            session.commit()
                            self.showErreur(0)
                            self.update_liste_emp.emit()
                    except Exception as e:
                        self.showErreur(3)
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Employé Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 2:
            msgbox.setText("Employé existe déja")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        
        
        msgbox.exec()

class DialogModifier(QDialog):
    update_liste_emp = pyqtSignal()
    def __init__(self, result, adminf, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "modifier_emp.ui"), self)
        self.result = result
        self.confirmer_button.clicked.connect(self.modifierEmp)
        if adminf == 0:
            self.archive_checkbox.hide()
        with Session(engine) as session:
            liste_dep = session.query(Departement.code_dep).all()
            for dep in liste_dep:
                self.combo_dep.addItem(dep[0])
        self.initModification()

    def initModification(self):
        self.mat.setText(self.result.matricule)
        self.nom.setText(self.result.nom)
        self.prenom.setText(self.result.prenom)
        self.poste.setText(self.result.poste)
        
        index = self.combo_dep.findText(self.result.code_dep, Qt.MatchFixedString)
        self.combo_dep.setCurrentIndex(index)
        
        index_genre = 1 if self.result.genre else 0
        self.combo_genre.setCurrentIndex(index_genre)
        
        self.archive_checkbox.setChecked(self.result.archive)
        
    def modifierEmp(self):
        mat = self.mat.text()
        nomEmp = self.nom.text().strip().upper()
        prenomEmp = self.prenom.text().strip().title()
        posteEmp = self.poste.text().strip().title()
        choix_genre = self.combo_genre.currentText()
        genreEmp = choix_genre == "Femme"
        dep = self.combo_dep.currentText()
        etat_archive = self.archive_checkbox.isChecked()
        if len(nomEmp)==0 or len(prenomEmp)==0 or len(posteEmp)==0:
            self.showErreur(1)
        else:
            try:
                with Session(engine) as session:
                    session.query(Employe).filter_by(matricule=mat).update({"nom":nomEmp,
                                                "prenom":prenomEmp,
                                                "poste":posteEmp,
                                                "genre":genreEmp,
                                                "code_dep":dep,
                                                "archive":etat_archive})
                    session.commit()
                    self.showErreur(0)
                    self.update_liste_emp.emit()
            except Exception as e:
                print(e)
                self.showErreur(3)
        
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Employé modifié")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        
        
        msgbox.exec()
    
class EmployeUI(QWidget):
    def __init__(self, adminFlag, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "employe.ui"), self)
        self.adminf = adminFlag
        if adminFlag==0:
            self.archiver_button.hide()
            self.archive_checkbox.hide()
            
        # table widget setup
        liste_columns = ["Matricule", "Nom", "Prénom", "Genre", "Poste", "Departement"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.initListeEmp()
        # slots
        self.ajouter_button.clicked.connect(self.ouvrirDialogAjout)
        self.archive_checkbox.stateChanged.connect(self.initListeEmp)
        self.archiver_button.clicked.connect(self.archiver)
        self.modifier_button.clicked.connect(self.modifier)
        self.rechercher_button.clicked.connect(self.rechercher)
    def ouvrirDialogAjout(self):
        self.menu_ajouter = DialogAjout()
        self.menu_ajouter.show()
        self.menu_ajouter.update_liste_emp.connect(self.initListeEmp)

    def remplirListeDep(self, listeEmp):
        taille = len(listeEmp)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listeEmp:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.matricule))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.nom))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.prenom))
            genre = "Femme" if instance.genre else "Homme"
            self.tableWidget.setItem(x, 3, QTableWidgetItem(genre))
            self.tableWidget.setItem(x, 4, QTableWidgetItem(instance.poste))
            self.tableWidget.setItem(x, 5, QTableWidgetItem(instance.code_dep))
            x += 1
    def initListeEmp(self):
        with Session(engine) as session:
            if self.archive_checkbox.isChecked():
                result = session.query(Employe).filter_by(archive=True).all()
            else:
                result = session.query(Employe).filter_by(archive=False).all()
            self.remplirListeDep(result)
        
    def archiver(self):
        if not self.archive_checkbox.isChecked():
            selected = self.tableWidget.selectedItems()
            codesupp = []
            for i in range(0, len(selected), self.nb_col):
                codesupp.append(selected[i].text())
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            listecodes = ",\n".join(codesupp)
            msgbox.setText("Voulez vous archiver ces employés?\n"+listecodes)
            msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnvalue = msgbox.exec()
            if returnvalue == QMessageBox.Ok:
                with Session(bind=engine) as session:
                    for code in codesupp:
                        try:
                            session.query(Employe).filter_by(matricule=code).update({"archive": True})
                            session.commit()
                            self.initListeEmp()
                        except Exception as e:
                            msgbox2 = QMessageBox()
                            msgbox2.setIcon(QMessageBox.Warning)
                            print(e)
                            msgbox2.setText("Erreur dans l'archivage de "+ code)
                            msgbox2.exec()
        else:
            msgbox2 = QMessageBox()
            msgbox2.setIcon(QMessageBox.Warning)
            msgbox2.setText("Ces employés est déjà dans l'archive")
            msgbox2.exec()
            
    def modifier(self):
        
        selected = self.tableWidget.selectedItems()
        if len(selected) != 6:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner un seul employé à modifier")
            msgbox.exec()
        else:
            with Session(engine) as session:
                result = session.query(Employe).filter_by(matricule=selected[0].text()).all()
            
            self.dialog_modifier = DialogModifier(result[0], self.adminf)
            self.dialog_modifier.show()
            self.dialog_modifier.update_liste_emp.connect(self.initListeEmp)
    
    def rechercher(self):
        mode_recherche = self.search_combo.currentText()
        recherche = self.recherche.text().strip().upper()
        if len(recherche)==0:
            self.initListeEmp()
        else:
            liste_resultat = []
            etat_archive = self.archive_checkbox.isChecked()
            with Session(engine) as session:
                if mode_recherche == "Nom":
                    liste_resultat = session.query(Employe).filter_by(nom=recherche, archive=etat_archive).all()
                elif mode_recherche=="Matricule":
                    liste_resultat = session.query(Employe).filter_by(matricule=recherche, archive=etat_archive).all()
                else:
                    liste_resultat = session.query(Employe).filter_by(code_dep=recherche, archive=etat_archive).all()
            self.remplirListeDep(liste_resultat)
            