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
# convert to normal list
    list_results = list(np.ravel(results))
#results
    msr_date = [result[0] for result in results[:365]]
    prcp_msr = [str(result[1]) for result in results[:365]]

    session.close()

    # Convert list of tuples into normal list
    dict_create = [{msr_date : prcp_msr}]

    return jsonify(dict_create)


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
    
    station_12count = session.query(Measurement.tobs).\
                filter(Measurement.station=='USC00519281').\
                filter(Measurement.date >= month_length).all()

    session.close()

    form_correct = list(np.ravel(station_12count))

    return jsonify(form_correct)

    #how to add date side-by-side

if __name__ == '__main__':
    app.run(debug=True)