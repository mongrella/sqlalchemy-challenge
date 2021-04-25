# Import Dependencies
import numpy as np


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create an engine 
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save a reference to measurement and station
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Home page
#List all routes that are available.
#NEED MORE WORK ON THIS
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


#/api/v1.0/precipitation
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)
   
    """Return a list of all precipitation"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

# Create a dictionary from the list of precipitation

    all_precipitation = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

#/api/v1.0/stations
#Return a JSON list of stations from the dataset in descending order.
@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).order_by(Station.station.desc()).all()
    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)


#/api/v1.0/tobs
#Query the dates and temperature observations of the most active station 
# for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temperature observations for station USC00519281"""
    # Query all tobs for the previous year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-8-23').order_by(Measurement.date).all()
    
    session.close()

    # Convert list into a dictionary
    active_station = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        active_station.append(tobs_dict)

    return jsonify(active_station)



#/api/v1.0/<start> and /api/v1.0/<start>/<end>

#When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
# greater than and equal to the start date.
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""
    #Query all TOBS

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from data and append

    start_temp = []
    for date, min, avg, max in results:
        start_temp_dict = {}
        start_temp_dict["date"] = date
        start_temp_dict["TMIN"] = min
        start_temp_dict["TAVG"] = avg
        start_temp_dict["TMAX"] = max

        start_temp.append(start_temp_dict)

    return jsonify(start_temp)



#When given the start and the end date, calculate the TMIN, TAVG, 
# and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of TMIN, TAVG, and TMAX for all dates between start/end date"""
    #Query all TOBS

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from data and append

    start_end_temp = []
    for date, min, avg, max in results:
        start_end_temp_dict = {}
        start_end_temp_dict["date"] = date
        start_end_temp_dict["TMIN"] = min
        start_end_temp_dict["TAVG"] = avg
        start_end_temp_dict["TMAX"] = max

        start_end_temp.append(start_end_temp_dict)

    return jsonify(start_end_temp)

if __name__ == '__main__':
    app.run(debug=True)