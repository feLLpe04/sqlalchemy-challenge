# Import dependencies
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Create Flask app
app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///hawaii.sqlite')

#Database into a new model
Base = automap_base()
Base.prepare(engine)

print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating Session
session = Session(engine)

# Define routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    # Convert to dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # Convert to list
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Example query for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    temperature_data = {date: tobs for date, tobs in results}
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start=None, end=None):
    #Return 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(map(lambda x: x, results))
    return jsonify(temps)

#Run the App 
if __name__ == '__main__':
    app.run(debug=True, port=5002)