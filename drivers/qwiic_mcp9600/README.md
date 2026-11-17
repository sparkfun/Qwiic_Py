![Qwiic MCP9600 - Python Package](docs/images/gh-banner.png "qwiic MCP9600 Python Package")

# SparkFun Qwiic MCP9600 - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_mcp9600)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_mcp9600_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_mcp9600_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_mcp9600_py/classqwiic__mcp9600_1_1_qwiic_m_c_p9600.html)

The SparkFun Qwiic Thermocouple Amplifier MCP9600 Module provides a simple and cost effective solution for adding Thermocouple Amplifier capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic MCP9600. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_mcp9600_py/classqwiic__mcp9600_1_1_qwiic_m_c_p9600.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the MCP9600 via a single Qwiic cable. This includes reading thermocouple temperature, reading ambient temperature, setting filtering and more. The capabilities of the MCP9600 are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Thermocouple Amplifier Sensor - MCP9600](https://www.sparkfun.com/products/16295)

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
path/to/venv/bin/pip3 install sparkfun-qwiic-mcp9600
```
Now you should be able to run any example or custom python scripts that have `import qwiic_mcp9600` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_mcp9600_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_mcp9600_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_mcp9600
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_mcp9600\qwiic_mcp9600_ex1_basic
circup example qwiic_mcp9600\qwiic_mcp9600_ex2_set_type
circup example qwiic_mcp9600\qwiic_mcp9600_ex3_set_filter
circup example qwiic_mcp9600\qwiic_mcp9600_ex4_set_resolution
circup example qwiic_mcp9600\qwiic_mcp9600_ex5_burst_mode
circup example qwiic_mcp9600\qwiic_mcp9600_ex6_config_temp_alert

```

Example Use
 ---------------
Below is a quickstart program to print readings from the MCP9600.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_mcp9600_py/blob/master/examples/README.md) for a summary of the available examples.

```python

import qwiic_mcp9600
import sys
import time 

def runExample():

	print("\nQwiic MCP9600 Example 1 - Basic Readings\n")

	myThermo = qwiic_mcp9600.QwiicMCP9600()

	if myThermo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myThermo.begin()

	while True:
		if myThermo.available():
			thermocouple_temp = myThermo.get_thermocouple_temp()
			ambient_temp = myThermo.get_ambient_temp()
			temp_delta = myThermo.get_temp_delta()

			print(f"Thermocouple: {thermocouple_temp}C   Ambient: {ambient_temp}C   Temperature Delta: {temp_delta}C")
			
		time.sleep(0.02)

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
