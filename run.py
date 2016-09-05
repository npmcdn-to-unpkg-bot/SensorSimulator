from SensorSimulator.simulator import VanSimulator
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-s', '--speed',
                    help='Speed of the simulation, 1 is real time',
                    type=float, default=1)

args = parser.parse_args()

with open('path.csv') as route:
    van = VanSimulator(route, 5, args.speed)

    van.start()
