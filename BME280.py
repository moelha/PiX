import math
import json
import paho.mqtt.publish as publish
from Adafruit_BME280 import *


def send_mqtt_message(sensor_data):
    mqttPath = "sensor/BME280"
    message = json.dumps(sensor_data)
    host = "127.0.0.1"
    return publish.single(mqttPath, message, hostname=host)

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

while(True):

    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()
    
    jsonObject = {}
    jsonObject["d"] = {}
    jsonObject["d"]["id"] = "BME280"
    jsonObject["d"]["temperature"] = degrees
    jsonObject["d"]["pressure"] = pascals
    jsonObject["d"]["humidity"] = humidity

    send_mqtt_message(jsonObject)

#print 'Temp      = {0:0.3f} deg C'.format(degrees)
#print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
#print 'Humidity  = {0:0.2f} %'.format(humidity)
