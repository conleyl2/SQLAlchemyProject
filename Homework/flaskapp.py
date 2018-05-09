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

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measure = Base.classes.hawaii_measure
station = Base.classes.hawaii_station
session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def prcp():

    sel = [measure.date, measure.tobs]
    lastyearprcp = session.query(*sel).filter(measure.date >= datetime.date(2017,5,2)).group_by(measure.date).all()
    prcpdata = list(np.ravel(lastyearprcp))

    return jsonify(prcpdata)

@app.route("/api/v1.0/stations")
def stat():
    sel = [station.name]
    stat_name = session.query(*sel).all()
    station_name = list(np.ravel(stat_name))
    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def temp():

    sel = [measure.date, measure.tobs]
    lastyeartemp = session.query(*sel).filter(measure.date >= datetime.date(2017,5,2)).group_by(measure.date).all()
    tempdata = list(np.ravel(lastyeartemp))

    return jsonify(tempdata)

@app.route("/api/v1.0/<start>")
def starting(start):
    temp_data = []
    date = datetime.datetime.strptime(start, "%Y-%m-%d")
    start_datey = date.year
    start_datem = date.month
    start_dated = date.day
    start_datey = date.year - 1
    sel = [measure.date, measure.tobs]

    calc_temps = session.query(*sel).filter(measure.date >= datetime.date(start_datey, start_datem, start_dated)).group_by(measure.date).all()

    temps_df = pd.DataFrame(calc_temps, columns = ['date','tobs']) 
    temp_data.append(str(temps_df['tobs'].min()))
    temp_data.append(str(temps_df['tobs'].max()))
    temp_data.append(str(temps_df['tobs'].mean()))
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    temp_data = []
    sdate = datetime.datetime.strptime(start, "%Y-%m-%d")
    edate = datetime.datetime.strptime(end, "%Y-%m-%d")
    start_datem = sdate.month
    start_dated = sdate.day
    start_datey = sdate.year - 1

    end_datem = edate.month
    end_dated = edate.day
    end_datey = edate.year - 1

    sel = [measure.date, measure.tobs]

    calc_temps = session.query(*sel).filter(measure.date >= datetime.date(start_datey, start_datem, start_dated)).filter(measure.date <= datetime.date(end_datey, end_datem, end_dated)).group_by(measure.date).all()

    temps_df = pd.DataFrame(calc_temps, columns = ['date','tobs']) 
    temp_data.append(str(temps_df['tobs'].min()))
    temp_data.append(str(temps_df['tobs'].max()))
    temp_data.append(str(temps_df['tobs'].mean()))
    return jsonify(temp_data)
if __name__ == '__main__':
    app.run(debug=True)