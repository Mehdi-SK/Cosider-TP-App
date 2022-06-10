from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from database import Base


class Service(Base):
    __tablename__ = "services"
    code_service = Column(String(10), primary_key=True)
    nom_service = Column(String(255), nullable=False)
    
    departements = relationship(
        "Departement",
        back_populates="service",
        cascade="all, delete")
    
    