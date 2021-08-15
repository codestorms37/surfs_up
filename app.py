# 9.5.1 Set Up the Database and Flask

# Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

# The conection shouldn´t be inside the functions in order to open and close as soon as possible??????????????????

# setup database
# The create_engine() function allows us to access and query our SQLite database file.
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes.
Base = automap_base()
Base.prepare(engine, reflect=True)

# save our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
# session = Session(engine)



# Set Up Flask
# create a Flask application called "app"
app = Flask(__name__)

# Important Note:
myNote = '''

Notice the __name__ variable in this code.
This is a special type of variable in Python.
Its value depends on where and how the code is run.
For example, if we wanted to import our app.py file into another Python file named example.py,
the variable __name__ would be set to example. Here's an example of what that might look like:

import app

print("example __name__ = %s", __name__)

if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")

However, when we run the script with python app.py, 
the __name__ variable will be set to __main__. 
This indicates that we are not using any other file to run this code.

'''

# 9.5.2 Create the Welcome Route

@app.route("/")

def welcome():
    return render_template('welcome.html')

# 9.5.3 Precipitation Route

@app.route("/api/v1.0/precipitation")

def precipitation():

    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation} # I dont understand this ??????????????
    return jsonify(precip)

# 9.5.4 Stations Route

@app.route("/api/v1.0/stations")

def stations():

    session = Session(engine)

    results = session.query(Station.station).all()
    stations = list(np.ravel(results)) # What is ravel??????????????????
    return jsonify(stations=stations) # stations=stations ?????????????????????????????


# 9.5.5 Monthly Temperature Route

@app.route("/api/v1.0/tobs")

def temp_monthly():

    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    #print(results)
    
    temps = list(np.ravel(results))
    
    return jsonify(temps=temps)


# 9.5.6 Statistics Route

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):

    session = Session(engine)

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
