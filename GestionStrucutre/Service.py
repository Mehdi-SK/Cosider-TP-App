from sqlalchemy import String, Column
from database import Base


class Service(Base):
    __tablename__ = "services"
    code_service = Column(String(10), primary_key=True)
    nom_service = Column(String(255), nullable=False)
    
    