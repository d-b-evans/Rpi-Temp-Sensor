# Stolen and modified from https://thingsboard.io/docs/samples/raspberry/temperature/

import os
import time
import sys
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt      
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'

# Access Token is created/accessed from the 'Devices' section on thingsverse website  
ACCESS_TOKEN = 'dDynH8yqU5uumM2KU94A'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor1_data = {'temperature1': 0, 'humidity1': 0}
sensor2_data = {'temperature2': 0, 'humidity2': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        humidity1,temperature1 = dht.read_retry(dht.DHT11, 14) #14 because the sensor is hooked up to GPIO14 
        humidity1 = round(humidity1, 2)
        temperature1 = round(temperature1, 2)
        print("Temperature1: %-3.1f C" % temperature1)
        print("Humidity1: %-3.1f %%" % humidity1)
        sensor1_data['temperature1'] = temperature1
        sensor1_data['humidity1'] = humidity1

        #humidity2,temperature2 = dht.read_retry(dht.DHT11, 2) #2 because the sensor is hooked up to GPIO2 
        #humidity2 = round(humidity2, 2)
        #temperature2 = round(temperature2, 2)
        #print("Temperature2: %-3.1f C" % temperature2)
        #print("Humidity2: %-3.1f %%" % humidity2)
        #sensor2_data['temperature2'] = temperature2
        #sensor2_data['humidity2'] = humidity2

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor1_data), 1)
        #client.publish('v1/devices/me/telemetry', json.dumps(sensor2_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()