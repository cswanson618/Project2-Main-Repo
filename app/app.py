# Import Dependencies 
from typing import List

from flask import Flask, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

# import datetime
# import pymysql
# import main

# from flask import Flask, jsonify, request, render_template, url_for
# from sqlalchemy import func
# from flask_sqlalchemy import SQLAlchemy



@app.route("/")
def home():
    return render_template("d_index.html")


@app.route("/data_by_country")
def data_by_country():

    # Query to bring the object in descinding order
    confirmed_cases = Covid.query.order_by(Covid.confirmed.desc()).all()
    return jsonify([confirmed.to_dict() for confirmed in confirmed_cases])

# @app.route("/trends")
# def trends():

    # SELECT date, SUM(confirmed), SUM(deaths), SUM(recovered) FROM Covid.daily_cases GROUP BY date

    # trends = db.session.query( 
    #                             Covid.date.label('date'),
    #                             func.sum(Covid.confirmed).label('total_confirmed'), 
    #                             func.sum(Covid.deaths).label('total_deaths'), 
    #                             func.sum(Covid.recovered).label('total_recovered')
    #                          ).group_by(Covid.date).all()

    # # return jsonify(trends)

    # test = Covid.query.all()
    # return jsonify([t.to_dict() for t in test])

@app.route("/date/")
def show_date():
    dates = app.session.query(Covid.date).all()
    print (jsonify([d.to_dict() for d in dates]))


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()

if __name__ == '__main__':
    app.run(debug=True)