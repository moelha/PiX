#!/usr/bin/python

# Import the mpu6050 class
from mpu6050 import mpu6050

# Create a new instance of the mpu6050 class
sensor = mpu6050(0x68)

# Get accelerometer data function
def get_acc():
    return sensor.get_accel_data()

# Get gyroscope data function
def get_gyro():
    return sensor.get_gyro_data()

# Get temperature function
def get_temperature():
    return sensor.get_temp()
