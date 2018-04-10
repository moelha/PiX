import time
import json
import paho.mqtt.publish as publish
import IMU
import BME280

def send_mqtt_message(sensor_data, mqttPath):
    message = json.dumps(sensor_data)
    host = "127.0.0.1"
    return publish.single(mqttPath, message, hostname=host)

while True:

    #Get temperature, pressure and humidity data
    try:
	temperature = BME280.get_temperature()
    except: 
	temperature = -1

    try:
	pressure = BME280.get_pressure()
    except:
	pressure = -1

    try:
	humidity = BME280.get_humidity()
    except:
	humidity = -1

    #Build Json object with all the identification and sensors data
    BME280_data = {}
    BME280_data["d"] = {}
    BME280_data["d"]["id"] = "BME280"
    BME280_data["d"]["temperature"] = temperature
    BME280_data["d"]["pressure"] = pressure
    BME280_data["d"]["humidity"] = humidity

    # Get accelereomter data
    try:
	accel_data = IMU.get_acc()
    except:
	accel_data = -1

    # Get gyroscope data
    try:
	gyro_data = IMU.get_gyro()
    except:
	gyro_data = -1

    # Parse accelerometer data
    accel_x = accel_data['x']
    accel_y = accel_data['y']
    accel_z = accel_data['z']

    # Parse gyroscope data
    gyro_x = gyro_data['x']
    gyro_y = gyro_data['y']
    gyro_z = gyro_data['z']

    #Build Json object with all the identification and sensors data
    IMU_data = {}
    IMU_data["d"] = {}
    IMU_data["d"]["id"] = "MPU6050"
    IMU_data["d"]["accelerometer"] = {}
    IMU_data["d"]["accelerometer"]["x"] = accel_x
    IMU_data["d"]["accelerometer"]["y"] = accel_y
    IMU_data["d"]["accelerometer"]["z"] = accel_z
    IMU_data["d"]["gyroscope"] = {} 
    IMU_data["d"]["gyroscope"]["x"] = gyro_x
    IMU_data["d"]["gyroscope"]["y"] = gyro_y
    IMU_data["d"]["gyroscope"]["z"] = gyro_z

    # Send data via MQTT
    try:
	send_mqtt_message(BME280_data, "sensor/BME280")
        send_mqtt_message(IMU_data, "sensor/IMU")
    except:
	print("sending data failed")    

    time.sleep(0.1)
