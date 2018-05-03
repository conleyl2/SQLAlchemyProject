import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import datetime
from flask import Flask, jsonify

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
measure = Base.classes.hawaii_measure
station = Base.classes.hawaii_station
session = Session(engine)

@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a list of dates and temperatures"""

    sel = [measure.date, measure.tobs]
    lastyearprcp = session.query(*sel).filter(measure.date >= datetime.date(2017,5,2)).group_by(measure.date).all()

 
    prcp_dict = []
    for items in lastyearprcp:
        prcp_date = {}
        prcp_dict[lastyearprcp.date] = lastyearprcp.tobs_df

        prcp_dict.append(prcp_date)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stat():
    """Return a list of stations"""
    sel = [station.name]
    stat_name = session.querry(*sel).all()
    station_name = list(np.ravel(stat_name))
    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def temp():
    """Return a list of dates and temperatures last year"""

    sel = [measure.date, measure.tobs]
    lastyeartemp = session.query(*sel).filter(measure.date >= datetime.date(2017,5,2)).group_by(measure.date).all()

    temp_dict = []
    for items in lastyeartemp:
        temp_date = {}
        temp_dict[lastyeartemp.date] = lastyeartemp.tobs_df

        temp_dict.append(temp_date)

    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>")
def starting(start):
    """Temp data after a date"""
    temp_data = []
    start_date = start.split("-")
    start_datey = start_date[0]
    start_datem = start_date[1]
    start_dated = start_date[2]
    start_datey = start_datey - 1
    sel = [measure.date, measure.tobs]

    calc_temps = session.query(*sel).filter(measure.date >= datetime.date(start_datey, start_datem, start_dated)).group_by(measure.date).all()

    temps_df = pd.DataFrame(lastyeartemp, columns = ['date','tobs']) 
    temp_data.append(temps_df['tobs'].min())
    temp_data.append(temps_df['tobs'].max())
    temp_data.append(temps_df['tobs'].mean())
    return jstonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
     """Temp data between two dates"""
    temp_data = []
    start_date = start.split("-")
    end_date = end.split("-")
    start_datey = start_date[0]
    start_datem = start_date[1]
    start_dated = start_date[2]
    end_datey = end_date[0]
    end_datem = end_date[1]
    end_dated = end_date[2]
    start_datey = start_datey - 1
    end_datey = end_date -1

    sel = [measure.date, measure.tobs]

    calc_temps = session.query(*sel).filter(measure.date >= datetime.date(start_datey, start_datem, start_dated)).filter(measure.date <= datetime.date(end_datey, end_datem, end_dated)).group_by(measure.date).all()

    temps_df = pd.DataFrame(lastyeartemp, columns = ['date','tobs']) 
    temp_data.append(temps_df['tobs'].min())
    temp_data.append(temps_df['tobs'].max())
    temp_data.append(temps_df['tobs'].mean())
    return jstonify(temp_data)