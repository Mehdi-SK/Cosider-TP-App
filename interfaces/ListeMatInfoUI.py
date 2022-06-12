
from select import select
from time import strftime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtGui import QIntValidator
from os import path
from GestionMateriels.Fournisseur import Fournisseur
from GestionMateriels.Informatique import Informatique
from GestionMateriels.Affectation import Affectation
from sqlalchemy.orm import Session
from sqlalchemy import or_
from GestionStrucutre.Employe import Employe
from database import engine
from datetime import date

class DialogAjout(QDialog):
    update_liste_fr = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_mat_info.ui"), self)
        self.onlyInt = QIntValidator()
        self.prixHTLineEdit.setValidator(self.onlyInt)
        self.garantieLineEdit.setValidator(self.onlyInt)

        with Session(engine) as session:
            listeF = session.query(Fournisseur.nomf).all()
        for f in listeF:
            self.nomFournisseurComboBox.addItem(f[0])
            
        self.confirmer_button.clicked.connect(self.ajouter_mat)
    
    def getFields(self):
        cinv = self.codeinv.text().strip()
        nserie = self.numserie.text().strip()
        ccat = self.codecat.text().strip().upper()
        desig = self.desg.text().strip().title()
        mq = self.mrq.text().strip().upper()
        tp = self.typ.text().strip().upper()
        choix_etat = self.et.currentText().lower()
        # 0 en service, 1 en panne, 2 en stock, 3 archive
        etat = {"stock":2, "en panne":1, "archive":3, "en service":0}[choix_etat]
        print(etat)
        prc = self.process.text().strip().upper()
        
        achat = self.tachat.currentIndex()
        print(achat)
        dt = self.dtacq.date().toPyDate()
        print(dt)
        prxht = self.prixHTLineEdit.text().strip()
        grt = self.garantieLineEdit.text()
        nbc = self.numBCLineEdit.text().strip()
        nfct = self.numFactureLineEdit.text().strip()
        nfr = self.nomFournisseurComboBox.currentText()
        if cinv and nserie and ccat and desig and mq and tp and prxht and nbc and nfct:
            mat1 = Informatique(code_inv=cinv,
                                num_serie=nserie,
                                code_cat=ccat,
                                desig=desig,
                                code_marque=mq,
                                type=tp,
                                code_etat=etat,
                                processeur=prc,
                                prix_ht=prxht,
                                date_aq=dt,
                                type_achat=achat,
                                garantie=grt,
                                nbc=nbc,
                                nfact=nfct,
                                nomF=nfr)
            return mat1
        else:
            self.showErreur(1)
            
        
        
    def ajouter_mat(self):
        mat1 = self.getFields()
        if mat1:
            with Session(engine) as session:
                check = session.query(Informatique).filter(
                    or_(Informatique.code_inv==mat1.code_inv, Informatique.num_serie==mat1.num_serie)).count()
                if check != 0:
                    self.showErreur(2)
                else:
                    try:
                        session.add(mat1)
                        session.commit()
                        self.update_liste_fr.emit()
                        self.showErreur(0)
                    except Exception as e:
                        print(e)
                        self.showErreur(3)
    
    
    
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Equipement Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 2:
            msgbox.setText("Equipement existe déja")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        
        
        msgbox.exec()


