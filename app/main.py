from typing import List

from flask import Flask, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from sqlalchemy import func

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def main():
    return f"See the data at {url_for('show_records')}"


# All records
@app.route("/records/")
def show_records():
    records = app.session.query(models.Record).all()
    return jsonify([record.to_dict() for record in records])


# All cases by date in USA
@app.route("/usa")
def usa():
    usa = (
        app.session.query(models.Record).filter_by(iso3='USA').all()
    )
    return jsonify([record.to_dict() for record in usa])

# World cases
@app.route("/total_world")
def total_world():
    totals = app.session.query(models.WorldTotalRecords).all()
    return jsonify([record.to_dict() for record in totals])


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


