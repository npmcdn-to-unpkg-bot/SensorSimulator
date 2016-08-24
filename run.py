from SensorSimulator.simulator import VanSimulator
import os

with open('path.csv') as route:
    van = VanSimulator(route)
