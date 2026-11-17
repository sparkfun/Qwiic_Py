SparkFun![Qwiic Ultrasonic Python Package](docs/images/ultrasonic-gh-banner-py.png "qwiic Ultrasonic Python Package" )

# SparkFun Qwiic Ultrasonic - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_ultrasonic)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_ultrasonic_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_ultrasonic_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_ultrasonic_py/classqwiic__ultrasonic_1_1_qwiic_ultrasonic.html)

The SparkFun Qwiic HC-SR04 Ultrasonic Distance Sensor provides a simple and cost effective solution for adding distance measurements (from 2cm to 400cm) to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic Ultrasonic. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_ultrasonic_py/classqwiic__ultrasonic_1_1_qwiic_ultrasonic.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the Ultrasonic Distance Sensor HC-SR04 via a single Qwiic cable. This includes reading distance and setting the I2C address of the device. The capabilities of the Ultrasonic Distance Sensor are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Qwiic Ultrasonic Distance Sensor - HC-SR04](https://www.sparkfun.com/sparkfun-qwiic-ultrasonic-distance-sensor-hc-sr04.html)

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

Note - the below instructions outline installation an Linux-based (Raspberry Pi) system.

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv path/to/venv
```
You can pass any path as path/to/venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
path/to/venv/bin/pip3 install sparkfun-qwiic-ultrasonic
```
Now you should be able to run any example or custom python scripts that have `import qwiic_ultrasonic` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_ultrasonic_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_ultrasonic_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_ultrasonic
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators (i.e. "/" vs. "\"). See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)
```sh
circup example qwiic_ultrasonic\qwiic_ultrasonic_ex1_basic_readings
circup example qwiic_ultrasonic\qwiic_ultrasonic_ex2_change_address.py
```

Example Use
 ---------------
Below is a quickstart program to print distance measurements (in mm) every tenth of a second.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_ultrasonic_py/blob/master/examples/README.md) for a summary of the available examples.

```python
import qwiic_ultrasonic
import sys
import time

# Here we set the device address. Note that an older version of the Qwiic
# Ultrasonic firmware used a default address of 0x00. If yours uses 0x00,
# you'll need to change the address below. It is also recommended to run
# Example 2 to change the address to the new default.
deviceAddress = qwiic_ultrasonic.QwiicUltrasonic.kDefaultAddress
# deviceAddress = 0x00

def runExample():
	print("\nQwiic Ultrasonic Example 1 - Basic Readings\n")

	# Create instance of device
	my_ultrasonic = qwiic_ultrasonic.QwiicUltrasonic(address=deviceAddress)

	# Check if it's connected
	if my_ultrasonic.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_ultrasonic.begin()

	# Loop forever
	while True:
		# Get measurement from sensor. Note that the measured distance actually
		# comes from the previous trigger, so measurements will be slightly delayed
		distance = my_ultrasonic.trigger_and_read()

		# Print measurement
		print("Distance (mm):", distance)

		# Wait a bit
		time.sleep(0.1)
```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
