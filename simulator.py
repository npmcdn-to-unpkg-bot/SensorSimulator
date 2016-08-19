import math
import csv
from datetime import datetime


class Airport:
    """Airport Class"""
    def __init__(self, name, coordinates):
        self._name = name
        self._coords = coordinates

    def getWeather(self, time):
        with open('weather_data/' + self._name + '.csv') as weatherFile:
            rowreader = csv.DictReader(weatherFile)
            for row in rowreader:
                mask = "%Y-%m-%d %H:%M:%S"
                timestamp = datetime.strptime(row['Timestamp'], mask)
                if timestamp > time:
                    return float(row['Temperature'])
            raise ValueError("Time given is out of range")

    def get_distance(self, coords):
        difference = (coords[0] - self._coords[0], coords[1] - self._coords[1])
        return math.sqrt(difference[0]**2 + difference[1]**2)

    def __str__(self):
        return self._name


class SensorSimulator:
    def __init__(self):
        self._airports = [
            Airport("heathrow", (51.4775, -0.461389)),
            Airport("luton", (51.874722, -0.368333)),
            Airport("oxford", (51.835882, -1.317293))
        ]

    def add_airport(self, name, coordinates):
        self._airports.append(Airport(name, coordinates))

    def closest_airport(self, coords):
        return min(self._airports, key=lambda x: x.get_distance(coords))

    def temp_at_coords(self, time, coords):
        airport = self.closest_airport(coords)
        return airport.getWeather(time)
