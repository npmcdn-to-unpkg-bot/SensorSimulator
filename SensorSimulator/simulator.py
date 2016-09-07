from math import sqrt
import csv
from datetime import datetime, timedelta
from stations import PollutionStation, WeatherStation
from Crypto.Cipher import AES
import time
import requests
import json


class SensorSimulator(object):
    """Sensor Simulator Class"""
    def __init__(self, deviceid, time, coords):
        self.deviceid = deviceid

        self.time = time
        self.coords = coords

        self._weather_stations = [
            WeatherStation("heathrow", (51.4775, -0.461389)),
            WeatherStation("luton", (51.874722, -0.368333)),
            WeatherStation("oxford", (51.835882, -1.317293))
        ]

        self._pollution_stations = [
            PollutionStation("westminster", (51.494670, -0.131931))
        ]

        self.cipher = AES.new("VLbWHdtrdHzNKfqj8Xt5nTQ4", AES.MODE_ECB)

    def closest_weather_station(self):
        return min(self._weather_stations, key=lambda x: x.get_distance_from(self.coords))

    def weather(self):
        weather_station = self.closest_weather_station()
        return weather_station.get_weather(self.time)

    def pollution(self):
        difference = (-0.134518 - self.coords[0], 51.510065 - self.coords[1])
        distance = sqrt(difference[0]**2 + difference[1]**2)
        pollution = 10 * (1 - distance/0.3)
        return {
            "Pollution": pollution
        }

    def send_reading(self):
        weather = self.weather()
        pollution = self.pollution()

        body = json.dumps({
            "deviceId": self.deviceid,
            "eventTime": (self.time - datetime(1970, 1, 1)).total_seconds(),
            "temp": round(weather["Temperature"], 3),
            "hum": round(weather["Humidity"], 3),
            "pres": round(weather["Pressure"]/10, 3),
            "bat": 1,
            "long": self.coords[0],
            "lat": self.coords[1],
            "con": round(pollution["Pollution"], 3)
        })

        print(body)

        padding = (16 - (len(body) % 16)) * "0"

        encrypted_body = self.cipher.encrypt(body + padding).encode("hex")

        r = requests.post(
            "http://sensorendpoint.azurewebsites.net/api/HttpTriggerNodeJS2?code=2hih8t6l2t6zjxsfng1hccwqz7xtt6b7r",
            data=encrypted_body
        )


class VanSimulator(object):
    """Van Simulator Class"""
    def __init__(self, route, timeBetweenReadings, speed, deviceid):
        self.rowreader = csv.DictReader(route)

        self.timeBetweenReadings = timedelta(minutes=timeBetweenReadings)

        row = next(self.rowreader)

        self.currentPosition = (float(row['Longitude']), float(row['Latitude']))
        self.currentTime = datetime.strptime(row['Time'], "%d/%m/%Y %H:%M:%S")
        self.timeToNextReading = self.timeBetweenReadings

        self.speed = 0
        self.simSpeed = speed

        self.deviceid = deviceid

    def start(self):
        moving = True
        while moving:
            moving = self.move_to_next_weypoint()

    def move_to_next_weypoint(self):
        try:
            row = next(self.rowreader)
        except StopIteration:
            return False

        row["Time"] = datetime.strptime(row['Time'], "%d/%m/%Y %H:%M:%S")

        self.speed = self.calculate_speed(row["Time"], float(row["Longitude"]), float(row["Latitude"]))

        while row["Time"] > self.currentTime + self.timeToNextReading:
            self.take_readings()
            self.move_to_next_reading()

        self.update_time_and_position(row)

        return True

    def update_time_and_position(self, row):
        self.timeToNextReading -= (row["Time"] - self.currentTime)
        self.currentTime = row["Time"]
        self.currentPosition = (float(row['Longitude']), float(row['Latitude']))

    def move_to_next_reading(self):
        time.sleep(self.timeBetweenReadings.total_seconds()/self.simSpeed)
        self.currentTime += self.timeBetweenReadings
        self.currentPosition = (
            self.currentPosition[0] + (self.speed[0] * timedelta_to_minutes(self.timeBetweenReadings)),
            self.currentPosition[1] + (self.speed[1] * timedelta_to_minutes(self.timeBetweenReadings))
        )

    def take_readings(self):
        sensor = SensorSimulator(self.deviceid, self.currentTime, self.currentPosition)
        sensor.send_reading()

    def calculate_speed(self, end_time, end_lon, end_lat):
        time_difference = end_time - self.currentTime
        lon_difference = end_lon - self.currentPosition[0]
        lat_difference = end_lat - self.currentPosition[1]

        if timedelta_to_minutes(time_difference) == 0:
            return [0,0]

        return [
            lon_difference/timedelta_to_minutes(time_difference),
            lat_difference/timedelta_to_minutes(time_difference)
        ]


def timedelta_to_minutes(td):
    return td.seconds//60
