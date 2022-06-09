
from database import Base, engine
from sqlalchemy.orm import Session




def init_db():
    from GestionAuthentification.Utilisateur import Utilisateur
    from GestionStrucutre.Employe import Employe
    from GestionStrucutre.Projet import Projet
    from GestionStrucutre.Service import Service
      
    
    Base.metadata.create_all(bind=engine)
    
    with Session(bind=engine) as session:
        try: 
            session.add(Utilisateur(id="0", login="Admin", mot_de_passe="Admin", admin_flag=1))
            session.commit()
        except :
            pass 

if __name__=="__main__":
    init_db()   