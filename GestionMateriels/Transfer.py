from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Transfer(Base):
    __tablename__="transfers"
    numt = Column(Integer, primary_key=True)
    datet = Column(DateTime, nullable=False)
    moyent = Column(String(50))
    nomC = Column(String(255))
    projetD = Column(String(10), ForeignKey("Projets.code_projet", ondelete="SET NULL"))
    id_util = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    
    projet = relationship("Projet")
    user = relationship("Utilisateur")