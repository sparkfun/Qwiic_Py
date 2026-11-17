![Qwiic VL53L1X - Python Package](docs/images/gh-banner.png "qwiic VL53L1X Python Package")

# SparkFun Qwiic VL53L1X - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_vl53l1x)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_vl53l1x_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_vl53l1x_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html)

The SparkFun Qwiic ToF Distance Sensor VL53L1X Module provides a simple and cost effective solution for adding ToF Distance Sensor capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic VL53L1X. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_vl53l1x_py/classqwiic__vl53l1x_1_1_qwiic_v_l53_l1_x.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the VL53L1X via a single Qwiic cable. This includes reading distance, setting distance mode, seting intermeasurement period and more. The capabilities of the VL53L1X are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun ToF Distance Sensor Sensor - VL53L1X](https://www.sparkfun.com/products/14722)

### Supported Platforms

| Python | Platform | Boards |
|--|--|--|
| Python | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html) , [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi - RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)
|CircuitPython | Raspberry Pi - RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)

> [!NOTE]
> The listed supported platforms and boards are the primary platform targets tested. It is fully expected that this package will work across a wide variety of Python enabled systems. 

## Installation 

The first step to using this package is installing it on your system. The install method depends on the python platform. The following sections outline installation on Python, MicroPython and CircuitPython.

### Python 

#### PyPi Installation

The package is primarily installed using the `pip3` command, downloading the package from the Python Index - "PyPi". 

Note - the below instructions outline installation on a Linux-based (Raspberry Pi) system.

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv path/to/venv
```
You can pass any path as path/to/venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
path/to/venv/bin/pip3 install sparkfun-qwiic-vl53l1x
```
Now you should be able to run any example or custom python scripts that have `import qwiic_vl53l1x` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_vl53l1x_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install github:sparkfun/qwiic_vl53l1x_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_vl53l1x
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_vl53l1x\Example1_ReadDistance
circup example qwiic_vl53l1x\Example2_SetDistanceMode
circup example qwiic_vl53l1x\Example3_StatusandRate
circup example qwiic_vl53l1x\Example4_SetIntermeasurementPeriod
```

Example Use
 ---------------
Below is a quickstart program to print readings from the VL53L1X.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_vl53l1x_py/blob/master/examples/README.md) for a summary of the available examples.

```python

	Reading distance from the laser based VL53L1X

	This example prints the distance to an object. If you are getting weird
	readings, be sure the vacuum tape has been removed from the sensor.

import qwiic_vl53l1x
import time

print("VL53L1X Qwiic Test\n")
ToF = qwiic_vl53l1x.QwiicVL53L1X()
if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor online!\n")

while True:
	try:
		ToF.start_ranging()						 # Write configuration bytes to initiate measurement
		time.sleep(.005)
		distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
		time.sleep(.005)
		ToF.stop_ranging()

		distanceInches = distance / 25.4
		distanceFeet = distanceInches / 12.0

		print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))

	except Exception as e:
		print(e)

```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
