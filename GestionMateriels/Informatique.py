
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from GestionMateriels.Affectation import Affectation
from GestionMateriels.Transfert import Transfert
class Informatique(Base):
    __tablename__= "informatiques"
    
    code_inv = Column(String(20), primary_key=True)
    num_serie = Column(String(20), unique=True, nullable=False)
    code_cat = Column(String(20), nullable=False)
    desig = Column(String(255))
    code_marque = Column(String(20), default="")
    type = Column(String(50), nullable=False)
    processeur = Column(String(20), nullable=False, default="sans-processeur")
    code_etat = Column(Integer, nullable=False, default=0) # 0 en service, 1 en panne, 2 en stock, 3 archive
    type_achat = Column(Integer, nullable=False, default=0) # 0 achat, 1 siege
    date_aq = Column(Date, nullable=False)
    prix_ht = Column(Integer, default=0)
    garantie = Column(Integer, default=0)
    nbc = Column(String(20))
    nfact = Column(String(20))
    nomF = Column(String(50), ForeignKey("fournisseurs.nomf", ondelete="SET NULL"))
    naffect = Column(Integer, ForeignKey("Affectations.numa", ondelete="SET NULL"), default=None)
    ntransfer = Column(Integer, ForeignKey("transferts.numt", ondelete="SET NULL"), default=None)
   
    affectation = relationship("Affectation", back_populates="equip_info")
    transfert = relationship("Transfert", back_populates="equip_info")