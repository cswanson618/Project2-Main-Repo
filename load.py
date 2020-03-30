# Dependencies 
import pandas as pd 
import requests 
from sqlalchemy import create_engine
import country_converter as coco
import datetime

from mySQLCredentials import *

# Get countries names and ISO3 
countries_url = "https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv"
countries_html = requests.get(countries_url).text
countries_df = pd.read_html(countries_html)[0]

# Covid-19 Confirmed Cases
confirmed_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
confirmed_html = requests.get(confirmed_url).text 
confirmed_df = pd.read_html(confirmed_html)[0]
confirmed_df = confirmed_df.iloc[:, 1:]
confirmed_df = confirmed_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'])
confirmed_df = confirmed_df.rename(columns={"Country/Region": "country_region", "Province/State": "province_state",  "Lat": "lat", "Long": "long", "variable":"date", "value": "confirmed"})

# Covid-19 Deaths
deaths_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
deaths_html = requests.get(deaths_url).text 
deaths_df = pd.read_html(deaths_html)[0]
deaths_df = deaths_df.iloc[:, 1:]
deaths_df = deaths_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'])
deaths_df = deaths_df.rename(columns={"Country/Region": "country_region", "Province/State": "province_state", "Lat": "lat", "Long": "long", "variable":"date", "value": "deaths"})

# Covid-19 Recovered
recovered_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
recovered_html = requests.get(recovered_url).text 
recovered_df = pd.read_html(recovered_html)[0]
recovered_df = recovered_df.iloc[:, 1:]
recovered_df = recovered_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'])
recovered_df = recovered_df.rename(columns={"Country/Region": "country_region", "Province/State": "province_state", "Lat": "lat", "Long": "long", "variable":"date", "value": "recovered"})

# Merge three dataframes
merged_df = pd.merge(confirmed_df, deaths_df, how="outer")
covid_df = pd.merge(merged_df, recovered_df, how="outer")

# Transform "Date" column into datatime format
covid_df["date"] = pd.to_datetime(covid_df["date"])

### Add column ISO3 to "covid_df"
# To avoid getting warnings..
not_country = ["Diamond Princess", "MS Zaandam"]
covid_df1 = covid_df.loc[~covid_df["country_region"].isin(not_country)]

cc = coco.CountryConverter()
covid_df1 = covid_df1.replace(to_replace="UK", value="United Kingdom")
country_list = list(covid_df1["country_region"])
standard_names = cc.convert(names=country_list, to="name_short")
covid_df1["iso3"] = cc.convert(names=standard_names, to="iso3")
covid_df = pd.merge(covid_df, covid_df1, how="outer")

# Create a customized dataframe for Sinah's plots
old_pop_df = pd.read_csv("older_pop_2018.csv")
covid_df2 = covid_df[["country_region", "date", "province_state", "confirmed", "deaths", "recovered"]]
covid_df2 = covid_df2.groupby(["country_region", "date"]).sum().reset_index()
covid_df2["case_fatality"] = round(covid_df2["deaths"] / covid_df2["confirmed"] * 100, 2)
covid_df3 = covid_df[["country_region", "iso3"]]
covid_df4 = pd.merge(covid_df2, covid_df3, how="left")
plot_df = pd.merge(covid_df4, old_pop_df, left_on="country_region", right_on="country", how="left")
plot_df = plot_df.drop_duplicates()
plot_df["date"] = plot_df["date"].dt.date
plot_df = plot_df.loc[plot_df["date"] >= datetime.date(2020,3,1)].reset_index().drop("index", axis=1)

# Connect to the "Covid" database in MySQL (CHANGE PASSWORD)
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = mySQLUsername
PASSWORD = mySQLPassword
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "Covid"
TABLE_WORLD_TIMESERIES = "world_timeseries"

connection_string = ( f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}" )
engine = create_engine(connection_string)

# Create "daily_cases" table in "Covid" database with "covid_db" dataframe
covid_df.to_sql(con=engine, name="daily_cases", if_exists="replace")
plot_df.to_sql(con=engine, name="plotting", if_exists="replace")
countries_df.to_sql(con=engine, name="countries", if_exists="replace")

# CREATE [OR REPLACE] [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name
engine.execute(f"DROP TABLE IF EXISTS {TABLE_WORLD_TIMESERIES}")

engine.execute(
    "CREATE table world_timeseries (id INT NOT NULL auto_increment, date datetime, total_confirmed bigint(20), total_deaths bigint(20), total_recovered bigint(20), primary key (id)) SELECT date, SUM(confirmed) as total_confirmed, SUM(deaths) as total_deaths, SUM(recovered) as total_recovered FROM Covid.daily_cases GROUP BY date"
    )




