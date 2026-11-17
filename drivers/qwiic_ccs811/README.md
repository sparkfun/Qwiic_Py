Qwiic_CCS811_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-ccs811/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_qwiic_ccs811.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_CCS811_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_CCS811_Py.svg" /></a>
	<a href="https://qwiic-ccs811-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-ccs811-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_CCS811_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/2/3/2/9/14348-01.jpg"  align="right" width=300 alt="SparkFun qwiic Environmental Combo">


Python module for the qwiic ccs811 sensor, which is part of the [SparkFun Qwiic Environmental Combo Breakout](https://www.sparkfun.com/products/14348)

This python package is a port of the existing [SparkFun CCS811 Arduino Library](https://github.com/sparkfun/SparkFun_CCS811_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### :warning: **Using this sensor on a Raspberry Pi**? :warning:
Your system might need modification. See this [note](#raspberry-pi-use).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
The qwiic CCS811 Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies 
--------------
This driver package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun qwiic CCS811 module documentation is hosted at [ReadTheDocs](https://qwiic-ccs811-py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-ccs811](https://pypi.org/project/sparkfun-qwiic-ccs811/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-ccs811
```
For the current user:

```sh
pip install sparkfun-qwiic-ccs811
```
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun_qwiic_ccs811-<version>.tar.gz
```

Raspberry Pi Use
-------------------
For this sensor to work on the Raspberry Pi, I2C clock stretching must be enabled. 

To do this:
- Login as root to the target Raspberry Pi
- Open the file /boot/config.txt in your favorite editor (vi, nano ...etc)
- Scroll down until the block that contains the following is found:
```ini
dtparam=i2c_arm=on
dtparam=i2s=on
dtparam=spi=on
```
- Add the following line:
```ini
# Enable I2C clock stretching
dtparam=i2c_arm_baudrate=10000
```
- Save the file
- Reboot the raspberry pi

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_ccs811
import time
import sys

def runExample():

	print("\nSparkFun CCS811 Sensor Basic Example \n")
	mySensor = qwiic_ccs811.QwiicCcs811()

	if mySensor.isConnected() == False:
		print("The Qwiic CCS811 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	mySensor.begin()

	while True:

		mySensor.readAlgorithmResults()

		print("CO2:\t%.3f" % mySensor.getCO2())

		print("tVOC:\t%.3f\n" % mySensor.getTVOC())	

		
		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Basic Example")
		sys.exit(0)

```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
