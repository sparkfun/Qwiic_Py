![Qwiic MAX1704X - Python Package](docs/images/gh-banner.png "qwiic MAX1704X Python Package")

# SparkFun Qwiic MAX1704X - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_max1704x)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_max1704x_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_max1704x_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html)

The SparkFun Qwiic LiPo Fuel Guage MAX1704X Sensor provides a simple and cost effective solution for adding LiPo Fuel Guage sensing to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic MAX1704X. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_max1704x_py/classqwiic__max1704x_1_1_qwiic_m_a_x1704_x.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the MAX1704X via a single Qwiic cable. This includes reading voltage level, reading state of charge, setting threshold alerts,  and more. The capabilities of the MAX1704X are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun LiPo Fuel Guage Sensor - MAX1704X](https://www.sparkfun.com/products/20680)

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
path/to/venv/bin/pip3 install sparkfun-qwiic-max1704x
```
Now you should be able to run any example or custom python scripts that have `import qwiic_max1704x` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_max1704x_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_max1704x_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_max1704x
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_max1704x\qwiic_max1704x_ex1_basic
circup example qwiic_max1704x\qwiic_max1704x_ex4_kitchen_sink

```

Example Use
 ---------------
Below is a quickstart program to print readings from the MAX1704X.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_max1704x_py/blob/master/examples/README.md) for a summary of the available examples.

```python


import qwiic_max1704x
import sys
import time

def runExample():
	print("\nQwiic MAX1704X Example 1 - Simple\n")

	myLipo = qwiic_max1704x.QwiicMAX1704X() # defaults to the MAX17043 device


	if myLipo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLipo.begin()

	myLipo.quick_start()

	myLipo.set_threshold(20)

	while True:
		voltage = myLipo.get_voltage()
		print("Voltage: %.2fV" % voltage)

		soc = myLipo.get_soc()
		print("State of Charge: %.2f%%" % soc)

		if myLipo.get_alert():
			print("Battery SoC is below threshold!")
		else:
			print("Battery SoC is above threshold.")

		time.sleep(0.500)

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
