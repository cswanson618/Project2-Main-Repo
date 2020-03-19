# Import Dependencies
import datetime
import pymysql

from flask import Flask, jsonify, request, render_template, url_for
import sqlalchemy
from sqlalchemy import create_engine, inspect, func, MetaData, desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# The database URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@127.0.0.1:3306/Covid"

db = SQLAlchemy(app)

# Create our database model

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(getattr(self, column.name), datetime.datetime)
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class Covid(db.Model, DictMixIn):
    __tablename__ = "daily_cases"

    iso3 = db.Column(db.String, primary_key=True)
    country_region = db.Column(db.String)
    province_state = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    date = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    recovered = db.Column(db.Integer)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/show_data")
def show_data():

    # Query for confirmed
    confirmed_cases = Covid.query.order_by(Covid.confirmed.desc()).all()
    
    return jsonify([confirmed.to_dict() for confirmed in confirmed_cases])

if __name__ == '__main__':
    app.run(debug=True)