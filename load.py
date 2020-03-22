# Dependencies 
import pandas as pd 
import requests 
from sqlalchemy import create_engine
import country_converter as coco

# Get countries names and ISO3 
countries_url = "https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv"
countries_html = requests.get(countries_url).text
countries_df = pd.read_html(countries_html)[0]

# Covid-19 Confirmed Cases
confirmed_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
confirmed_html = requests.get(confirmed_url).text 
confirmed_df = pd.read_html(confirmed_html)[0]
confirmed_df = confirmed_df.iloc[:, 1:]
confirmed_df = confirmed_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'])
confirmed_df = confirmed_df.rename(columns={"Country/Region": "country", "Province/State": "state", "variable":"date", "value": "confirmed"})

# Covid-19 Deaths
deaths_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
deaths_html = requests.get(deaths_url).text 
deaths_df = pd.read_html(deaths_html)[0]
deaths_df = deaths_df.iloc[:, 1:]
deaths_df = deaths_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'])
deaths_df = deaths_df.rename(columns={"Country/Region": "country", "Province/State": "state", "variable":"date", "value": "deaths"})

# Covid-19 Recovered
recovered_url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
recovered_html = requests.get(recovered_url).text 
recovered_df = pd.read_html(recovered_html)[0]
recovered_df = recovered_df.iloc[:, 1:]
recovered_df = recovered_df.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long'])
recovered_df = recovered_df.rename(columns={"Country/Region": "country", "Province/State": "state", "variable":"date", "value": "recovered"})

# Merge three dataframes
merged_df = pd.merge(confirmed_df, deaths_df)
covid_df = pd.merge(merged_df, recovered_df)

# Transform "Date" column into datatime format
covid_df["date"] = pd.to_datetime(covid_df["date"])

### Add column ISO3 to "covid_df" ###
# covid_df1 = covid_df.loc[covid_df["country"] != "Cruise Ship"]
# cc = coco.CountryConverter()
# covid_df1 = covid_df1.replace(to_replace="UK", value="United Kingdom")
# country_list = list(covid_df1["country"])
# standard_names = cc.convert(names=country_list, to="name_short")
# covid_df1["iso3"] = cc.convert(names=standard_names, to="iso3")
# covid_df = pd.merge(covid_df, covid_df1, how="outer")

## Summary table 
# we are not sure if the most current date is today or yesterday.
last_update = [covid_df["date"].max()]
total_countries_infected = covid_df["country"].nunique() - 1
# Find the total number per date
confirmed_byDate = covid_df.groupby("date").sum()["confirmed"]
# The last value is the total world
total_confirmed_world = confirmed_byDate[-1]
# Find total deaths
deaths_byDate = covid_df.groupby("date").sum()["deaths"]
total_deaths_world = deaths_byDate[-1]
# Find total deaths
recovered_byDate = covid_df.groupby("date").sum()["recovered"]
total_recovered_world = recovered_byDate[-1]

summary = pd.DataFrame(
    {
        "total_confirmed_world": total_confirmed_world,
        "total_deaths_world": total_deaths_world,
        "total_recovered_world": total_recovered_world,
        "total_countries_infected": total_countries_infected,
        "last_update": last_update,
    }
)

# Aggregate by county
# confirmed_by_country_df = covid_df.groupby(["date", "country"])["confirmed"].sum().to_frame().reset_index()

# Connect to the "Covid" database in MySQL (CHANGE PASSWORD)
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "kangsong87"
DIALECT = "mysql"
DRIVER = "pymysql"
DATABASE = "Covid"

connection_string = ( f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}" )
engine = create_engine(connection_string)

# Create "daily_cases" table in "Covid" database with "covid_db" dataframe
covid_df.to_sql(con=engine, name="daily_cases", if_exists="replace")
summary.to_sql(con=engine, name="summary", if_exists="replace")
countries_df.to_sql(con=engine, name="countries", if_exists="replace")

# engine.execute(
#     "CREATE table world_timeseries (id INT NOT NULL auto_increment, date datetime, total_confirmed bigint(20), total_deaths bigint(20), total_recovered bigint(20), primary key (id)) SELECT date, SUM(confirmed) as total_confirmed, SUM(deaths) as total_deaths, SUM(recovered) as total_recovered FROM Covid.daily_cases GROUP BY date"
#     )
