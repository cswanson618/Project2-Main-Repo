from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

USER = "root"
PASSWORD = "Amd230313"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "Covid"

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Amd230313@127.0.0.1:3306/Covid"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}", echo=False)

engine.execute(f"USE {DATABASE}")

# engine = create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
