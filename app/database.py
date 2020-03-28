from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import sys
import os
sys.path.append(os.path.join('..'))
from mySQLCredentials import *

USER = mySQLUsername
PASSWORD = mySQLPassword
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "covid"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}", echo=False)

engine.execute(f"USE {DATABASE}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
