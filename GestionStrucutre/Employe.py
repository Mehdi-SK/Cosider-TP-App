from database import Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
class Employe(Base):
    __tablename__= "Employe"
    
    matricule = Column(String(30), primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    poste = Column(String(100), nullable=False)
    genre = Column(Boolean, nullable=False) # homme=0 femme=1
    code_dep = Column(String(10), ForeignKey("departements.code_dep"))
    
    departement = relationship("Departement")
    