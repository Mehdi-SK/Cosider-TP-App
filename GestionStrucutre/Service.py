from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.orm import relationship
from database import Base


class Service(Base):
    __tablename__ = "services"
    code_service = Column(String(10), primary_key=True)
    nom_service = Column(String(255), nullable=False)
    code_str = Column(String(10), ForeignKey('structures.code_str', ondelete="CASCADE"), nullable=False)
    
    structure = relationship(
        "Structure",
        back_populates="services",
        cascade="all, delete")
    
    