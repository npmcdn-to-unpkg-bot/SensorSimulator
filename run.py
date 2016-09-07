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

with open(args.route) as route:
    van = VanSimulator(route, args.t, args.speed, args.d)

    van.start()
