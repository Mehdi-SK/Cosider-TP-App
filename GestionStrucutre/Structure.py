from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from database import Base


class Structure(Base):
    __tablename__ = "structures"
    code_str = Column(String(10), primary_key=True)
    nom_str = Column(String(255), nullable=False)
    
    services = relationship(
        "Service",
        back_populates="structure",
        cascade="all, delete")