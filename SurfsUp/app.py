# Import the dependencies.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# def home():
#     print("Testing")
#     return "Testing"

#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect the tables
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Stationary Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to my Page</h1> <br/>"
        f"/precipitation<br/>"
        f"/station<br/>"
        f"/tobs<br/>"
        f"/data/start<br/>"
        f"/data/start/end"
    )

@app.route("/precipitation")
def precipitation():
    session = Session(engine)
    # Query all precipitation data
    lastest_date = (
        session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    )
    # define date- 12M prior to last data point
    one_yr_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_yr_before
    # Get precipitation data for the last year using filter
    results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= one_yr_before)
        .order_by(Measurement.date.desc())
        .all()
    )

    session.close()
    # Convert output in to format where date=key and prcp = result
    ret_dict = {res.date: res.prcp for res in results}

    # precip_lastyr = list(np.ravel(ret_dict))
    # return jsonify(list([list(x)for x in results]))
    return jsonify(ret_dict)


@app.route("/station")
def station():
    session = Session(engine)
    # select all data from measurement table
    sel_data = session.query(
        (Measurement.id),
        (Measurement.station),
        (Measurement.prcp),
        (Measurement.tobs),
        (Measurement.date),
    ).all()
    session.close()
    sel_data_mod = list(np.ravel(sel_data))
    return jsonify(sel_data_mod)


@app.route("/tobs")
def tobs():
    session = Session(engine)
    # define date- 12M prior to last data point
    one_yr_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_yr_before
    # select all data from measurement table and filter on top station and previous 12 mon of data
    sel_all_data = (
        session.query(Measurement.tobs, Measurement.date)
        .filter(Measurement.station == "USC00519281")
        .filter(Measurement.date >= one_yr_before)
        .all()
    )
    session.close()
    sel_data_top = list(np.ravel(sel_all_data))
    return jsonify(sel_data_top)

# Flask Dynamic Routes
#################################################
@app.route("/data/<start>")
@app.route("/data/<start>/<end>")
def data(start=None,end=None):
    session = Session(engine)
    if not end:
        start_dt = dt.datetime.strptime(start, "%m%d%Y")

        data_filter = (
            session.query(
                func.min(Measurement.tobs),
                func.max(Measurement.tobs),
                func.avg(Measurement.tobs),
            )
            .filter(Measurement.date >= start_dt)
            .all()
        )
    start_dt = dt.datetime.strptime(start, "%m%d%Y")
    end_dt= dt.datetime.strptime(end,"%m%d%Y")
    data_filter = (
        session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs),
            )
            .filter(Measurement.date >= start_dt).filter(Measurement.date<=end_dt)
            .all()
    )
    session.close()
    data_filter_ob = list(np.ravel(data_filter))
    return jsonify(data_filter_ob)


if __name__ == "__main__":
    app.run(debug=True)
