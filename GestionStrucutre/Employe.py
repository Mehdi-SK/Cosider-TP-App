from database import Base
from sqlalchemy import Column, String, Integer, Boolean

class Employe(Base):
    __tablename__= "Employe"
    
    matricule = Column(String(30), primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    poste = Column(String(100), nullable=False)
    genre = Column(Boolean, nullable=False) # homme=0 femme=1
    