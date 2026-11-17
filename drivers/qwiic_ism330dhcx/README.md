![Qwiic ISM330DHCX - Python Package](docs/images/gh-banner.png "qwiic ISM330DHCX Python Package")

# SparkFun Qwiic ISM330DHCX - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_ism330dhcx)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_ism330dhcx_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_ism330dhcx_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html)

The SparkFun Qwiic 6DoF IMU ISM330DHCX Module provides a simple and cost effective solution for adding 6DoF IMU capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic ISM330DHCX. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_ism330dhcx_py/classqwiic__ism330dhcx_1_1_qwiic_i_s_m330_d_h_c_x.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the ISM330DHCX via a single Qwiic cable. This includes reading acceleration, reading gyroscope, setting filters, setting data rate and more. The capabilities of the ISM330DHCX are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun 6DoF IMU Sensor - ISM330DHCX](https://www.sparkfun.com/products/19764)

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
path/to/venv/bin/pip3 install sparkfun-qwiic-ism330dhcx
```
Now you should be able to run any example or custom python scripts that have `import qwiic_ism330dhcx` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_ism330dhcx_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install github:sparkfun/qwiic_ism330dhcx_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_ism330dhcx
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_ism330dhcx\qwiic_ism330dhcx_ex1_basic
```

Example Use
 ---------------
Below is a quickstart program to print readings from the ISM330DHCX.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_ism330dhcx_py/blob/master/examples/README.md) for a summary of the available examples.

```python

import qwiic_ism330dhcx
import sys
import time

def runExample():
	print("\nQwiic ISM330DHCX Example 1 - Basic Readings\n")

	myIsm = qwiic_ism330dhcx.QwiicISM330DHCX()

	if myIsm.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myIsm.begin()
	myIsm.device_reset()

	while myIsm.get_device_reset() == False:
		time.sleep(1)

	print("Reset.")
	print("Applying settings.")
	time.sleep(0.100)

	myIsm.set_device_config()
	myIsm.set_block_data_update()

	myIsm.set_accel_data_rate(myIsm.kXlOdr104Hz)
	myIsm.set_accel_full_scale(myIsm.kXlFs4g)

	myIsm.set_gyro_data_rate(myIsm.kGyroOdr104Hz)
	myIsm.set_gyro_full_scale(myIsm.kGyroFs500dps)

	myIsm.set_accel_filter_lp2()
	myIsm.set_accel_slope_filter(myIsm.kLpOdrDiv100)

	myIsm.set_gyro_filter_lp1()
	myIsm.set_gyro_lp1_bandwidth(myIsm.kBwMedium)

	while True:
		if myIsm.check_status():
			accelData = myIsm.get_accel()
			print("Accel X: %f, Y: %f, Z: %f " % (accelData.xData, accelData.yData, accelData.zData), end='')
			gyroData = myIsm.get_gyro()
			print("Gyro X: %f, Y: %f, Z: %f" % (gyroData.xData, gyroData.yData, gyroData.zData))
		
		time.sleep(0.100) # Delay so that we don't spam user console or I2C bus

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
