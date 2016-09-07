from SensorSimulator.simulator import VanSimulator
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('route',
                    help='Route to be taken')
parser.add_argument('-s', '--speed',
                    help='Speed of the simulation, 1 is real time',
                    type=float, default=1)
parser.add_argument('-t', metavar="MINUTES",
                    help='Time between readings in minutes',
                    type=float, default=5)
parser.add_argument('-d', metavar="DEVICE ID",
                    help='Device ID',
                    type=str, default='fake')

args = parser.parse_args()

<<<<<<< HEAD
    van.start()

    lats = [lat for ((lat, lon), time, weather, pollution) in van.readings]
    lons = [lon for ((lat, lon), time, weather, pollution) in van.readings]

    for reading in van.readings:
        if reading[2] > 27:
            colour = "#800026"
        elif reading[2] > 25:
            colour = "#bd0026"
        elif reading[2] > 23:
            colour = "#e31a1c"
        elif reading[2] > 21:
            colour = "#fc4e2a"
        elif reading[2] > 19:
            colour = "#fd8d3c"
        elif reading[2] > 17:
            colour = "#feb24c"
        elif reading[2] > 15:
            colour = "#fed976"
        elif reading[2] > 13:
            colour = "#ffeda0"
        else:
            colour = "#ffffcc"
=======
with open(args.route) as route:
    van = VanSimulator(route, args.t, args.speed, args.d)
>>>>>>> develop

    van.start()
