from database import engine
from sqlalchemy.orm import Session
from GestionStrucutre.Projet import Projet
with Session(bind=engine) as session:
    listeProjets = session.query(Projet).all()
        
        
    print(*listeProjets)