import math
import csv

class coords:
	def __init__(self, lon, lat):
		self._coords = (lon, lat)

	def __getitem__(self, j):
		return self._coords[j]

	def __setitem__(self, j, val):
		self._coords[j] = val

	def __neg__(self):
		return coords(-self[0], -self[1])

	def __add__(self, other):
		return coords(self[0] + other[0], self[1] + other[1])

	def __sub__(self, other):
		return coords(self[0] - other[0], self[1] - other[1])

	def __mul__(self, other):
		if isinstance(other, (float, int)):
			return coords(other*self[0], other*self[1])
		elif isinstance(other, Vector):
			return coords(other[0]*self[0], other[1]*self[1])
		else:
			raise TypeError

	def __rmul__(self, other):
		if isinstance(other, (float, int)):
			return coords(other*self[0], other*self[1])
		elif isinstance(other, Vector):
			return coords(other[0]*self[0], other[1]*self[1])
		else:
			raise TypeError


	def __eq__(self, other):
		return self_coords == other_coords

	def __ne__(self, other):
		return not self == other

	def __str__(self):
		return '<' + str(self._coords)[1:-1] + '>'


class sensor_simulator:
	def __init__(self):
		self._locations = {
    		"heathrow": coords(51.4775, -0.461389),
    		"luton": coords(51.874722, -0.368333),
    		"oxford": coords(51.835882, -1.317293)
		}

	def closest_airport(self, coordinate):
		return min(self._locations, key=lambda k: self.distance(coordinate , self._locations[k]))

	def distance(self, p1, p2):
		difference = p1 - p2
		return math.sqrt(difference[0]**2 + difference[1]**2)

	def temp_at_aiport(self, time, airport):
		with open(airport+'.csv', 'rb') as csvfile:
			rowreader = csv.reader(csvfile, delimiter=',')
			for row in rowreader:
				print(row['temperature'])


	def temp_at_coords(self, time, coords):
		airport = self.closest_airport(coords)
		return self.temp_at_aiport(time, airport)

hatfield = coords(51.762124, -0.243090)

ss = sensor_simulator()
print(ss.temp_at_coords('now', hatfield))