class DialogModifier(QDialog):
    update_liste_fr = pyqtSignal()
    def __init__(self, selected, parent=None):
        super().__init__(parent)
    
        loadUi(path.join(path.dirname(__file__), "modifier_mat_info.ui"), self)
        self.onlyInt = QIntValidator()
        self.prixHTLineEdit.setValidator(self.onlyInt)
        self.garantieLineEdit.setValidator(self.onlyInt)
        self.selected = selected
        with Session(engine) as session:
            listeF = session.query(Fournisseur.nomf).all()
        for f in listeF:
            self.nomFournisseurComboBox.addItem(f[0])
            
        self.confirmer_button.clicked.connect(self.modifier)
        self.initModification()
        
    
    def initModification(self):
        self.codeinv.setText(self.selected.code_inv)
        self.numserie.setText(self.selected.num_serie)
        self.codecat.setText(self.selected.code_cat)
        self.desg.setText(self.selected.desig)
        self.mrq.setText(self.selected.code_marque)
        self.typ.setText(self.selected.type)
        if self.selected.processeur: self.process.setText(self.selected.processeur)
        self.prixHTLineEdit.setText(str(self.selected.prix_ht))
        self.garantieLineEdit.setText(str(self.selected.garantie))
        self.numBCLineEdit.setText(self.selected.nbc)
        self.numFactureLineEdit.setText(self.selected.nfact)
        self.et.setCurrentIndex(self.selected.code_etat)
        self.tachat.setCurrentIndex(self.selected.type_achat)
        
        datem = self.selected.date_aq
        self.dtacq.setDate(QDate(datem.day,datem.month, datem.year))
        
        index = self.nomFournisseurComboBox.findText(self.selected.nomF, Qt.MatchFixedString)
        self.nomFournisseurComboBox.setCurrentIndex(index)
    
    def modifier(self):
        cinv = self.codeinv.text().strip()
        with Session(engine) as session:
            mat1 = session.query(Informatique).filter_by(code_inv=cinv).one()
            print(type(mat1))
            ccat = self.codecat.text().strip().upper()
            desig = self.desg.text().strip().title()
            mq = self.mrq.text().strip().upper()
            tp = self.typ.text().strip().upper()
            choix_etat = self.et.currentText().lower()
            # 0 en service, 1 en panne, 2 en stock, 3 archive
            etat = {"stock":2, "en panne":1, "archive":3, "en service":0}[choix_etat]
            prc = self.process.text().strip().upper()
            achat = self.tachat.currentIndex()
            dt = self.dtacq.date().toPyDate()

            prxht = self.prixHTLineEdit.text().strip()
            grt = self.garantieLineEdit.text()
            nbc = self.numBCLineEdit.text().strip()
            nfct = self.numFactureLineEdit.text().strip()
            nfr = self.nomFournisseurComboBox.currentText()
            
            if ccat and desig and mq and tp and prxht and nbc and nfct:
                try:
                    mat1.code_cat=ccat
                    mat1.desig =desig
                    mat1.code_marque = mq
                    mat1.type = tp
                    mat1.code_etat=etat
                    mat1.processeur= prc
                    mat1.type_achat=achat
                    mat1.date_aq=dt
                    mat1.prix_ht=prxht
                    mat1.garantie=grt
                    mat1.nbc=nbc
                    mat1.nfact=nfct
                    mat1.nomF=nfr
                    
                    session.commit()
                    self.update_liste_fr.emit()
                    self.showErreur(0)
                    
                except:
                    self.showErreur(3)
            else:
                self.showErreur(1)
    
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        
        if code == 0:
            msgbox.setText("Equipement Modifié")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs:")
            msgbox.setIcon(QMessageBox.Information)
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        
        
        msgbox.exec()

class DialogAffecter(QDialog):
    update_liste_mat = pyqtSignal()
    def __init__(self, selectedCodes, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "affecter.ui"), self)
        self.selectedCodes = selectedCodes
        with Session(engine) as session:
            result = session.query(Employe.matricule).all()
        for res in result:
            self.combo_emp.addItem(res[0])
        self.combo_emp.currentTextChanged.connect(self.updateNomPrenom)
        self.confirmer_button.clicked.connect(self.affecter)
    def updateNomPrenom(self):
        mat = self.combo_emp.currentText()
        with Session(engine) as session:
            emp = session.query(Employe).filter_by(matricule=mat).one()
        self.champ.setText(f'{emp.nom} {emp.prenom}')

    def affecter(self):
        mat = self.combo_emp.currentText()
        with Session(engine) as session:
            emp = session.query(Employe).filter_by(matricule=mat).one()
            dt = date.today()
            aff = Affectation(date_affectation=dt)
            aff.employe=emp
            try:
                session.add(aff)
                session.commit()
                for code in self.selectedCodes:
                    print(code)
                    print(aff.numa)
                    eq = session.query(Informatique).filter_by(code_inv=code).one()
                    eq.affectation = aff
                    eq.code_etat = 0
                    session.commit()
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Affectation avec sucess!")
                msgbox.buttonClicked.connect(self.close)
                self.update_liste_mat.emit()
                msgbox.exec()
                
            except Exception as e:
                print(e)
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setText("Erreur dans l'affectation")
                msgbox.exec()
    
