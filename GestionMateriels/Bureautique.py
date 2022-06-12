
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Bureautique(Base):
    __tablename__= "bureautiques"
    
    # informations d'identification
    code_inv = Column(String(20), primary_key=True)
    code_cat = Column(String(20), nullable=False)
    desig = Column(String(255))
    code_marque = Column(String(20), default="")
    type = Column(String(50), nullable=False)
    # confirmation d'etat
    code_etat = Column(Integer, nullable=False, default=0) # 0 en service, 1 en panne, 2 en stock, 3 archive
    #informations d'achat
    type_achat = Column(Integer, nullable=False, default=0) # 0 achat, 1 siege
    date_aq = Column(Date, nullable=False)
    prix_ht = Column(Integer, default=0)
    garantie = Column(Integer, default=0)
    nbc = Column(String(20))
    nfact = Column(String(20))
    # cle etrangere
    nomF = Column(String(50), ForeignKey("fournisseurs.nomf", ondelete="SET NULL"))
    naffect = Column(Integer, ForeignKey("Affectations.numa", ondelete="SET NULL"))
    ntransfer = Column(Integer, ForeignKey("transferts.numt", ondelete="SET NULL"))
    
    transfer = relationship("Transfert")
    affectation = relationship("Affectation")