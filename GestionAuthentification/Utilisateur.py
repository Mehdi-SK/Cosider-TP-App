from sqlalchemy import Column,String, Integer

from database import Base


class Utilisateur(Base):
    __tablename__= 'utilisateurs'
    login = Column(String(20), primary_key=True)
    mot_de_passe= Column(String(20), nullable=False)
    admin_flag = Column(Integer, default=0)
    def __repr__(self) -> str:
        return '<Login : {0}, Mot de passe : {1}, Admin flag : {2}>'.format(self.login, 
                                                                            self.mot_de_passe,
                                                                            self.admin_flag)

    


