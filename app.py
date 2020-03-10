# Import Dependencies
from flask import Flask, jsonify, request, render_template, url_for
import sqlalchemy
from sqlalchemy import create_engine, inspect, func, MetaData, desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)