from SensorSimulator.simulator import VanSimulator
import os
import csv

with open('path.csv') as route:
    van = VanSimulator(route)

    van.start()

    lats = [lat for ((lat, lon), time, weather, pollution) in van.readings]
    lons = [lon for ((lat, lon), time, weather, pollution) in van.readings]

    with open('map/data.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([
            "Latitude",
            "Longitude",
            "Time",
            "Temperature",
            "Humidity",
            "Pressure"
        ])
        for reading in van.readings:

            csvwriter.writerow([
                reading[0][0],
                reading[0][1],
                str(reading[1]),
                reading[2][0],
                reading[2][1],
                reading[2][2]
            ])
