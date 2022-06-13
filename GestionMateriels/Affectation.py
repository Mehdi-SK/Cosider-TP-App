
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from GestionMateriels.Bureautique import Bureautique
from GestionMateriels.Informatique import Informatique
from GestionMateriels.MatAffectation import mat_affectation_bureau, mat_affectation_info


class Affectation(Base):
    __tablename__ ="affectations"
    numa = Column(Integer, primary_key=True)
    date_affectation = Column(Date, nullable=False)
    mat_emp = Column(String(30), ForeignKey("Employe.matricule", ondelete="SET NULL"))
    nom_util = Column(String(20), ForeignKey("utilisateurs.login", ondelete="SET NULL"))
    
    employe = relationship("Employe")
    
    matInfo = relationship("Informatique", secondary=mat_affectation_info, back_populates="affectations")
    matBureau = relationship("Bureautique", secondary=mat_affectation_bureau, back_populates="affectations")




