from datetime import date
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from PyQt5.QtGui import QIntValidator,QIcon
from os import path
from GestionMateriels.Bureautique import Bureautique
from GestionMateriels.Fournisseur import Fournisseur

from GestionMateriels.Affectation import Affectation
from sqlalchemy.orm import Session
from sqlalchemy import or_
from GestionMateriels.Transfert import Transfert
from GestionStrucutre.Employe import Employe
from GestionStrucutre.Projet import Projet
from database import Global, engine



class ListMatBureauUi(QWidget):
    def __init__(self, parent=None, adminFlag=1):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), 'listeMatBureau.ui'), self)
        
         # Table Widget
        liste_columns = ["Code Inventaire", "Désignation", "Catégorie", "Marque", "Etat",
                         "Type Achat", "Date Acquisition", "Prix HT",
                         "Garantie(Mois)", "NBon de commande", "NFacture", "Fournisseur","Affecté à"]
        self.nb_col = len(liste_columns)
        self.tableWidget.setColumnCount(self.nb_col)
        self.tableWidget.setHorizontalHeaderLabels(liste_columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ajouter_button.clicked.connect(self.ouvrirMenuAjout)
        self.modifier_button.clicked.connect(self.ouvrirMenuModification)
        self.affecter_button.clicked.connect(self.ouvrirAffectation)
        self.transfer_button.clicked.connect(self.ouvrirTransfert)
        self.qr_button.clicked.connect(self.genererQR)
        self.initListeMat()
        
        
        
        
    def remplirListeMat(self, listemat):
        taille = len(listemat)
        self.tableWidget.setRowCount(taille)
        x = 0
        for instance in listemat:
            self.tableWidget.setItem(x, 0, QTableWidgetItem(instance.code_inv))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(instance.desig))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(instance.code_cat))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(instance.code_marque))
            
            # 0 en service, 1 en panne, 2 en stock, 3 archive, 4 transfert
            et = {0:"En service", 1:"En panne", 2:"Stock", 3:"Archive",
                  4:"Transferé"}[instance.code_etat]
            self.tableWidget.setItem(x,4, QTableWidgetItem(et))
            
            tachat = "Projet" if instance.type_achat==0 else "Siège"
            self.tableWidget.setItem(x, 5, QTableWidgetItem(tachat))
            dateq = instance.date_aq.strftime("%Y-%m-%d")
            self.tableWidget.setItem(x, 6, QTableWidgetItem(dateq))
            self.tableWidget.setItem(x, 7, QTableWidgetItem(str(instance.prix_ht)))
            
            if instance.garantie:
                self.tableWidget.setItem(x, 8, QTableWidgetItem(str(instance.garantie)))
            self.tableWidget.setItem(x, 9, QTableWidgetItem(instance.nbc))
            self.tableWidget.setItem(x, 10, QTableWidgetItem(instance.nfact))
            self.tableWidget.setItem(x, 11, QTableWidgetItem(instance.nomF))
            if instance.mat_emp:
                nomcomplet= instance.employe.nom+ " " + instance.employe.prenom
            else:
                nomcomplet = ""
            self.tableWidget.setItem(x, 12, QTableWidgetItem(nomcomplet))
            
            x += 1
      
      
    def ouvrirMenuAjout(self):
        self.menuaj = DialogAjout()
        self.menuaj.show()
        self.menuaj.update_liste_fr.connect(self.initListeMat)

    
    def ouvrirMenuModification(self):
        selected = self.tableWidget.selectedItems()

        if len(selected) == 0 or len(selected)>13:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Erreur")
            msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText("Selectionner un seul materiel à modifier")
            msgbox.exec()
        else:
            with Session(engine) as session:
                result = session.query(Bureautique).filter_by(code_inv=selected[0].text()).all()
            
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
            
            listeDejaT = []
            with Session(engine) as session:
                for code in codeInvTransfert:
                    result = session.query(Bureautique).filter_by(code_inv=code).one()
                    if result.code_etat == 4:
                        listeDejaT.append(result.code_inv)
            if len(listeDejaT) != 0:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setWindowTitle("Erreur")
                msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
                msg = "\n".join(listeDejaT)
                msgbox.setText("Ces materiels sont déja transferés:\n"+msg)
                msgbox.exec()
            else:
                self.dialogTransfert = DialogTransfert(codeInvTransfert)
                self.dialogTransfert.show()
                self.dialogTransfert.update_liste_mat.connect(self.initListeMat)
        else:
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
            msgbox.setText("Selectionner au moins un materiel à transférer.")
            msgbox.exec()
    
        
    def initListeMat(self):
        with Session(engine) as session:
            result = session.query(Bureautique).all()
            self.remplirListeMat(result)
    
    def searchDirectory(self):
        filedir = str(QFileDialog.getExistingDirectory(self, "Selectionner le dossier"))
        return filedir
    def genererQR(self):
        selected = self.tableWidget.selectedItems()
        if len(selected) != 0:
            filedir = self.searchDirectory()
            if filedir:
                codeInvAffect = []
                for i in range(0, len(selected)):
                    if selected[i].column()==0:
                        codeInvAffect.append(selected[i].text())
                with Session(engine) as session:
                    for code in codeInvAffect:
                        eq = session.query(Bureautique).filter_by(code_inv=code).one()
                        informationsQR = f'{eq.code_inv}/{eq.code_cat}/{eq.code_marque}/{eq.desig}'
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
        from os.path import dirname, abspath
        img = qrcode.make(informations)
        img.save(f'{nomfichier}.png')
        old = dirname(dirname(abspath(__file__)))
        oldpath = old+"\\"+nomfichier+".png"
        newpath = filedir+"/"+nomfichier+".png"
        shutil.move(oldpath, newpath)
    

        
            
            
            
            
