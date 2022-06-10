from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Departement(Base):
    __tablename__ = "departements"
    code_dep = Column(String(10), primary_key=True)
    nom_dep = Column(String(255), nullable=False)
    code_service = Column(String(10), ForeignKey('services.code_service', ondelete="CASCADE"), nullable=False)
    
    service = relationship("Service", back_populates="departements")
    
