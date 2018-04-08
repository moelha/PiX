



# Pi<img src="https://upload.wikimedia.org/wikipedia/commons/3/36/SpaceX-Logo-Xonly.svg" alt="alt text" width="50" height="60"> 
Rocket flight recorder based on Raspberry Pi Zero W v1.3)

<table border="0">
  <tr>
    <td><img src="/PiX_front.jpg" alt="Front"></td>
    <td><img src="/PiX_back.jpg" alt="Back"></td>
  </tr>

</table>



 
 ---
 
 ## Table of Contents
- [Getting started](#getting-started)
- [Electronic components](#electronic-components)
- [Model rocket](#model-rocket)
- [Getting started](#getting-started)
  - [Raspbian Jessie Lite](#raspbian-jessie-lite)
  - [Python](#python)
  - [Mosquitto](#mosquitto)
  - [RPi Cam Interface](#rpi-cam-interface)
  - [Node-RED](#node-red) 
 ---

 ## Electronic components 

| Component             |        Description       |     Source      |                          Price                            |
| -------------         |:-------------:           |:-----:          | -----:                                                    |
| Raspberry Pi Zero W   | Version 1.3              |[Pimoroni](https://shop.pimoroni.com/products/raspberry-pi-zero)|       £4.58            |
| MicroSD Card   | 64GB              |[Amazon](https://www.amazon.co.uk/SanDisk-microSDXC-Memory-Adapter-Performance/dp/B073JYVKNX/ref=sr_1_2)|       £17.49            |
| Camera   | Camera for Raspberry Pi Zero   |[Pimoroni](https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module)|       £14            |
| LiPo SHIM             | Enables the RPi to be power supplied from a battery |[Pimoroni](https://shop.pimoroni.com/products/lipo-shim)| £10 |
| LiPo Battery          | 150mAh                   |[Pimoroni](https://shop.pimoroni.com/products/lipo-battery-pack) |    £5                  |
| BMP280                | Pressure, temperature and humidity sensor|[Pimoroni](https://shop.pimoroni.com/products/adafruit-bmp280-i2c-or-spi-barometric-pressure-altitude-sensor)|    £10.50       |
| MPU6050         | Accelerometer and Gyroscope     |[Sparkfun](https://www.sparkfun.com/products/11028)  |   £21.26       |

## Model rocket:

| Component             |        Description       |     Source      |                          Price                            |
| -------------         |:-------------:           |:-----:          | -----:                                                    |
| SpaceX Falcon 9   | Model rocket              |[SpaceX](https://shop.spacex.com/accessories/f9-flying-model-rocket-kit.html)|       £20.59            |

<img src="/image_from_rocket.jpg" alt="Shot from model rocket">

## Getting started
Let's get started! First thing first, solder the MPU6050, BME280 and the LiPo SHIM for the best results. Other means of connection, such as jumper wires or connectors are discouraged as they might disconnect during takeoff. 

Now, we are also going to need a few tools, so downloading them now is a good idea.

- [Etcher](https://etcher.io/) - SD Card flasher
- [Advanced IP Scanner](https://www.advanced-ip-scanner.com) - IP Scanner
- [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) - SSH client


### Raspbian Jessie Lite

Download and flash [Raspbian Jessie Lite](http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2017-07-05/2017-07-05-raspbian-jessie-lite.zip) on a micro SD card (preferably a 64GB one) with [Etcher](https://etcher.io/), or an alternative flasher. We will be using the lite version of Raspbian since we will not need a video output or many of the software packages that come with the Desktop version. 

After flashing the OS on the SD card, we need to enable the SSH server and connect it to a Wireless Access Point in order to communicate with it. Open the micro SD card directory from your File Explorer and create an empty file called ***ssh***. 
Create another file called ***wpa_supplicant.conf*** with the following text:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="YOUR_SSID"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```
Where *YOUR_SSID* and *YOUR_PASSWORD* are the SSID and Password of your WiFi router.

This is what your /boot directory should look like now
<img src="/ssh_wpa.jpg" alt="Boot directory">

The Raspberry Pi Zero W on boot will read these two files and automatically enable the SSH server and connect it to your WiFi router.

Now eject the micro SD card, put it in the Raspberry and power it on with a micro USB cable.

Now your Pi should have connected to your router, and we need to find out its IP address. An easy way to do this is to use [Advanced IP Scanner](https://www.advanced-ip-scanner.com).
<img src="/ip_scanner.jpg" alt="IP scan">

Now that we have found out the IP address, let's SSH into it. We'll use [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) for that.
<img src="/putty.jpg" alt="Putty">

You'll be asked username and password. 
<img src="/login.jpg" alt="Putty login">

The default user name is:
```
pi
```
And the default password is:
```
raspberry
```
Now you should be logged in. It is advised to change these credentials for safety reasons.
<img src="/logged_in.jpg" alt="Putty logged in">

We're all set! Let's move forwards by installing some essentials modules.

**Note that all the following commands will be executed on the Raspberry Pi Zero W through the Putty SSH session.**

---
### Python
Python will be used to read from the sensors and transmit the data to Node-RED via mqtt
```
sudo apt-get install python-2.7 python-pip
```
Now let's install the mqtt library for Python
```
sudo pip install paho-mqtt
```
In order to read from the I2C from Python, we need to install the smbus module
```
sudo apt-get install python-smbus
```
This library is needed so that Python can read from the BMP280 sensor
```
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
```
---
### Mosquitto
Now let's install a MQTT broker, Mosquitto
```
cd ~	
```
```
wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
```
```
sudo apt-key add mosquitto-repo.gpg.key
```
```
cd /etc/apt/sources.list.d/
```
```
sudo wget http://repo.mosquitto.org/debian/mosquitto-jessie.list
```
```
sudo apt-get update
```
```
sudo apt-get install mosquitto mosquitto-clients
```
---
### RPi Cam interface

RPi Cam Web Interface is a web interface for the Raspberry Pi Camera module. It can be used for a wide variety of applications including surveillance, dvr recording and time lapse photography. We will be using it to capture images and live video from the camera. 

Connect the camera with the Raspberry Pi Zero W and proceed with the instructions below.

First, let's clone the RPi Cam Web Interface repository and install it
```
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
```
```
cd RPi_Cam_Web_Interface
```
```
./install.sh
```
---

### Node-RED

Now let's install Node-RED
```
bash <(curl -sL https://raw.githubusercontent.com/node-red/raspbian-deb-package/master/resources/update-nodejs-and-nodered)
```
Install the dashboard module
```
sudo npm install node-red-dashboard
```
Make it autostart on boot
```
sudo systemctl enable nodered.service
```
