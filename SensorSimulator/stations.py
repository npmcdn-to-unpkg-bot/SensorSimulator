from math import sqrt
import csv
from datetime import datetime


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
            timestamp = datetime.strptime(row['Timestamp'], mask)
            if timestamp > time:
                raise ValueError("Time given is out of range")
            for row in rowreader:
                timestamp = datetime.strptime(row['Timestamp'], mask)
                if timestamp > time:
                    return ({
                        "Temperature": row['Temperature'],
                        "Humidity": row['Humidity'],
                        "Pressure": row['Pressure']
                    })
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
