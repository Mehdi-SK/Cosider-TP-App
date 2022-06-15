

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Transfert(Base):
    __tablename__="transferts"
    numt = Column(Integer, primary_key=True)
    datet = Column(Date, nullable=False)
    moyent = Column(String(50))
    nomC = Column(String(255))
    projetD = Column(String(10), ForeignKey("Projets.code_projet", ondelete="SET NULL"))
    nom_util = Column(String(20), ForeignKey("utilisateurs.login", ondelete="SET NULL"))
    
    projet = relationship("Projet")
    user = relationship("Utilisateur")
    
    equip_info = relationship("Informatique", back_populates="transfert")
    equip_bureau = relationship("Bureautique", back_populates="transfert")