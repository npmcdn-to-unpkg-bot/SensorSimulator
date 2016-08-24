import math
import csv
from datetime import datetime, timedelta


class Airport:
    """Airport Class"""
    def __init__(self, name, coordinates):
        self._name = name
        self._coords = coordinates

    def get_weather(self, time):
        with open('weather_data/' + self._name + '.csv') as weatherFile:
            rowreader = csv.DictReader(weatherFile, quoting=csv.QUOTE_NONNUMERIC)
            mask = "%Y-%m-%d %H:%M:%S"
            row = next(rowreader)
            timestamp = datetime.strptime(row['Timestamp'], mask)
            if timestamp > time:
                raise ValueError("Time given is out of range")
            for row in rowreader:
                timestamp = datetime.strptime(row['Timestamp'], mask)
                if timestamp > time:
                    return row['Temperature']
            raise ValueError("Time given is out of range")

    def get_distance_from(self, coords):
        difference = (coords[0] - self._coords[0], coords[1] - self._coords[1])
        return math.sqrt(difference[0]**2 + difference[1]**2)

    def __str__(self):
        return self._name


class SensorSimulator:
    """Sensor Simulator Class"""
    def __init__(self):
        self._airports = [
            Airport("heathrow", (51.4775, -0.461389)),
            Airport("luton", (51.874722, -0.368333)),
            Airport("oxford", (51.835882, -1.317293))
        ]

    def add_airport(self, name, coordinates):
        self._airports.append(Airport(name, coordinates))

    def closest_airport(self, coords):
        return min(self._airports, key=lambda x: x.get_distance_from(coords))

    def weather_at(self, time, coords):
        airport = self.closest_airport(coords)
        return airport.get_weather(time)


class VanSimulator:
    """Van Simulator Class"""
    def __init__(self, routeFile):
        self.rowreader = csv.DictReader(routeFile, quoting=csv.QUOTE_NONNUMERIC)

        row = next(self.rowreader)

        self.current_position = (row['Longitude'], row['Latitude'])
        self.current_time = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")

    def get_weather(self):
        sensor = SensorSimulator()
        return sensor.weather_at(self.current_time, self.current_position)
