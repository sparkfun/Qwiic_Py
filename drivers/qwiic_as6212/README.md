Qwiic_AS6212_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-as6212/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-as6212.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_AS6212_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_AS6212_Py.svg" /></a>
	<a href="https://qwiic-as6212-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-as6212-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_AS6212_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>

</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/7/9/7/0/18521-SparkFun_Digital_Temperature_Sensor_Breakout_-_AS6212__Qwiic_-01.jpg"  align="right" width=300 alt="SparkFun Digital Temperature Sensor Breakout - AS6212 (Qwiic)">

Python module for the [SparkFun Digital Temperature Sensor Breakout - AS6212 (Qwiic)](https://www.sparkfun.com/products/18521)

This python package is a port of the existing [SparkFun AS6212 Qwiic Arduino Library](https://github.com/sparkfun/SparkFun_AS6212_Qwiic_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
This Python package currently supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)

Dependencies
--------------
This driver package depends on the qwiic I2C driver:
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
This module documentation is hosted at [ReadTheDocs](https://qwiic-as6212-py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-as6212](https://pypi.org/project/sparkfun-qwiic-as6212/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-as6212
```
For the current user:

```sh
pip install sparkfun-qwiic-as6212
```

### Local Installation

To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

### Rebuild Package

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun-qwiic-as6212-<version>.tar.gz
```

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_as6212
import time
import sys

def runExample():

	print("\nSparkFun Qwiic AS6212 Sensor Example 1\n")
	myTempSensor = qwiic_as6212.QwiicAs6212Sensor()

	if myTempSensor.is_connected == False:
		print("The Qwiic AS6212 Sensor device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myTempSensor.begin()
	time.sleep(1)

	print("Initialized.")

	# Initialize configuration settings
	# These settings are saved in the sensor, even if it loses power
  
	# set the number of consecutive faults before triggering alarm.
	# valid options: 1,2,3 or 4
	myTempSensor.set_consecutive_faults(1)
  
	# set the polarity of the Alert. (0:Active LOW, 1:Active HIGH).
	myTempSensor.set_alert_polarity(myTempSensor.AS6212_ALERT_ACTIVE_LOW)
  
	# set the sensor in Comparator Mode (0) or Interrupt Mode (1).
	myTempSensor.set_interrupt_mode(myTempSensor.AS6212_MODE_COMPARATOR)
  
	# set the Conversion Cycle Time (how quickly the sensor gets a new reading)
	myTempSensor.set_conversion_cycletime(myTempSensor.AS6212_CONVERSION_CYCLE_TIME_250MS)

	# set T_HIGH, the upper limit to trigger the alert on
	myTempSensor.set_high_temp_f(78.0)  # set T_HIGH in F
	# myTempSensor.set_high_temp_c(25.56) # set T_HIGH in C
  
	# set T_LOW, the lower limit to shut turn off the alert
	myTempSensor.set_low_temp_f(75.0)	# set T_LOW in F
	# myTempSensor.set_low_temp_c(23.89)	# set T_LOW in C

	print("TLOW F: ", myTempSensor.read_low_temp_f())
	print("THIGH F: ", myTempSensor.read_high_temp_f())
		
	while True:
		myTempSensor.set_sleep_mode(0) # turn sleep  mode off (0)
		time.sleep(0.250) # allow time to wake up and complete first conversion
		
		temperature = myTempSensor.read_temp_f()
		
		# Check for alert
		alertRegisterState = myTempSensor.get_alert_status()		# read the Alert from register
		
		# Place sensor in sleep mode to save power.
		# Current consumption typically ~0.1uA.
		myTempSensor.set_sleep_mode(1) # turn sleep  mode on (1)
		
		print("Temperature: ", temperature, "\tAlert Register: ", alertRegisterState)
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>

