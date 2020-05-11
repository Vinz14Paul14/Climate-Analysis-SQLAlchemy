import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    month_length = dt.date(2017,8,23) - dt.timedelta(days=365)
    month_length
# Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= month_length).\
        order_by(Measurement.date.desc()).all()
    
    session.close

    all_measurements = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["precipitation"] = prcp
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    stations_name = list(np.ravel(results))

    return jsonify(stations_name)

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    month_length = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    station_12count = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station=='USC00519281').\
                filter(Measurement.date >= month_length).all()

    session.close()

    form_correct = list(np.ravel(station_12count))

    return jsonify(form_correct)

@app.route("/api/v1.0/<start>")
def date_test(start):
#   Create our session (link) from Python to the D
    session = Session(engine)

# Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp)
    
    session.close

    all_measurements = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["precipitation"] = prcp
        all_measurements.append(measurement_dict)

    canonicalized = date
    for test_date in all_measurements:
        search_term = test_date["date"]

        if search_term == canonicalized:
            return jsonify(test_date)

    # results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    #         filter(Measurement.date=='USC00519281').all()


if __name__ == '__main__':
    app.run(debug=True)