import math
import csv
from datetime import datetime

class sensor_simulator:
	def __init__(self):
		self._locations = {
			"heathrow": (51.4775, -0.461389),
			"luton": (51.874722, -0.368333),
			"oxford": (51.835882, -1.317293)
		}

	def closest_airport(self, coordinate):
		return min(self._locations, key=lambda k: self.distance(coordinate , self._locations[k]))

	def distance(self, p1, p2):
		difference = (p1[0] - p2[0], p1[1] - p2[1])
		return math.sqrt(difference[0]**2 + difference[1]**2)

	def temp_at_airport(self, time, airport):
		with open('weather_data/' + airport+'.csv') as csvfile:
			rowreader = csv.DictReader(csvfile)
			for row in rowreader:
				timestamp = datetime.strptime(row['Timestamp'], "%Y-%m-%d %H:%M:%S")
				if timestamp > time:
					return row['Temperature']
			raise ValueError("Time given is out of range")

	def temp_at_coords(self, time, coords):
		airport = self.closest_airport(coords)
		return self.temp_at_airport(time, airport)