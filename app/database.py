import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
import sys
import os
sys.path.append(os.path.join('..'))

# HOSTNAME = "127.0.0.1"
# PORT = 3306
# USERNAME = mySQLUsername
# PASSWORD = mySQLPassword
# DIALECT = "mysql"
# DRIVER = "pymysql"
# DATABASE = "Covid"

connection_string = (sqlalchemy.engine.url.URL(drivername= "mysql+pymysql", username= "root", password= "ehaarmanny", database= "Covid", query= {"unix_socket": "/cloudsql/{}".format("project2-270717:us-central1:covid2019")},))

engine = create_engine(connection_string, echo=False)

# engine.execute(f"USE {DATABASE}")
# engine.execute(f"SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()