class DialogAjout(QDialog):
    update_liste_fr = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "ajouter_mat_bureau.ui"), self)
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
        desig = self.designation.text().strip()
        ccat = self.codecat.text().strip().upper()
        mq = self.mrq.text().strip().upper()
        choix_etat = self.et.currentText().lower()
        # 0 en service, 1 en panne, 2 en stock, 3 archive
        etat = {"stock":2, "en panne":1, "archive":3, "en service":0, "transferé": 4}[choix_etat]
        # infos d'achat
        achat = self.tachat.currentIndex()
        dt = self.dtacq.date().toPyDate()
        prxht = self.prixHTLineEdit.text().strip()
        grt = self.garantieLineEdit.text()
        nbc = self.numBCLineEdit.text().strip()
        nfct = self.numFactureLineEdit.text().strip()
        nfr = self.nomFournisseurComboBox.currentText()
        if cinv and ccat and mq  and prxht and nbc and nfct:
            mat1 = Bureautique(code_inv=cinv,
                                desig=desig,
                                code_cat=ccat,
                                code_marque=mq,
                                code_etat=etat,
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
                check = session.query(Bureautique).filter(Bureautique.code_inv==mat1.code_inv).count()
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
        msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
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


# ____________________Modifier__________
class DialogModifier(QDialog):
    update_liste_mat = pyqtSignal()
    def __init__(self, selected:Bureautique, parent=None):
        super().__init__(parent)
    
        loadUi(path.join(path.dirname(__file__), "modifier_mat_bureau.ui"), self)
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
        self.desig.setText(self.selected.desig)
        self.codecat.setText(self.selected.code_cat)
        self.mrq.setText(self.selected.code_marque)
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
            mat1 = session.query(Bureautique).filter_by(code_inv=cinv).one()

            ccat = self.codecat.text().strip().upper()
            mq = self.mrq.text().strip().upper()
            desig = self.desig.text().strip().title()
            choix_etat = self.et.currentText().lower()
            # 0 en service, 1 en panne, 2 en stock, 3 archive
            etat = {"stock":2, "en panne":1, "archive":3, "en service":0, "transferé":4}[choix_etat]
            achat = self.tachat.currentIndex()
            dt = self.dtacq.date().toPyDate()

            prxht = self.prixHTLineEdit.text().strip()
            grt = self.garantieLineEdit.text()
            nbc = self.numBCLineEdit.text().strip()
            nfct = self.numFactureLineEdit.text().strip()
            nfr = self.nomFournisseurComboBox.currentText()
            
            if ccat and mq and prxht and nbc and nfct:
                try:
                    mat1.code_cat=ccat
                    mat1.code_marque = mq
                    mat1.desig=desig
                    mat1.code_etat=etat
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
        msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
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
        
# _____________________ AFFECTER__________________________
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
                        result = session.query(Bureautique).filter_by(code_inv=code).one()
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
                        msgb.setWindowIcon(QIcon("./Interfaces/icon.png"))
                        msgb.setText("Ces materiels sont déjà affecté à(" + matemp+"):\n"+msgs)
                        msgb.exec()
                    if len(mat_affect) !=0:
                        affect = Affectation(date_affectation=dateaff, mat_emp=matemp, nom_util=user, matBureau=mat_affect)
                        session.add(affect)
                    
                        for materiel in mat_affect:
                            materiel.mat_emp = matemp
                            materiel.code_etat = 0
                            
                        session.commit()
                        self.update_liste_mat.emit()
                        msgbox = QMessageBox()
                        msgbox.setIcon(QMessageBox.Information)
                        msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
                        msgbox.setWindowTitle("Information")
                        msgbox.setText("Succès")
                        msgbox.buttonClicked.connect(self.close)
                        msgbox.exec()
                        
            except Exception as e:
                msgbox = QMessageBox()
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
                msgbox.setWindowTitle("Erreur")
                msgbox.setText("Erreur")
                print(e)
                msgbox.exec()
    
# ________________Transfert__________________
class DialogTransfert(QDialog):
    update_liste_mat = pyqtSignal()
    def __init__(self, selectedCodes, parent=None):
        super().__init__(parent)
        loadUi(path.join(path.dirname(__file__), "transfert.ui"), self)
        self.selectedCodes = selectedCodes
        with Session(engine) as session:
            listeF = session.query(Projet.code_projet).all()
        for f in listeF:
            if f[0] !="T146": self.comboBox.addItem(f[0])
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
                result = session.query(Bureautique).filter_by(code_inv=code).one()
                result.code_etat = 4
                result.ntransfer = t1.numt
                result.mat_emp = None
                liste_materiels.append(result)
        
            session.commit()
            self.update_liste_mat.emit()
            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setWindowTitle("Information")
            msgbox.setWindowIcon(QIcon("./Interfaces/icon.png"))
            msgbox.setText("Succès")
            msgbox.buttonClicked.connect(self.close)
            msgbox.exec()


    


