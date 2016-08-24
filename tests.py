import unittest
from datetime import datetime
from simulator import SensorSimulator, Airport, VanSimulator


class SensorSimulatorMethods(unittest.TestCase):
    def setUp(self):
        self.sim = SensorSimulator()

    def test_closest_airport(self):
        hatfield = (51.762244, -0.243851)
        self.assertEqual(str(self.sim.closest_airport(hatfield)), "luton")

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
        self.van = VanSimulator()

    def test_get_position(self):
        latitude, longitude = self.van.get_position()
        self.assertIsInstance(latitude, float)
        self.assertIsInstance(longitude, float)

    def test_get_weather(self):
        weather = self.van.get_weather()
        self.assertIsInstance(weather, (float, int))

    def test_take_journey(self):
        self.van.go()
        end_target = self.van.end_coordinates
        end_true = [round(coord, 7) for coord in self.van.current_coordinates]
        self.assertEqual(end_true, end_target)


class AirportMethods(unittest.TestCase):
    def setUp(self):
        self.airport = Airport("Test", (51.501225, -0.141821))

    def test_get_distance(self):
        hatfield = (51.762244, -0.243851)
        distance = self.airport.get_distance_from(hatfield)
        self.assertIsInstance(distance, (float, int))


if __name__ == '__main__':
    unittest.main()
