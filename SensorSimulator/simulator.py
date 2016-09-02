from math import sqrt
import csv
from datetime import datetime, timedelta
from stations import PollutionStation, WeatherStation


class SensorSimulator(object):
    """Sensor Simulator Class"""
    def __init__(self):
        self._weather_stations = [
            WeatherStation("heathrow", (51.4775, -0.461389)),
            WeatherStation("luton", (51.874722, -0.368333)),
            WeatherStation("oxford", (51.835882, -1.317293))
        ]

        self._pollution_stations = [
            PollutionStation("westminster", (51.494670, -0.131931))
        ]

    def closest_weather_station(self, coords):
        return min(self._weather_stations, key=lambda x: x.get_distance_from(coords))

    def closest_pollution_station(self, coords):
        return min(self._pollution_stations, key=lambda x: x.get_distance_from(coords))

    def weather_at(self, time, coords):
        weather_station = self.closest_weather_station(coords)
        return weather_station.get_weather(time)

    def pollution_at(self, time, coords):
        pollution_station = self.closest_pollution_station(coords)
        return pollution_station.get_pollution(time)


class VanSimulator(object):
    """Van Simulator Class"""
    def __init__(self, route):
        self.rowreader = csv.DictReader(route, quoting=csv.QUOTE_NONNUMERIC)

        self.timeBetweenReadings = timedelta(minutes=5)

        row = next(self.rowreader)

        self.currentPosition = (row['Longitude'], row['Latitude'])
        self.currentTime = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")
        self.timeToNextReading = self.timeBetweenReadings

        self.readings = []

        self.speed = 0

    def start(self):
        moving = True
        while moving:
            moving = self.move_to_next_weypoint()

    def move_to_next_weypoint(self):
        try:
            row = next(self.rowreader)
        except StopIteration:
            return False

        row["Time"] = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")

        self.speed = self.calculate_speed(row["Time"], row["Longitude"], row["Latitude"])

        while row["Time"] > self.currentTime + self.timeToNextReading:
            self.readings.append(self.take_readings())
            self.move_to_next_reading()

        self.update_time_and_position(row)

        return True

    def update_time_and_position(self, row):
        self.timeToNextReading -= (row["Time"] - self.currentTime)
        self.currentTime = row["Time"]
        self.currentPosition = (row['Longitude'], row['Latitude'])

    def move_to_next_reading(self):
        self.currentTime += self.timeBetweenReadings
        self.currentPosition = (
            self.currentPosition[0] + (self.speed[0] * timedelta_to_minutes(self.timeBetweenReadings)),
            self.currentPosition[1] + (self.speed[1] * timedelta_to_minutes(self.timeBetweenReadings))
        )

    def take_readings(self):
        sensor = SensorSimulator()
        weather = sensor.weather_at(self.currentTime, self.currentPosition)
        pollution = sensor.pollution_at(self.currentTime, self.currentPosition)
        return (self.currentPosition, str(self.currentTime), weather, pollution)

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
