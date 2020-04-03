from typing import List

from flask import (
    Flask,
    _app_ctx_stack,
    jsonify,
    url_for,
    render_template,
    request,
    Flask,
)
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from sqlalchemy import (
    func,
    MetaData,
    desc,
    Column,
    Integer,
    String,
    DateTime,
    table,
    Date,
    create_engine,
    inspect,
)

from . import models
from .database import SessionLocal, engine
from .plot import bar_div, bubble_div

import json

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def home():
    deaths = int(json.loads(globaltimeseries())[-1].get("Deaths"))
    cases = int(json.loads(globaltimeseries())[-1].get("Cases"))
    recovered = int(json.loads(globaltimeseries())[-1].get("Recovered"))
    return render_template(
        "index.html", bar=bar_div, deaths=deaths, cases=cases, recovered=recovered
    )


@app.route("/routes")
def routes():
    return render_template("routes.html")


# API Route 1: Most Recent Totals for Every Country Worldwide
@app.route("/API/most_recent")
def worldwidetotals():
    subquery1 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidetotals = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(models.Cases.date.in_(subquery1))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict = []
    for item in worldwidetotals:
        dict.append(
            {
                "country": item[0],
                "Date": str(item[1]),
                "Cases": item[2],
                "Deaths": item[3],
                "Recovered": item[4],
            }
        )
    dicts = json.dumps(dict)
    return dicts


# API Route 2: Most Recent Confirmed Cases for Every Country Worldwide


@app.route("/API/cases")
def worldwidecases():
    subquery2 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidecases = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(models.Cases.date.in_(subquery2))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict2 = []
    for item in worldwidecases:
        dict2.append(
            {"country": item[0], "Cases": item[2], "Last Update": str(item[1])}
        )
    dicts2 = json.dumps(dict2)
    return dicts2


# API Route 3: Most Recent Deaths for Every Country Worldwide


@app.route("/API/dead")
def worldwidedead():
    subquery3 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidedead = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(models.Cases.date.in_(subquery3))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict3 = []
    for item in worldwidedead:
        dict3.append(
            {"country": item[0], "Deaths": item[3], "Last Update": str(item[1])}
        )
    dicts3 = json.dumps(dict3)
    return dicts3


# API Route 4: Most Recent Number of Recoveries for Every Country Worldwide


@app.route("/API/recovered")
def worldwiderecovered():
    subquery4 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwiderecovered = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(models.Cases.date.in_(subquery4))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict4 = []
    for item in worldwiderecovered:
        dict4.append(
            {"country": item[0], "Recovered": item[4], "Last Update": str(item[1])}
        )
    dicts4 = json.dumps(dict4)
    return dicts4


# API Route 5: Most Recent Totals by Country


@app.route("/API/<iso3>")
def countrytotals(iso3):
    subquery5 = app.session.query(func.max(models.Cases.date)).subquery()
    countrytotals = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery5))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict5 = []
    for item in countrytotals:
        dict5.append(
            {
                "country": item[0],
                "Last Update": str(item[1]),
                "Cases": item[2],
                "Deaths": item[3],
                "Recovered": item[4],
            }
        )
    dicts5 = json.dumps(dict5)
    return dicts5


# API Route 6: Most Recent Cases by Country


@app.route("/API/cases/<iso3>")
def countrycases(iso3):
    subquery6 = app.session.query(func.max(models.Cases.date)).subquery()
    countrycases = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery6))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict6 = []
    for item in countrycases:
        dict6.append(
            {"country": item[0], "Cases": item[2], "Last Updated": str(item[1])}
        )
    dicts6 = json.dumps(dict6)
    return dicts6


# API Route 7: Most Recent Dead by Country


@app.route("/API/dead/<iso3>")
def countrydead(iso3):
    subquery7 = app.session.query(func.max(models.Cases.date)).subquery()
    countrydead = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery7))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict7 = []
    for item in countrydead:
        dict7.append(
            {"country": item[0], "Deaths": item[3], "Last Update": str(item[1])}
        )
    dicts7 = json.dumps(dict7)
    return dicts7


# API Route 8: Most Recent Recovered by Country


@app.route("/API/recovered/<iso3>")
def countryrecovered(iso3):
    subquery8 = app.session.query(func.max(models.Cases.date)).subquery()
    countryrecovered = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .filter(models.Cases.date.in_(subquery8))
        .group_by(models.Cases.iso3)
        .all()
    )
    dict8 = []
    for item in countryrecovered:
        dict8.append(
            {"country": item[0], "Recovered": item[4], "Last Update": str(item[1]),}
        )
    dicts8 = json.dumps(dict8)
    return dicts8


