![Qwiic SGP40 Python Package](docs/images/sgp40-gh-banner-py.PNG "qwiic SGP40 Python Package" )

# SparkFun Qwiic SGP40 - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_sgp40)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_sgp40_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_sgp40_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html)

The SparkFun Qwiic SGP40 Air Quality Sensor Breakout Boards provide a simple and cost effective solution for adding air quality sensing to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic SGP40. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the SGP40 via a single Qwiic cable. This includes reading the volatile organic compound (VOC) index, perform a self-test, and more. The capabilities of the SGP40 are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Air Quality Sensor - SGP40](https://www.sparkfun.com/sparkfun-air-quality-sensor-sgp40-qwiic.html)

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
path/to/venv/bin/pip3 install sparkfun-qwiic-sgp40
```
Now you should be able to run any example or custom python scripts that have `import qwiic_sgp40` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_sgp40_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_sgp40_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_sgp40
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators (i.e. "/" vs. "\"). See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)
```sh
circup example qwiic_sgp40\qwiic_sgp40_ex1_basic_readings
circup example qwiic_sgp40\qwiic_sgp40_ex2_function_test
```

Example Use
 ---------------
Below is a quickstart program to print Volatile Organic Compound (VOC) Index read from the SGP40.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_sgp40_py/blob/main/examples/README.md) for a summary of the available examples.

```python
def run_example():

	print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Example 1\n")
	my_sgp40 = qwiic_sgp40.QwiicSGP40()
	
	if my_sgp40.begin() != 0:
		print("\nThe Qwiic SGP40 isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	
	print("\nSGP40 ready!")
	
	while True:
		
		print("\nVOC Index is: " + str(my_sgp40.get_VOC_index()))
		
		time.sleep(1)
```

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
