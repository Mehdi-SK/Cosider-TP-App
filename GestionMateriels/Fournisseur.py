
from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Fournisseur(Base):
    __tablename__= "fournisseurs"
    nomf = Column(String(50), primary_key=True)
    numT = Column(String(20))
    email = Column(String(50))
    loc = Column(String(100))
    
    def __repr__(self) -> str:
        return f"<{self.nomf}, {self.numT}, {self.email}, {self.loc}>"