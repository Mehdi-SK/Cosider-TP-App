from database import Base
from sqlalchemy import Column, String, Integer, Boolean

class Projet(Base):
    __tablename__= "Projets"
    code_projet = Column(String(10), primary_key=True)
    nom_projet = Column(String(255), nullable=False)
    adresse =  Column(String(255))
    
    def __repr__(self) -> str:
        return "<Code Projet={0}, Nom Projet={1}, Adresse={2}>".format(self.code_projet,
                                                                      self.nom_projet,
                                                                      self.adresse)


