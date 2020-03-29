from typing import List

from flask import Flask, _app_ctx_stack, jsonify, url_for, render_template, request, Flask
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from sqlalchemy import func, MetaData, desc, Column, Integer, String, DateTime, table, Date, create_engine, inspect

from . import models
from .database import SessionLocal, engine

import json

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/routes")
def routes():
    return render_template("routes.html")


#API Route 1: Most Recent Totals Worldwide (duplicates functionality at the moment; this will replace queries below)

@app.route("/API/most_recent")
def worldwidetotals():
    subquery1 = app.session.query(func.max(models.Cases.date)).subquery()
    worldwidetotals = app.session.query(models.Cases.country_region, models.Cases.date, func.sum(models.Cases.confirmed), func.sum(models.Cases.deaths), func.sum(models.Cases.recovered)).filter(models.Cases.date.in_(subquery1)).group_by(models.Cases.iso3).all()
    dict = []
    for item in worldwidetotals:
        dict.append({
            "country": item[0],
            "Date": str(item[1]),
            "Cases": item[2],
            "Deaths": item[3],
            "Recovered": item[4]
        })
    dicts = json.dumps(dict)
    return dicts

#All records (from Daniela)
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

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


