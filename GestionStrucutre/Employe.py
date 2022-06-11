from email.policy import default
from database import Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
class Employe(Base):
    __tablename__= "Employe"
    
    matricule = Column(String(30), primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    genre = Column(Boolean, nullable=False) # Femme = true, Homme= false
    poste = Column(String(100), nullable=False)
    code_dep = Column(String(10), ForeignKey("departements.code_dep", ondelete='SET NULL'))
    archive = Column(Boolean, default=False) 
    
    departement = relationship("Departement")
    
    def __repr__(self) -> str:
        return f"{self.matricule}, {self.nom}, {self.prenom},{self.genre}, {self.poste}, {self.code_dep} "