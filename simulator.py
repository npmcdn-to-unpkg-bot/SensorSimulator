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
            rowreader = csv.DictReader(weatherFile)
            mask = "%Y-%m-%d %H:%M:%S"
            row = next(rowreader)
            timestamp = datetime.strptime(row['Timestamp'], mask)
            if timestamp > time:
                raise ValueError("Time given is out of range")
            for row in rowreader:
                timestamp = datetime.strptime(row['Timestamp'], mask)
                if timestamp > time:
                    return float(row['Temperature'])
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

    def simulate_route(self, routeCSVFile):
        pass


class VanSimulator:
    """Van Simulator Class"""
    def __init__(self):
        self.start_coordinates = [51.762244, -0.243851]
        self.end_coordinates = [51.503358, -0.127659]
        self.start_time = datetime(2016, 8, 18, 10, 0)
        self.trip_duration = 300
        self.step_time = 5

        self.current_time = self.start_time
        self.current_coordinates = self.start_coordinates

        self.lon_distance = self.end_coordinates[0] - self.start_coordinates[0]
        self.lat_distance = self.end_coordinates[1] - self.start_coordinates[1]

    def go(self):
        while (self.current_time < self.start_time + timedelta(minutes=self.trip_duration)):
            self.step()

    def step(self):
        self.current_time += timedelta(minutes=self.step_time)
        self.current_coordinates[0] += (self.lon_distance / (self.trip_duration/self.step_time))
        self.current_coordinates[1] += (self.lat_distance / (self.trip_duration/self.step_time))

    def get_position(self):
        return self.current_coordinates

    def get_weather(self):
        sensor = SensorSimulator()
        return sensor.weather_at(self.current_time, self.current_coordinates)
