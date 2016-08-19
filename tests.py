import unittest
from datetime import datetime
from simulator import SensorSimulator


class SensorSimulatorMethods(unittest.TestCase):
    def setUp(self):
        self.sim = SensorSimulator()

    def test_closest_airport(self):
        hatfield = (51.762244, -0.243851)
        self.assertEqual(str(self.sim.closest_airport(hatfield)), "luton")

    def test_temp_at_coords(self):
        testTimeA = datetime(2016, 8, 18, 14, 10, 00)
        testTimeB = datetime(2015, 8, 18, 14, 10, 00)
        hatfield = (51.762244, -0.243851)
        temperature = self.sim.temp_at_coords(testTimeA, hatfield)
        self.assertIsInstance(temperature, (float, int))


if __name__ == '__main__':
    unittest.main()
