# CONFIGURATION
DB_CONFIG = {'SERVER': 'DESKTOP-RALHEP6\MEHDI',
          'DATABASE': 'cosidertp',
          'DRIVER': 'ODBC Driver 17 for SQL Server'}

DATABASE_CONN_FORM = 'mssql://@{SERVER}/{DATABASE}?driver={DRIVER}' # DB connexion format

DATABASE_CONN_DEFAULT = DATABASE_CONN_FORM.format(**DB_CONFIG) # DB SETUP 



from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base



engine = create_engine(DATABASE_CONN_DEFAULT)

Base = declarative_base()

class Global():
    utilisateur = None
    