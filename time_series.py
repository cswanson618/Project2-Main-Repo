# Dependencies 
import pandas as pd 
import requests 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
	
Base = declarative_base()

# Covid-19 Confirmed Cases
confirmed_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
confirmed_html = requests.get(confirmed_url).text 
confirmed_df = pd.read_html(confirmed_html)[0]
confirmed_df = confirmed_df.iloc[:, 2:].drop(columns = ["Lat", "Long"])
confirmed_df = confirmed_df.melt(id_vars=['Country/Region'])
confirmed_df = confirmed_df.rename(columns={"Country/Region": "country", "variable":"date"})
confirmed_df["date"] = pd.to_datetime(confirmed_df["date"])
confirmed_df = confirmed_df.groupby(["date", "country"])["value"].sum().to_frame().reset_index().set_index("date")

# Covid-19 Deaths 
deaths_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
deaths_html = requests.get(deaths_url).text 
deaths_df = pd.read_html(deaths_html)[0]
deaths_df = deaths_df.iloc[:, 2:].drop(columns = ["Lat", "Long"])
deaths_df = deaths_df.melt(id_vars=['Country/Region'])
deaths_df = deaths_df.rename(columns={"Country/Region": "country", "variable":"date"})
deaths_df["date"] = pd.to_datetime(deaths_df["date"])
deaths_df = deaths_df.groupby(["date", "country"])["value"].sum().to_frame().reset_index().set_index("date")

# Connect to the "Covid" Database in MySQL
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "kangsong87"
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "Covid"

connection_string = ( f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}" )
engine = create_engine(connection_string)
conn = engine.connect()
session = Session(bind=engine)

# Create tables in "Covid" db with the dataframes created 
confirmed_df.to_sql(con=engine, name="confirmed_timeseries", if_exists="replace")
deaths_df.to_sql(con=engine, name="deaths_timeseries", if_exists="replace")