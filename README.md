# SQL Alchemy Challenge

Planning a long holiday vacation in Honolulu, Hawaii. To help with my trip planning, I did some climate analysis on the area.  By accessing weather Hawaii weather data from a number of weather stations, I will be able to get names of stations, precipitation, temperature, latitutude, and longitude data. 

## Observation Analysis on the following:

* Precipitation: Retrieve the last 12 months of precipitation data selecting only 'date' and 'prcp'. Load data into dataframe and plot.
* Station: Calculate total number of stations. List most active stations, observation counts, plot results.
* Temperature: Meaningful difference between the temperature in, for example, June and December? T-Test to compare. Min, Avg, Max temps for specific dates of the trip.
* Daily Rainfall Average: Rainfall per station, daily normals, load into dataframe.

### Libraries, Databases, Apps:

* Flask, Matplotlib, NumPy, Pandas, Datetime, SQLAlchemy, SciPy
* SQLite
* VSCode (app.py)

### Climate_Analysis

All analysis work is displayed within this notebook.

### App.py

Using Flask, the following is being returned through specific web links:

* Station, Name, and Prcp data
* List of stations 
* Temperature Observations of most active station for the last year
* Custom begin date to latest date min, avg, max temperature.
* Custom begin and end date min, avg, max temperature.