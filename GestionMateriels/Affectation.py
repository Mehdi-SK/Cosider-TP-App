from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Affectation(Base):
    __tablename__ ="Affectations"
    numa = Column(Integer, primary_key=True)
    date_affectation = Column(DateTime, nullable=False)
    mat_emp = Column(String(30), ForeignKey("Employe.matricule", ondelete="SET NULL"))
    id_util = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    
    employe = relationship("Employe")
    user = relationship("Utilisateur")