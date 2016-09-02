import unittest
from math import sqrt
from datetime import datetime
from SensorSimulator import SensorSimulator, WeatherStation, VanSimulator, PollutionStation


class SensorSimulatorMethods(unittest.TestCase):
    def setUp(self):
        self.sim = SensorSimulator()

    def test_closest_weather_station(self):
        hatfield = (51.762244, -0.243851)
        closestWeatherStation = str(self.sim.closest_weather_station(hatfield))
        self.assertEqual(closestWeatherStation, "luton")

    def test_weather_at_coords(self):
        testTimeA = datetime(2016, 8, 18, 14, 10, 00)
        hatfield = (51.762244, -0.243851)
        temperatureA = self.sim.weather_at(testTimeA, hatfield)
        self.assertIsInstance(temperatureA, tuple)

    def test_weather_at_coords2(self):
        testTimeB = datetime(2015, 8, 18, 14, 10, 00)
        hatfield = (51.762244, -0.243851)
        with self.assertRaises(ValueError):
            temperatureB = self.sim.weather_at(testTimeB, hatfield)


class VanSimulatorMethods(unittest.TestCase):
    def setUp(self):
        self.van = VanSimulator(open('path.csv', 'r'))

    def test_route(self):
        self.van.start()

    def test_get_weather(self):
        readings = self.van.take_readings()
        self.assertIsInstance(readings, tuple)


class WeatherStationMethods(unittest.TestCase):
    def setUp(self):
        self.weather_station = WeatherStation("luton", (51.501225, -0.141821))

    def test_get_distance(self):
        hatfield = (51.762244, -0.243851)
        distance = self.weather_station.get_distance_from(hatfield)
        true_distance = sqrt((hatfield[0] - 51.501225)**2 + (hatfield[1]--0.141821)**2)
        self.assertIsInstance(distance, (float, int))
        self.assertEqual(distance, true_distance)

    def test_get_weather(self):
        time = datetime(2016, 8, 18, 8)
        weather = self.weather_station.get_weather(time)
        self.assertIsInstance(weather, tuple)


class PollutionStationMethods(unittest.TestCase):
    def setUp(self):
        self.pollution_station = PollutionStation("westminster", (51.501225, -0.141821))

    def test_get_distance(self):
        hatfield = (51.762244, -0.243851)
        distance = self.pollution_station.get_distance_from(hatfield)
        self.assertIsInstance(distance, (float, int))

    def test_get_pollution(self):
        time = datetime(2016, 8, 18, 8)
        pollution = self.pollution_station.get_pollution(time)
        self.assertIsInstance(pollution, (float, int))

if __name__ == '__main__':
    unittest.main()
