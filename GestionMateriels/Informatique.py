
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Informatique(Base):
    __tablename__= "informatiques"
    
    code_inv = Column(String(20), primary_key=True)
    num_serie = Column(String(20), unique=True, nullable=False)
    code_cat = Column(String(20), nullable=False)
    code_marque = Column(String(20), default="")
    type = Column(String(50), nullable=False)
    processeur = Column(String(20), nullable=False, default="sans-processeur")
    code_etat = Column(Integer, nullabe=False, default=0) # 0 en utilisation, 1 en panne, 2 archive
    type_achat = Column(Integer, nullable=False, default=0) # 0 achat, 1 siege
    date_aq = Column(DateTime, nullable=False)
    prix_ht = Column(Integer, default=0)
    garantie = Column(Integer, default=0)
    nbc = Column(String(20))
    nfact = Column(String(20))
    mat_emp = Column(String(30), ForeignKey("Employe.matricule", ondelete="SET NULL"))
    
    proprietaire = relationship("Employe")