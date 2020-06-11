import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


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
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"/api/v1.0/YYYY-MM-DD <br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD (start date/end date)<br/>"
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

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates

@app.route("/api/v1.0/<start_date>")
def Start_Date_Search(start_date):
    """Fetch the beginning date requested when 'start' matches
       the path variable supplied by the user, or a 404 if not."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    

    # Fetch latest date in dataset
    latest_date = (session.query(Measurement.date)
               .order_by(Measurement.date.desc()).first())
    latest_date = ''.join(map(str, latest_date))

    try:
        # Verify date input matches date in dataset
        input_date = (session.query(Measurement.date)
        .filter(Measurement.date == start_date).first())
        input_date = ''.join(map(str, input_date))
    except:
        return jsonify({"error": f"{start_date} not found. Date given is not located in database or wrong format. Date format is 'YYYY-MM-DD'."}), 404
        

    def calc_temps(start_date):
        """TMIN, TAVG, and TMAX for a list of dates.
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
            
        Returns:
            TMIN, TAVE, and TMAX
            
        """
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= latest_date).all()

    # session.close()

    # Get input, lower text for matching purposes. Date may not apply but input anyways
    canonicalized = start_date.replace(" ", "").lower()
    
    # Verify input with database
    search_term = input_date.replace(" ", "").lower()


    if search_term == canonicalized:
        results = calc_temps(start_date)
        return jsonify(results)

    else:
        return jsonify({"error": f"{start_date} not found. Date given is not located in database or wrong format. Date format is 'YYYY-MM-DD'."}), 404
       
    



# @app.route("/api/v1.0/<start>/<end>")
# # * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# #   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# #   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>/<end_date>")
def End_Date_Search(start_date, end_date):
    """Fetch the beginning date requested when 'start' matches
       the path variable supplied by the user, or a 404 if not."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    

    try:
        # Verify date input matches date in dataset
        input_date = (session.query(Measurement.date)
        .filter(Measurement.date == start_date).first())
        input_date = ''.join(map(str, input_date))
    except:
        return jsonify({"error": f"{start_date} not found. Date given is not located in database or wrong format. Date format is 'YYYY-MM-DD'."}), 404
        
    try:
        # Verify date input matches date in dataset
        input_end_date = (session.query(Measurement.date)
        .filter(Measurement.date == end_date).first())
        input_end_date = ''.join(map(str, input_end_date))
    except:
        return jsonify({"error": f"{end_date} not found. Date given is not located in database or wrong format. Date format is 'YYYY-MM-DD'."}), 404
           
    # Get min, avg, max of dates passed
    def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
            
        Returns:
            TMIN, TAVE, and TMAX
            
        """
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # session.close()


    # Get input, lower text for matching purposes. Date may not apply but input anyways
    canonicalized = start_date.replace(" ", "").lower()
    canonicalized_end = end_date.replace(" ", "").lower()

    # Verify input with database
    search_term = input_date.replace(" ", "").lower()
    search_term_end = input_end_date.replace(" ", "").lower()

    # (search_term, search_term_end) = (canonicalized, canonicalized)
    if (search_term, search_term_end) == (canonicalized, canonicalized_end):
        results = calc_temps(start_date, end_date)
        return jsonify(results)

    else:
        return jsonify({"error": f"Start and End date provided do not match after verifying with the database. Start: {start_date}, End: {end_date}."}), 404


if __name__ == '__main__':
    app.run(debug=True)

