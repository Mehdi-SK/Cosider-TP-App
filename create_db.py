
from database import Base, engine
from sqlalchemy.orm import Session




def init_db():
    from GestionAuthentification.Utilisateur import Utilisateur
    from GestionStrucutre.Employe import Employe
    from GestionStrucutre.Projet import Projet
    from GestionStrucutre.Service import Service
    from GestionStrucutre.Structure import Structure
    from GestionMateriels.Informatique import Informatique  
    from GestionMateriels.Bureautique import Bureautique
    from GestionMateriels.Affectation import Affectation, mat_affectation_bureau, mat_affectation_info
    from GestionMateriels.Transfert import Transfert
    from GestionMateriels.Fournisseur import Fournisseur
    
    Base.metadata.create_all(bind=engine)
    
    with Session(bind=engine) as session:
        try: 
            session.add(Utilisateur(login="Admin", mot_de_passe="Admin", admin_flag=1))
            session.commit()
        except :
            pass 

if __name__=="__main__":
    init_db()   