from SensorSimulator.simulator import VanSimulator
import os
from datetime import datetime

cipher = AES.new("VLbWHdtrdHzNKfqj8Xt5nTQ4", AES.MODE_ECB)

with open('path.csv') as route:
    van = VanSimulator(route)

    van.start()
