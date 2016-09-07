from math import sqrt
import csv
from datetime import datetime
import random


class Station(object):
    def __init__(self, name, coordinates):
        self._name = name
        self._coords = coordinates

    def get_distance_from(self, coords):
        difference = (coords[0] - self._coords[0], coords[1] - self._coords[1])
        return sqrt(difference[0]**2 + difference[1]**2)

    def __str__(self):
        return self._name


class WeatherStation(Station):
    def get_weather(self, time):
        with open('weather_data/' + self._name + '.csv') as weatherFile:
            rowreader = csv.DictReader(
                weatherFile,
                quoting=csv.QUOTE_NONNUMERIC
                )
            mask = "%Y-%m-%d %H:%M:%S"
            row = next(rowreader)
            row["time"] = datetime.strptime(row['Timestamp'], mask)
            oldRow = row
            if row["time"] > time:
                raise ValueError("Time given is out of range")
            for row in rowreader:
                row["time"] = datetime.strptime(row['Timestamp'], mask)
                if row["time"] > time:

                    a = row["time"] - time
                    b = time - oldRow["time"]

                    oldComponent = timedelta_to_minutes(a) / (timedelta_to_minutes(a)+timedelta_to_minutes(b))
                    newComponent = timedelta_to_minutes(b) / (timedelta_to_minutes(a)+timedelta_to_minutes(b))

                    return ({
                        "Temperature": oldComponent*oldRow['Temperature'] + newComponent*row['Temperature'] + random.gauss(0,0.4),
                        "Humidity": oldComponent*oldRow['Humidity'] + newComponent*row['Humidity'] + random.gauss(0,1),
                        "Pressure": oldComponent*oldRow['Pressure'] + newComponent*row['Pressure'] + random.gauss(0,0.2)
                    })
                oldRow = row
            raise ValueError("Time given is out of range")


class PollutionStation(Station):
    def get_pollution(self, time):
        with open('pollution_data/' + self._name + '.csv') as pollutionFile:
            rowreader = csv.DictReader(
                pollutionFile,
                quoting=csv.QUOTE_NONNUMERIC
                )
            mask = "%Y-%m-%d %H:%M:%S"
            row = next(rowreader)
            timestamp = datetime.strptime(row['Timestamp'], mask)
            if timestamp > time:
                raise ValueError("Time given is out of range")
            for row in rowreader:
                timestamp = datetime.strptime(row['Timestamp'], mask)
                if timestamp > time:
                    return({
                        "NO": row['NO']
                    })
            raise ValueError("Time given is out of range")

def timedelta_to_minutes(td):
    return float(td.seconds//60)