class ListMatInfoUI(QWidget):
    def __init__(self, parent=None, adminFlag=1):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listeMatInfo.ui'), self)

        # Table Widget
        liste_columns = ["CodeInv", "NumSerie", "Designation", "Cat", "Marque",
                         "Type", "Processeur", "Etat", "TAchat", "DateAcq", "PrixHt",
                         "Garantie", "NBC", "NFact", "Proprietaire"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.archive_checkbox.stateChanged.connect(self.initListeMat)
        self.modifier_button.clicked.connect(self.ouvrirMenuModification)
        self.affecter_button.clicked.connect(self.ouvrirAffectation)
        self.qr_button.clicked.connect(self.genererQR)
        self.initListeMat()
        
        
        # slots
        
        self.ajouter_button.clicked.connect(self.ouvrirMenuAjout)
    
    def ouvrirMenuAjout(self):
        self.menuaj = DialogAjout()
        self.menuaj.show()
        self.menuaj.update_liste_fr.connect(self.initListeMat)
   
    def ouvrirMenuModification(self):
        selected = self.tableWidget.selectedItems()

        if len(selected) == 0 or len(selected)>15:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner un seul materiel à modifier")
            msgbox.exec()
        else:
            with Session(engine) as session:
                result = session.query(Informatique).filter_by(code_inv=selected[0].text()).all()
            
            self.dialog_modifier = DialogModifier(result[0])
            self.dialog_modifier.show()
            self.dialog_modifier.update_liste_fr.connect(self.initListeMat)
    
    def ouvrirAffectation(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            codeInvAffect = []
            for i in range(0, len(selected), self.nb_col):
                codeInvAffect.append(selected[i].text())
            self.dialogAffect = DialogAffecter(codeInvAffect)
            self.dialogAffect.show()
            self.dialogAffect.update_liste_mat.connect(self.initListeMat)    
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner au moins un materiel pour affecter")
            msgbox.exec()
    def remplirListeMat(self, listemat):
        taille = len(listemat)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listemat:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_inv))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.num_serie))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.desig))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(instance.code_cat))
            self.tableWidget.setItem(x, 4, QTableWidgetItem(instance.code_marque))
            self.tableWidget.setItem(x, 5, QTableWidgetItem(instance.type))
            if instance.processeur: self.tableWidget.setItem(x, 6, QTableWidgetItem(instance.processeur))
            # 0 en service, 1 en panne, 2 en stock, 3 archive
            et = {0:"En service", 1:"En panne", 2:"Stock", 3:"Archive", 0:"En service"}[instance.code_etat]
            self.tableWidget.setItem(x, 7, QTableWidgetItem(et))
            tachat = "Projet" if instance.type_achat==0 else "Siege"
            self.tableWidget.setItem(x, 8, QTableWidgetItem(tachat))
            dateq = instance.date_aq.strftime("%Y-%M-%D")
            self.tableWidget.setItem(x, 9, QTableWidgetItem(dateq))
            self.tableWidget.setItem(x, 10, QTableWidgetItem(str(instance.prix_ht)))
            self.tableWidget.setItem(x, 11, QTableWidgetItem(str(instance.garantie)))
            self.tableWidget.setItem(x, 12, QTableWidgetItem(instance.nbc))
            self.tableWidget.setItem(x, 13, QTableWidgetItem(instance.nfact))
            if instance.naffect:
                self.tableWidget.setItem(x, 14, QTableWidgetItem(instance.affectation.employe.nom))
            x += 1
    
    
    def genererQR(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            codeInvAffect = []
            for i in range(0, len(selected), self.nb_col):
                codeInvAffect.append(selected[i].text())
            with Session(engine) as session:
                for code in codeInvAffect:
                    eq = session.query(Informatique).filter_by(code_inv=code).one()
                    informationsQR = f'{eq.code_inv}/{eq.code_cat}/{eq.code_marque}/{eq.num_serie}/{eq.type}/{eq.desig}'
                    nomFichier = f'{eq.code_cat}-{eq.code_inv}'
                    self.creerQR(nomFichier, informationsQR)
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner au moins un materiel pour gener le code")
            msgbox.exec()
    
    def creerQR(self, nomfichier, informations):
        import qrcode
        import os
        img = qrcode.make(informations)
        img.save(f'{nomfichier}.png')
        oldpath = "E:\PFE\\app\\"+nomfichier+".png"
        newpath = "E:\PFE\\app\QR\\"+nomfichier+".png"
        os.rename(oldpath, newpath)
        
    
    def initListeMat(self):
        with Session(engine) as session:
            if self.archive_checkbox.isChecked():
                result = session.query(Informatique).filter(Informatique.code_etat==3).all()
            else:
                result = session.query(Informatique).filter(Informatique.code_etat!=3).all()
            self.remplirListeMat(result)