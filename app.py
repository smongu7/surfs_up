# MODULE 9.4
# import flask
# from flask import Flask

# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello world'

# MODULE 9.5.1
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create func that allows access and query db
# engine = create_engine("sqlite:///hawaii.sqlite")
# add code to be able to refresh page
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={"check_same_thread": False})

# reflect db into classes
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# create variable for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session link fro python to db
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    return(
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    Available Routes:
    <p>/api/v1.0/precipitation</p>
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
# define stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# define temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# define stats route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)