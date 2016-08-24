import math
import csv
from datetime import datetime, timedelta

class Station:
    def __init__(self, name, coordinates):
        self._name = name
        self._coords = coordinates

    def get_distance_from(self, coords):
        difference = (coords[0] - self._coords[0], coords[1] - self._coords[1])
        return math.sqrt(difference[0]**2 + difference[1]**2)

    def get_distance_from(self, coords):
        difference = (coords[0] - self._coords[0], coords[1] - self._coords[1])
        return math.sqrt(difference[0]**2 + difference[1]**2)

    def __str__(self):
        return self._name


class WeatherStation(Station):
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


class SensorSimulator:
    """Sensor Simulator Class"""
    def __init__(self):
        self._weather_stations = [
            WeatherStation("heathrow", (51.4775, -0.461389)),
            WeatherStation("luton", (51.874722, -0.368333)),
            WeatherStation("oxford", (51.835882, -1.317293))
        ]

    def closest_weather_station(self, coords):
        return min(self._weather_stations, key=lambda x: x.get_distance_from(coords))

    def weather_at(self, time, coords):
        weather_station = self.closest_weather_station(coords)
        return weather_station.get_weather(time)


class VanSimulator:
    """Van Simulator Class"""
    def __init__(self, routeFile):
        self.rowreader = csv.DictReader(routeFile, quoting=csv.QUOTE_NONNUMERIC)

        self.timeBetweenReadings = timedelta(minutes=5)

        row = next(self.rowreader)

        self.currentPosition = (row['Longitude'], row['Latitude'])
        self.currentTime = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")
        self.timeToNextReading = self.timeBetweenReadings

        self.speed = 0

    def start(self):
        moving = True
        while moving:
            try:
                self.move_to_next_route_marker()
            except StopIteration:
                moving = False

    def move_to_next_route_marker(self):
        row = next(self.rowreader)
        row["Time"] = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")

        self.speed = self.calculate_speed(row["Time"], row["Longitude"], row["Latitude"])

        while row["Time"] > self.currentTime + (self.timeToNextReading):
            self.move_to_next_reading()

        self.timeToNextReading -= (row["Time"] - self.currentTime)
        self.currentTime = row["Time"]
        self.currentPosition = (row['Longitude'], row['Latitude'])

    def move_to_next_reading(self):
        self.currentTime += self.timeBetweenReadings
        self.currentPosition = (
            self.currentPosition[0] + (self.speed[0] * timedelta_to_minutes(self.timeBetweenReadings)),
            self.currentPosition[1] + (self.speed[1] * timedelta_to_minutes(self.timeBetweenReadings))
        )

    def get_weather(self):
        sensor = SensorSimulator()
        return sensor.weather_at(self.currentTime, self.currentPosition)

    def calculate_speed(self, end_time, end_lon, end_lat):
        time_difference = end_time - self.currentTime
        lon_difference = end_lon - self.currentPosition[0]
        lat_difference = end_lat - self.currentPosition[1]

        return [
            lon_difference/timedelta_to_minutes(time_difference),
            lat_difference/timedelta_to_minutes(time_difference)
        ]


def timedelta_to_minutes(td):
    return td.seconds//60
