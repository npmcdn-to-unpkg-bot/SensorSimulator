from SensorSimulator.simulator import VanSimulator
import os
import gmplot

with open('path.csv') as route:
    van = VanSimulator(route)

    gmap = gmplot.GoogleMapPlotter(51.503358, -0.127659, 11)

    van.start()
    lats = [lat for ((lat, lon), time, temp, pollution) in van.readings]
    lons = [lon for ((lat, lon), time, temp, pollution) in van.readings]

    for reading in van.readings:
        if reading[2] > 24:
            colour = "#ff0000"
        elif reading[2] > 21:
            colour = "#00ff00"
        elif reading[2] > 18:
            colour = "#000000"
        elif reading[2] > 15:
            colour = "#0000ff"
        else:
            colour = "#ffffff"


        gmap.scatter([reading[0][0]], [reading[0][1]], size=500, color=colour, marker=False)

    gmap.draw("mymap.html")
