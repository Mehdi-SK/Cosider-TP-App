
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from GestionMateriels.MatAffectation import mat_affectation_info
from GestionMateriels.Transfert import Transfert
class Informatique(Base):
    __tablename__= "informatiques"
    
    # identification
    code_inv = Column(String(20), primary_key=True)
    num_serie = Column(String(20), unique=True, nullable=False)
    code_cat = Column(String(20), nullable=False)
    code_marque = Column(String(20), default="")
    type = Column(String(50), nullable=False)
    processeur = Column(String(20), nullable=False, default="sans-processeur")
    # etat
    code_etat = Column(Integer, nullable=False, default=0) # 0 en service, 1 en panne, 2 en stock, 3 archive
    # achat
    type_achat = Column(Integer, nullable=False, default=0) # 0 achat, 1 siege
    date_aq = Column(Date, nullable=False)
    prix_ht = Column(Integer, default=0)
    garantie = Column(Integer, default=0)
    nbc = Column(String(20))
    nfact = Column(String(20))
    # cle etrangere
    
    
    nomF = Column(String(50), ForeignKey("fournisseurs.nomf", ondelete="SET NULL"))
    ntransfer = Column(Integer, ForeignKey("transferts.numt", ondelete="SET NULL"), default=None)
    mat_emp = Column(String(30), ForeignKey("Employe.matricule", ondelete="SET NULL"))
    
    employe = relationship("Employe")
    transfert = relationship("Transfert")
    
    affectations = relationship("Affectation", secondary=mat_affectation_info, back_populates="matInfo")