Qwiic_ADXL313_Py
==================

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-adxl313/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_qwiic_adxl313.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_ADXL313_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_ADXL313_Py.svg" /></a>
	<a href="https://qwiic-adxl313-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-adxl313-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_ADXL313_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/6/2/2/4/17241-SparkFun_3-Axis_Digital_Accelerometer_Breakout_-_ADXL313__Qwiic_02.jpg"  align="right" width=300 alt="SparkFun 3-Axis Digital Accelerometer Breakout - ADXL313 (Qwiic)">

Python module for the [SparkFun 3-Axis Digital Accelerometer Breakout - ADXL313 (Qwiic)](https://www.sparkfun.com/products/17241)

This python package is a port of the existing [SparkFun ADXL313 Arduino Library](https://github.com/sparkfun/SparkFun_ADXL313_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Dependencies 
---------------
This driver package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun qwiic Adxl313 module documentation is hosted at [ReadTheDocs](https://qwiic-adxl313-py.readthedocs.io/en/latest/?)

Installation
-------------

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic-adxl313](https://pypi.org/project/sparkfun-qwiic-adxl313/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-adxl313
```
For the current user:

```sh
pip install sparkfun-qwiic-adxl313
```

### Local Installation
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
pip install sparkfun_qwiic_adxl313-<version>.tar.gz
  
```
Example Use
 ---------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_adxl313
import time
import sys

def runExample():

	print("\nSparkFun Adxl313  Example 1 - Basic Readings\n")
	myAdxl = qwiic_adxl313.QwiicAdxl313()

	if myAdxl.connected == False:
		print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Device connected successfully.")        

	myAdxl.measureModeOn()

	while True:
		if myAdxl.dataReady():
			myAdxl.readAccel() # read all axis from sensor, note this also updates all instance variables
			print(\
			 '{: 06d}'.format(myAdxl.x)\
			, '\t', '{: 06d}'.format(myAdxl.y)\
			, '\t', '{: 06d}'.format(myAdxl.z)\
			)
			time.sleep(0.03)
		else:
			print("Waiting for data")
			time.sleep(0.5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)

```
<p align="center">
<a href="https://www.sparkfun.com" alt="SparkFun">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something"></a>
</p>
