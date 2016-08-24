import unittest
from datetime import datetime
from SensorSimulator.simulator import SensorSimulator, WeatherStation, VanSimulator


class SensorSimulatorMethods(unittest.TestCase):
    def setUp(self):
        self.sim = SensorSimulator()

    def test_closest_airport(self):
        hatfield = (51.762244, -0.243851)
        self.assertEqual(str(self.sim.closest_weather_station(hatfield)), "luton")

    def test_weather_at_coords(self):
        testTimeA = datetime(2016, 8, 18, 14, 10, 00)
        hatfield = (51.762244, -0.243851)
        temperatureA = self.sim.weather_at(testTimeA, hatfield)
        self.assertIsInstance(temperatureA, (float, int))

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
        weather = self.van.get_weather()
        self.assertIsInstance(weather, (float, int))


class WeatherStationMethods(unittest.TestCase):
    def setUp(self):
        self.weather_station = WeatherStation("Test", (51.501225, -0.141821))

    def test_get_distance(self):
        hatfield = (51.762244, -0.243851)
        distance = self.weather_station.get_distance_from(hatfield)
        self.assertIsInstance(distance, (float, int))


if __name__ == '__main__':
    unittest.main()
