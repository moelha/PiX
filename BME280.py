#!/usr/bin/python

# Import the Adafruit_BME280
from Adafruit_BME280 import *

# Create a new instance of the BME280 class
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

# Get temperature function
def get_temperature():
    return sensor.read_temperature()

# Get pressure function
def get_pressure():
    return sensor.read_pressure()

# Get temperature function
def get_humidity():
    return sensor.read_humidity()
    