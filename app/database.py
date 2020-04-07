from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import sys
import os
sys.path.append(os.path.join('..'))
from mySQLCredentials import *

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = mySQLUsername
PASSWORD = mySQLPassword
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "Covid"

connection_string = (
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
)

engine = create_engine(connection_string, echo=False)

engine.execute(f"USE {DATABASE}")
engine.execute(f"SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