# API Route 9: Country Timeseries


@app.route("/API/<iso3>/timeseries/")
def countrytimeseries(iso3):
    countrytimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict9 = []
    for item in countrytimeseries:
        dict9.append(
            {
                "country": item[0],
                "Total Results as of Date": str(item[1]),
                "Cases": item[2],
                "Deaths": item[3],
                "Recovered": item[4],
            }
        )
    dicts9 = json.dumps(dict9)
    return dicts9


# API Route 10: Global Timeseries


@app.route("/API/timeseries/")
def globaltimeseries():
    globaltimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .group_by(models.Cases.date)
        .all()
    )
    dict10 = []
    for item in globaltimeseries:
        dict10.append(
            {
                "Total Results as of Date": str(item[1]),
                "Cases": item[2],
                "Deaths": item[3],
                "Recovered": item[4],
            }
        )
    dicts10 = json.dumps(dict10)
    return dicts10


# API Route 11: Global Timeseries for Cases


@app.route("/API/cases/timeseries")
def casestimeseries():
    casestimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .group_by(models.Cases.date)
        .all()
    )
    dict11 = []
    for item in casestimeseries:
        dict11.append(
            {"Total Results as of Date": str(item[1]), "Cases": item[2],}
        )
    dicts11 = json.dumps(dict11)
    return dicts11


# API Route 12: Global Timeseries for Deaths
@app.route("/API/dead/timeseries")
def deadtimeseries():
    deadtimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .group_by(models.Cases.date)
        .all()
    )
    dict12 = []
    for item in deadtimeseries:
        dict12.append(
            {"Total Results as of Date": str(item[1]), "Deaths": item[3],}
        )
    dicts12 = json.dumps(dict12)
    return dicts12


# API Route 13: Global Timeseries for Recoveries
@app.route("/API/recovered/timeseries")
def recoveredtimeseries():
    recoveredtimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .group_by(models.Cases.date)
        .all()
    )
    dict13 = []
    for item in recoveredtimeseries:
        dict13.append(
            {"Total Results as of Date": str(item[1]), "Recovered": item[4],}
        )
    dicts13 = json.dumps(dict13)
    return dicts13


# API Route 14: Country Timeseries for Cases


@app.route("/API/cases/<iso3>/timeseries")
def countrycasestimeseries(iso3):
    countrycasestimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict14 = []
    for item in countrycasestimeseries:
        dict14.append(
            {"Total Results as of Date": str(item[1]), "Cases": item[2],}
        )
    dicts14 = json.dumps(dict14)
    return dicts14


# API Route 15: Country Timeseries for Deaths
@app.route("/API/dead/<iso3>/timeseries")
def countrydeadtimeseries(iso3):
    countrydeadtimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .filter(iso3 == models.Cases.iso3)
        .group_by(models.Cases.date)
        .all()
    )
    dict15 = []
    for item in countrydeadtimeseries:
        dict15.append(
            {"Total Results as of Date": str(item[1]), "Deaths": item[3],}
        )
    dicts15 = json.dumps(dict15)
    return dicts15


# API Route 16: Country Timeseries for Recoveries
@app.route("/API/recovered/<iso3>/timeseries")
def countryrecoveredtimeseries(iso3):
    countryrecoveredtimeseries = (
        app.session.query(
            models.Cases.country_region,
            models.Cases.date,
            func.sum(models.Cases.confirmed),
            func.sum(models.Cases.deaths),
            func.sum(models.Cases.recovered),
        )
        .group_by(models.Cases.date)
        .all()
    )
    dict16 = []
    for item in countryrecoveredtimeseries:
        dict16.append(
            {"Total Results as of Date": str(item[1]), "Recovered": item[4],}
        )
    dicts16 = json.dumps(dict16)
    return dicts16


# All records (from Daniela)
@app.route("/records/")
def show_records():
    cases = app.session.query(models.Cases).all()
    return jsonify([record.to_dict() for record in records])


# All cases by date by country (from Daniela).
@app.route("/country/<iso3>")
def country_by_ISO3(iso3):
    try:
        country = app.session.query(models.Record).filter_by(iso3=iso3).all()
        return jsonify([record.to_dict() for record in country])
    except:
        return jsonify()


# World cases (from Daniela)
@app.route("/total_world")
def total_world():
    totals = app.session.query(models.WorldTotalRecords).all()
    return jsonify([record.to_dict() for record in totals])


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/plot")
def render_plots():
    return render_template("plot.html", bar=bar_div, bubble=bubble_div)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
