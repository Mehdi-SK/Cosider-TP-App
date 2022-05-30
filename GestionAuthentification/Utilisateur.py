
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column,String, Integer, create_engine
from Global import DATABASE_CONN

Base = declarative_base()


class Utilisateur(Base):
    __tablename__= 'utilisateurs'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True, nullable=False)
    mot_de_passe= Column(String(20), nullable=False)
    admin_flag = Column(Integer, default=0)
    
    def __repr__(self) -> str:
        return '<ID : {0} Login : {1}, Mot de passe : {2}, Admin flag : {3}>'.format(self.id,
                                                                                     self.login, 
                                                                                    self.mot_de_passe,
                                                                                    self.admin_flag)

# Base.metadata.create_all(engine)
# engine = create_engine(DATABASE_CONN)
# Session = sessionmaker(bind=engine)


# with Session() as session:
#    results = session.query(Utilisateur).order_by(Utilisateur.id)
#    print(type(results))
    
