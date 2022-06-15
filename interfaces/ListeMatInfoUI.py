
from datetime import date
from select import select
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtGui import QIntValidator
from os import path
from GestionMateriels.Fournisseur import Fournisseur
from GestionMateriels.Informatique import Informatique
from GestionMateriels.Affectation import Affectation
from sqlalchemy.orm import Session
from sqlalchemy import or_
from GestionMateriels.Transfert import Transfert
from GestionStrucutre.Employe import Employe
from GestionStrucutre.Projet import Projet
from database import Global, engine


#TODO add ajouter fournisseur to ajouter mat
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
        mq = self.mrq.text().strip().upper()
        tp = self.typ.text().strip().upper()
        choix_etat = self.et.currentText().lower()
        # 0 en service, 1 en panne, 2 en stock, 3 archive
        etat = {"stock":2, "en panne":1, "archive":3, "en service":0, "transferé": 4}[choix_etat]
        prc = self.process.text().strip().upper()
        # infos d'achat
        achat = self.tachat.currentIndex()
        dt = self.dtacq.date().toPyDate()
        prxht = self.prixHTLineEdit.text().strip()
        grt = self.garantieLineEdit.text()
        nbc = self.numBCLineEdit.text().strip()
        nfct = self.numFactureLineEdit.text().strip()
        nfr = self.nomFournisseurComboBox.currentText()
        if cinv and nserie and ccat and mq and tp and prxht and nbc and nfct:
            mat1 = Informatique(code_inv=cinv,
                                num_serie=nserie,
                                code_cat=ccat,
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
        msgbox.setWindowTitle("Information")
        
        if code == 0:
            msgbox.setText("Equipement Ajouté")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.buttonClicked.connect(self.close)
        elif code == 1:
            msgbox.setText("Veuillez remplir tout les champs nécessaires")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 2:
            msgbox.setText("Equipement existe déja")
            msgbox.setIcon(QMessageBox.Information)
        
        elif code == 3:
            msgbox.setText("Informations invalides")
            msgbox.setIcon(QMessageBox.Information)
        
        
        msgbox.exec()

class DialogModifier(QDialog):
    update_liste_mat = pyqtSignal()
    def __init__(self, selected:Informatique, parent=None):
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
        # 0 en service, 1 en panne, 2 en stock, 3 archive, 4 transfert
        if selected.code_etat == 0: self.et.addItem("En service")
        if selected.code_etat == 4: self.et.addItem("Transferé")
        self.confirmer_button.clicked.connect(self.modifier)
        self.initModification()
        
    
    def initModification(self):
        self.codeinv.setText(self.selected.code_inv)
        self.numserie.setText(self.selected.num_serie)
        self.codecat.setText(self.selected.code_cat)
        self.mrq.setText(self.selected.code_marque)
        self.typ.setText(self.selected.type)
        if self.selected.processeur: self.process.setText(self.selected.processeur)
        self.prixHTLineEdit.setText(str(self.selected.prix_ht))
        self.garantieLineEdit.setText(str(self.selected.garantie))
        self.numBCLineEdit.setText(self.selected.nbc)
        self.numFactureLineEdit.setText(self.selected.nfact)
        
        et = {0:"En service", 1:"En panne", 2:"Stock", 3:"Archive",
                  4:"Transferé"}[self.selected.code_etat]
        self.et.setCurrentText(et)
        self.tachat.setCurrentIndex(self.selected.type_achat)
        
        datem = self.selected.date_aq.strftime("%Y-%m-%d")
        dateq = QDate.fromString(datem, "yyyy-M-d")
        self.dtacq.setDate(dateq)
        
        index = self.nomFournisseurComboBox.findText(self.selected.nomF, Qt.MatchFixedString)
        self.nomFournisseurComboBox.setCurrentIndex(index)
    
    def modifier(self):
        cinv = self.codeinv.text().strip()
        with Session(engine) as session:
            mat1 = session.query(Informatique).filter_by(code_inv=cinv).one()

            ccat = self.codecat.text().strip().upper()
            mq = self.mrq.text().strip().upper()
            tp = self.typ.text().strip().upper()
            choix_etat = self.et.currentText().lower()
            # 0 en service, 1 en panne, 2 en stock, 3 archive
            etat = {"stock":2, "en panne":1, "archive":3, "en service":0, "transferé":4}[choix_etat]
            prc = self.process.text().strip().upper()
            achat = self.tachat.currentIndex()
            dt = self.dtacq.date().toPyDate()

            prxht = self.prixHTLineEdit.text().strip()
            grt = self.garantieLineEdit.text()
            nbc = self.numBCLineEdit.text().strip()
            nfct = self.numFactureLineEdit.text().strip()
            nfr = self.nomFournisseurComboBox.currentText()
            
            if ccat and mq and tp and prxht and nbc and nfct:
                try:
                    mat1.code_cat=ccat
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
                    if etat != 1:
                        mat1.mat_emp=None
                    session.commit()
                    self.showErreur(0)
                    
                except:
                    self.showErreur(3)
            else:
                self.showErreur(1)
        self.update_liste_mat.emit()
    
    def showErreur(self, code):
        msgbox = QMessageBox()
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setWindowTitle("information")
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

# _______________________Affectation_________________________
class DialogAffecter(QDialog):
    update_liste_mat = pyqtSignal()
    def __init__(self, selectedCodes, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "affecter.ui"), self)
        self.selectedCodes = selectedCodes
        liste_columns = ["Matricule", "Nom", "Prénom", "Genre", "Poste", "Service"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.initListeEmp()
        
        # links
        
        self.confirmer_button.clicked.connect(self.affecter)
        

    def remplirListeEmp(self, listeEmp):
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
            self.tableWidget.setItem(x, 5, QTableWidgetItem(instance.code_service))
            x += 1
    def initListeEmp(self):
        with Session(engine) as session:
            result = session.query(Employe).filter_by(archive=False).all()
        self.remplirListeEmp(result)
    
    def affecter(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            try:
                user = Global.utilisateur
                matemp = selected[0].text()
                dateaff = date.today()
                with Session(engine) as session:
                    mat_affect=[]
                    matDejaAffecte=[]
                   
                    for code in self.selectedCodes:
                        result = session.query(Informatique).filter_by(code_inv=code).one()
                        if result.mat_emp == matemp:
                            info = result.code_inv +"/"+result.code_cat+"/"+result.code_marque+"/"+result.type
                            matDejaAffecte.append(info)
                        else:    
                            mat_affect.append(result)
                    if len(matDejaAffecte) !=0:
                        msgs = "\n".join(matDejaAffecte)
                        msgb = QMessageBox()
                        msgb.setIcon(QMessageBox.Information)
                        msgb.setWindowTitle("Information")
                        msgb.setText("C'est materiels sont déjà affecté à(" + matemp+"):\n"+msgs)
                        msgb.exec()
                    if len(mat_affect):
                        affect = Affectation(date_affectation=dateaff, mat_emp=matemp, nom_util=user, matInfo=mat_affect)
                        session.add(affect)
                    
                        for materiel in mat_affect:
                            materiel.mat_emp = matemp
                            materiel.code_etat = 0
                            
                        session.commit()
                        self.update_liste_mat.emit()
                        msgbox = QMessageBox()
                        msgbox.setIcon(QMessageBox.Information)
                        msgbox.setWindowTitle("Information")
                        msgbox.setText("Succès")
                        msgbox.buttonClicked.connect(self.close)
                        msgbox.exec()
                        
            except Exception as e:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setWindowTitle("Erreur")
                msgbox.setText("Erreur")
                print(e)
                msgbox.exec()
    
    
class ListMatInfoUI(QWidget):
    def __init__(self, parent=None, adminFlag=1):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listeMatInfo.ui'), self)

        # Table Widget
        liste_columns = ["CodeInv", "NumSerie", "Catégorie", "Marque", "Type",
                         "Processeur", "Etat", "TAchat", "DateAcq", "PrixHt",
                         "Garantie", "NBC", "NFact", "Fournisseur","Proprietaire"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.rechercher_button.clicked.connect(self.rechercher)
        self.modifier_button.clicked.connect(self.ouvrirMenuModification)
        self.affecter_button.clicked.connect(self.ouvrirAffectation)
        self.qr_button.clicked.connect(self.genererQR)
        self.transfer_button.clicked.connect(self.ouvrirTransfert)
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
            self.dialog_modifier.update_liste_mat.connect(self.initListeMat)
    
    def ouvrirAffectation(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            
            codeInvAffect = []
            for i in range(0, len(selected)):
                if selected[i].column() == 0:
                    codeInvAffect.append(selected[i].text())
            self.dialogAffect = DialogAffecter(codeInvAffect)
            self.dialogAffect.show()
            self.dialogAffect.update_liste_mat.connect(self.initListeMat)
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner au moins un materiel pour affecter")
            msgbox.exec()
    def ouvrirTransfert(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            codeInvTransfert = []
            for i in range(0, len(selected)):
                if selected[i].column() == 0:
                    codeInvTransfert.append(selected[i].text())
            self.dialogTransfert = DialogTransfert(codeInvTransfert)
            self.dialogTransfert.show()
            self.dialogTransfert.update_liste_mat.connect(self.initListeMat)
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner au moins un materiel à transférer.")
            msgbox.exec()
    
    def remplirListeMat(self, listemat):
        taille = len(listemat)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listemat:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_inv))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.num_serie))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.code_cat))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(instance.code_marque))
            self.tableWidget.setItem(x, 4, QTableWidgetItem(instance.type))
            if instance.processeur:
                self.tableWidget.setItem(x, 5, QTableWidgetItem(instance.processeur))
                
            # 0 en service, 1 en panne, 2 en stock, 3 archive, 4 transfert
            et = {0:"En service", 1:"En panne", 2:"Stock", 3:"Archive",
                  4:"Transferé"}[instance.code_etat]
            self.tableWidget.setItem(x, 6, QTableWidgetItem(et))
            
            tachat = "Projet" if instance.type_achat==0 else "Siège"
            self.tableWidget.setItem(x, 7, QTableWidgetItem(tachat))
            dateq = instance.date_aq.strftime("%Y-%m-%d")
            self.tableWidget.setItem(x, 8, QTableWidgetItem(dateq))
            self.tableWidget.setItem(x, 9, QTableWidgetItem(str(instance.prix_ht)))
            
            if instance.garantie:
                self.tableWidget.setItem(x, 10, QTableWidgetItem(str(instance.garantie)))
            self.tableWidget.setItem(x, 11, QTableWidgetItem(instance.nbc))
            self.tableWidget.setItem(x, 12, QTableWidgetItem(instance.nfact))
            self.tableWidget.setItem(x, 13, QTableWidgetItem(instance.nomF))
            if instance.mat_emp:
                nomcomplet= instance.employe.nom+ " " + instance.employe.prenom
            else:
                nomcomplet = ""
            self.tableWidget.setItem(x, 14, QTableWidgetItem(nomcomplet))
            
            x += 1
    
    def searchDirectory(self):
        filedir = str(QFileDialog.getExistingDirectory(self, "Selectionner le dossier"))
        return filedir
    def genererQR(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            filedir = self.searchDirectory()
            if filedir:
                codeInvAffect = []
                for i in range(0, len(selected), self.nb_col):
                    codeInvAffect.append(selected[i].text())
                with Session(engine) as session:
                    for code in codeInvAffect:
                        eq = session.query(Informatique).filter_by(code_inv=code).one()
                        informationsQR = f'{eq.code_inv}/{eq.code_cat}/{eq.code_marque}/{eq.num_serie}/{eq.type}'
                        nomFichier = f'{eq.code_cat}-{eq.code_inv}'
                        self.creerQR(nomFichier, informationsQR, filedir)
                        msgbox = QMessageBox()
                        msgbox.setIcon(QMessageBox.Information)
                        msgbox.setText("Code(s) crée(s)")
                        msgbox.exec()
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner au moins un materiel pour génerer le(s) code(s) QR")
            msgbox.exec()
    
    def creerQR(self, nomfichier, informations, filedir):
        import qrcode
        import shutil
        import os
        img = qrcode.make(informations)
        img.save(f'{nomfichier}.png')
        oldpath = "E:\PFE\\app\\"+nomfichier+".png"
        newpath = filedir+"/"+nomfichier+".png"
        shutil.move(oldpath, newpath)
    
    def rechercher(self):
        choix_etat = self.choix_etat.currentText().lower()
        etat = {"stock":2, "en panne":1, "archive":3, "en service":0, "transferé": 4, "":None}[choix_etat]
        entry = self.recherche_code.text().strip()
        searchTypeIndex = self.recherche_combo.currentIndex()
        with Session(bind=engine) as session:
            if etat is None:
                if entry == "":
                    self.initListeMat()
                else:
                    if searchTypeIndex == 0: #code inventaire
                        result = session.query(Informatique).filter_by(code_inv=entry).all()
                    elif searchTypeIndex == 1: #Fournisseur
                        result = session.query(Informatique).filter_by(nomF=entry).all()
                    elif searchTypeIndex == 2: # Categorie
                        result = session.query(Informatique).filter_by(code_cat=entry).all()
                    self.remplirListeMat(result)
            else:
                if entry== "":
                    result = session.query(Informatique).filter_by(code_etat=etat).all()
                else:
                    if searchTypeIndex == 0: #code inventaire
                        result = session.query(Informatique).filter_by(code_inv=entry, code_etat=etat).all()
                    elif searchTypeIndex == 1: #Fournisseur
                        result = session.query(Informatique).filter_by(nomF=entry, code_etat=etat).all()
                    elif searchTypeIndex == 2: # Categorie
                        result = session.query(Informatique).filter_by(code_cat=entry, code_etat=etat).all()
                self.remplirListeMat(result)
    def initListeMat(self):
        with Session(engine) as session:
            result = session.query(Informatique).all()
            self.remplirListeMat(result)

class DialogTransfert(QDialog):
    # FIXME remove t146 from liste transfert destination.
    update_liste_mat = pyqtSignal()
    def __init__(self, selectedCodes, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "transfert.ui"), self)
        self.selectedCodes = selectedCodes
        with Session(engine) as session:
            listeF = session.query(Projet.code_projet).all()
        for f in listeF:
            self.comboBox.addItem(f[0])
        self.confirmer.clicked.connect(self.transferer)
        
    def transferer(self):
        codepDestin = self.comboBox.currentText()
        datetr = date.today()
        moyen = self.mdt.text().strip().title()
        nc = self.nomchauffeur.text().strip().title()
        user = Global.utilisateur
        
        liste_materiels= []
        with Session(engine) as session:
            t1 = Transfert(datet=datetr, moyent=moyen, nomC=nc, nom_util=user, projetD=codepDestin)
            session.add(t1)
            session.flush()
            for code in self.selectedCodes:
                result = session.query(Informatique).filter_by(code_inv=code).one()
                result.code_etat = 4
                result.ntransfer = t1.numt
                result.mat_emp = None
                liste_materiels.append(result)
        
            session.commit()
            self.update_liste_mat.emit()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setWindowTitle("Information")
            msgbox.setText("Succès")
            msgbox.buttonClicked.connect(self.close)
            msgbox.exec()
            
        