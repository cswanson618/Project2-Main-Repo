# Creating the table coountries 

import requests
import pandas as pd
from sqlalchemy import create_engine


# Get countries names and ISO3 and create a table in our database
url_countries = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.csv"
df_countries = pd.read_csv(url_countries)

#connect to DB and create new table with csv data
engine = create_engine(f"mysql+pymysql://root:Amd230313@localhost/Covid")
with engine.connect() as conn, conn.begin():
    df_countries.to_sql("countries", conn, index=False)