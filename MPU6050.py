#!/usr/bin/python

import smbus
import math
import time
import paho.mqtt.publish as publish
import json

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def send_mqtt_message(dof):
    mqttPath = "sensor/6DOF"
    message = json.dumps(dof)
    host = "127.0.0.1"
    return publish.single(mqttPath, message, hostname=host)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
    #time.sleep(0.1)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0


    #Build Json object with all the identification and sensors data
    jsonObject = {}
    jsonObject["d"] = {}
    jsonObject["d"]["id"] = "MPU6050"
    jsonObject["d"]["accelerometer"] = {}
    jsonObject["d"]["accelerometer"]["x"] = accel_xout / 16384.0
    jsonObject["d"]["accelerometer"]["y"] = accel_yout / 16384.0
    jsonObject["d"]["accelerometer"]["z"] = accel_zout / 16384.0

    jsonObject["d"]["gyroscope"] = {} 
    jsonObject["d"]["gyroscope"]["x"] = gyro_xout / 131
    jsonObject["d"]["gyroscope"]["y"] = gyro_yout / 131
    jsonObject["d"]["gyroscope"]["z"] = gyro_zout / 131


    send_mqtt_message(jsonObject)

    #time.sleep(0.5)


