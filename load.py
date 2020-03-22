import pandas as pd
import country_converter as coco
import pycountry_convert
import pymysql
import warnings

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta


# Imported raw data
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

# Convert the data to a dataFrame
df_confirmed = pd.read_csv(url_confirmed)
df_deaths = pd.read_csv(url_deaths)
df_recovered = pd.read_csv(url_recovered)


# Organize columns name to make it easy to work
df_confirmed.columns = (
    df_confirmed.columns.str.strip().str.lower().str.replace("/", "_")
)
df_deaths.columns = df_deaths.columns.str.strip().str.lower().str.replace("/", "_")
df_recovered.columns = (
    df_recovered.columns.str.strip().str.lower().str.replace("/", "_")
)

# Change "UK" for "United Kingdom"
df_confirmed = df_confirmed.replace(to_replace="UK", value="United Kingdom")

df_deaths = df_deaths.replace(to_replace="UK", value="United Kingdom")

df_recovered = df_recovered.replace(to_replace="UK", value="United Kingdom")

# Add column ISO3 to each table
some_names_confirmed = list(df_confirmed.country_region)
standard_names = coco.convert(
    names=some_names_confirmed, to="name_short", not_found="n/a"
)
iso3_codes = coco.convert(names=standard_names, to="iso3", not_found=None)
df_confirmed["iso3"] = iso3_codes

some_names_deaths = list(df_deaths.country_region)
standard_names = coco.convert(names=some_names_deaths, to="name_short", not_found="n/a")
iso3_codes = coco.convert(names=standard_names, to="iso3", not_found=None)
df_deaths["iso3"] = iso3_codes

some_names_recovered = list(df_recovered.country_region)
standard_names = coco.convert(
    names=some_names_recovered, to="name_short", not_found="n/a"
)
iso3_codes = coco.convert(names=standard_names, to="iso3", not_found=None)
df_recovered["iso3"] = iso3_codes

# Change columns date position from columns to rows
df_confirmed = df_confirmed.melt(
    id_vars=["iso3", "country_region", "province_state", "lat", "long"]
).rename(columns={"variable": "date", "value": "confirmed"})
df_deaths = df_deaths.melt(
    id_vars=["iso3", "country_region", "province_state", "lat", "long"]
).rename(columns={"variable": "date", "value": "confirmed"})
df_recovered = df_recovered.melt(
    id_vars=["iso3", "country_region", "province_state", "lat", "long"]
).rename(columns={"variable": "date", "value": "confirmed"})

# Fix the date format
df_confirmed["date"] = df_confirmed["date"].str.replace("_", "-")
df_deaths["date"] = df_deaths["date"].str.replace("_", "-")
df_recovered["date"] = df_recovered["date"].str.replace("_", "-")

# Join the 3 tables
df_merged = pd.merge(
    df_confirmed,
    df_deaths,
    on=["iso3", "country_region", "province_state", "lat", "long", "date"],
)
df_merged = pd.merge(
    df_merged,
    df_recovered,
    on=["iso3", "country_region", "province_state", "lat", "long", "date"],
)

# Rename columns to confirmed, deaths and recovered
df_merged = df_merged.rename(
    columns={
        "confirmed_x": "confirmed",
        "confirmed_y": "deaths",
        "confirmed": "recovered",
    }
)

# Format datetime and set index to be used as primary key
df_merged["date"] = pd.to_datetime(df_merged["date"], format="%m-%d-%y")
df_merged = df_merged.reset_index()

# Make the Covid table a html table
covid_table_html = df_merged.to_html()

# Create another table with totals

# we are not sure if the most current date is today or yesterday.
last_update = [df_merged["date"].max()]

total_countries_infected = df_merged["iso3"].nunique()

# Find the total number per date
confirmed_byDate = df_merged.groupby("date").sum()["confirmed"]
# The last value is the total world
total_confirmed_world = confirmed_byDate[-1]
# Find total deaths
deaths_byDate = df_merged.groupby("date").sum()["deaths"]
total_deaths_world = deaths_byDate[-1]
# Find total deaths
recovered_byDate = df_merged.groupby("date").sum()["recovered"]
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


# Insert tables to Covid Database in MySQL with 3 tables
USER = "root"
PASSWORD = "Amd230313"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "Covid"
TABLE_CASES = "daily_cases"
TABLE_SUMMARY = "summary"
TABLE_WORLD_TIMESERIES = "world_timeseries"

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}", echo=False)

engine.execute(f"USE {DATABASE}")

# Drop the tables so we can insert new updated data
engine.execute(f"DROP TABLE IF EXISTS {TABLE_CASES}")
engine.execute(f"DROP TABLE IF EXISTS {TABLE_SUMMARY}")
engine.execute(f"DROP TABLE IF EXISTS {TABLE_WORLD_TIMESERIES}")

# Insert the dataframe into our database Covid
df_merged.to_sql(name="daily_cases", con=engine, index=False)
summary.to_sql(name="summary", con=engine, index=False)

engine.execute(
    "CREATE table world_timeseries (id INT NOT NULL auto_increment, date datetime, total_confirmed bigint(20), total_deaths bigint(20), total_recovered bigint(20), primary key (id)) SELECT date, SUM(confirmed) as total_confirmed, SUM(deaths) as total_deaths, SUM(recovered) as total_recovered FROM Covid.daily_cases GROUP BY date"
    )

