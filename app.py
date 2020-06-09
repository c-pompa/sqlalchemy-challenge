import numpy as np

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
#   * Home page.
#   * List all routes that are available.
def Welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.
def Precipitation_dict():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and prcp measurements from Measurement table"""
    # Query all date and prcp measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of date_prcp_data
    date_prcp_data = []
    for datee, prcpp in results:
        date_prcp_dict = {}
        date_prcp_dict[datee] = prcpp
        date_prcp_data.append(date_prcp_dict)

    return jsonify(date_prcp_data)


@app.route("/api/v1.0/stations")
#  * Return a JSON list of stations from the dataset.
def Station_List():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station and station names from Station table"""
    # Query all date and prcp measurements
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations_list
    stations_list = []
    for ss, sn in results:
        stations_dict = {}
        stations_dict['station'] = ss
        stations_dict['name'] = sn
        stations_list.append(stations_dict)

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
#   * Query the dates and temperature observations of the most active station for the last year of data.
#   * Return a JSON list of temperature observations (TOBS) for the previous year.
def Temp_Obs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and temperature observations
    Highest_observation = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    columns = [Measurement.date, Measurement.tobs]

    results = (session.query(*columns)
                 .filter(Measurement.date > '2016-08-18')
                #  .filter(Measurement.tobs == meas_highest_tobs_top)
                 .order_by(Measurement.date.desc()).all())

    session.close()

    # Create a dictionary from the row data and append to a list of stations_list
    temp_obs_list = []
    for datee, tobss in results:
        tobs_dict = {}
        tobs_dict['date'] = datee
        tobs_dict['tobs'] = tobss
        temp_obs_list.append(tobs_dict)

    return jsonify(temp_obs_list)
    

# @app.route("/api/v1.0/<start>")
# # * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# #   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# #   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# def passengers():



# @app.route("/api/v1.0/<start>/<end>")
# # * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# #   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# #   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# def passengers():



if __name__ == '__main__':
    app.run(debug=True)









#################################################
# Flask Routes
# #################################################

# @app.route("/")
# def welcome():
#     """List all available api routes."""
#     return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/names<br/>"
#         f"/api/v1.0/passengers"
#     )


# @app.route("/api/v1.0/names")
# def names():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Passenger.name).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


# if __name__ == '__main__':
#     app.run(debug=True)
