![Qwiic AS7343 - Python Package](docs/images/gh-banner.png "qwiic AS7343 Python Package")

# SparkFun Qwiic AS7343 - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_as7343)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_as7343_py)
![License](https://img.shields.io/github/license/sparkfun/Qwiic_AS7343_Py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_as7343_py/classqwiic__as7343_1_1_qwiic_a_s7343.html)

The SparkFun Qwiic Multi-Spectral Sensor AS7343 Module provides a simple and cost effective solution for adding Multi-Spectral Sensor capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic AS7343. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_as7343_py/classqwiic__as7343_1_1_qwiic_a_s7343.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the AS7343 via a single Qwiic cable. This includes reading RGB, reading NIR, reading multi-channel spectral data and more. The capabilities of the AS7343 are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Multi-Spectral Sensor Sensor - AS7343](https://www.sparkfun.com/sparkfun-spectral-sensor-as7343-qwiic.html)

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
path/to/venv/bin/pip3 install sparkfun-qwiic-as7343
```
Now you should be able to run any example or custom python scripts that have `import qwiic_as7343` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_as7343_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_as7343_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_as7343
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_as7343\qwiic_as7343_ex1_basic_readings
circup example qwiic_as7343\qwiic_as7343_ex2_all_channels
circup example qwiic_as7343\qwiic_as7343_ex3_gain
circup example qwiic_as7343\qwiic_as7343_ex5_flicker_detection
circup example qwiic_as7343\qwiic_as7343_ex6_sleep
```

Example Use
 ---------------
Below is a quickstart program to print readings from the AS7343.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_as7343_py/blob/main/examples/README.md) for a summary of the available examples.

```python

import qwiic_as7343 
import sys
import time

def runExample():
	print("\nQwiic AS7343 Example 1 - Basic Readings\n")

	myAS7343 = qwiic_as7343.QwiicAS7343()

	if myAS7343.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	if not myAS7343.begin():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	
	myAS7343.power_on()
	print("Device powered on")

	if not myAS7343.set_auto_smux(myAS7343.kAutoSmux18Channels):
		print("Failed to set AutoSmux", file=sys.stderr)
		return
	print("AutoSmux set to 18 channels")

	if not myAS7343.spectral_measurement_enable():
		print("Failed to enable spectral measurements", file=sys.stderr)
		return
	print("Spectral measurements enabled")

	while True:
		myAS7343.set_led_drive(0) # 0 = 4mA
		myAS7343.set_led_on()

		time.sleep(0.100) # Wait 100 ms for LED to fully illuminate our target
		
		myAS7343.read_all_spectral_data()

		myAS7343.set_led_off()

		print(myAS7343.get_blue(), end=',')
		print(myAS7343.get_red(), end=',')
		print(myAS7343.get_green(), end=',')
		print(myAS7343.get_nir(), end=',\n')

		time.sleep(0.500) # Wait 500 ms before next reading

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)
```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
