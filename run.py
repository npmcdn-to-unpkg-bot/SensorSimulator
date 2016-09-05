from SensorSimulator.simulator import VanSimulator
import os
import gmplot

with open('path.csv') as route:
    van = VanSimulator(route)

    gmap = gmplot.GoogleMapPlotter(51.503358, -0.127659, 11)

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

        gmap.scatter([reading[0][0]], [reading[0][1]],
                     size=500, color=colour, marker=False, face_alpha=0.7)

    gmap.draw("mymap.html")
