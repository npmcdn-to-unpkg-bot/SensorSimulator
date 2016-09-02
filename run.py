from SensorSimulator.simulator import VanSimulator
import os
import csv
from Crypto.Cipher import AES
import requests
import json
from datetime import datetime

cipher = AES.new("VLbWHdtrdHzNKfqj8Xt5nTQ4", AES.MODE_ECB)

with open('path.csv') as route:
    van = VanSimulator(route)

    van.start()

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
                reading["Location"][0],
                reading["Location"][1],
                str(reading["Time"]),
                reading["Weather"]["Temperature"],
                reading["Weather"]["Humidity"],
                reading["Weather"]["Pressure"]
            ])

            body = json.dumps({
                "deviceId":"fake1",
                "eventTime": (datetime.strptime(reading["Time"], "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds(),
                "temp": reading["Weather"]["Temperature"],
                "hum": reading["Weather"]["Humidity"],
                "pres": reading["Weather"]["Pressure"]/10,
                "bat": 10,
                "long": reading["Location"][0],
                "lat": reading["Location"][1]
            })

            padding = (16 - len(body)%16) * "0"

            encrypted_body = cipher.encrypt(body + padding).encode("hex")

            r = requests.post(
                "http://sensorendpoint.azurewebsites.net/api/HttpTriggerNodeJS2?code=2hih8t6l2t6zjxsfng1hccwqz7xtt6b7r",
                data=encrypted_body
            )
