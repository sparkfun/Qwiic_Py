Qwiic_Proximity_Py
===================

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-proximity/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-proximity.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Proximity_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Proximity_Py.svg" /></a>
	<a href="https://qwiic-proximity-py.readthedocs.io/en/latest/index.html" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-proximity-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Proximity_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/3/5/9/2/15177-SparkFun_Proximity_Sensor_Breakout_-_20cm__VCNL4040__Qwiic_-01.jpg"  align="right" width=340>

Python module to interface with the [Qwiic Proximity board](https://www.sparkfun.com/products/15177).

This package is a port of the [SparkFun VCNL4040 Proximity Sensor Arduino Library](https://github.com/sparkfun/SparkFun_VCNL4040_Arduino_Library)

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
The qwiic Proximity Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies 
-------------
This driver package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun qwiic Proximity module documentation is hosted at [ReadTheDocs](https://qwiic-proximity-py.readthedocs.io/en/latest/index.html)

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic-proximity](https://pypi.org/project/sparkfun-qwiic-proximity/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-proximity
```
For the current user:

```sh
pip install sparkfun-qwiic-proximity
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
pip install sparkfun_qwiic_proximity-<version>.tar.gz
```

Example Use
--------------
See the examples directory for more detailed use examples.

```python
import qwiic_proximity
import time
import sys

def runExample():

	print("\nSparkFun Proximity Sensor VCN4040 Example 1\n")
	oProx = qwiic_proximity.QwiicProximity()

	if oProx.isConnected() == False:
		print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	oProx.begin()

	while True:
		proxValue = oProx.getProximity()
		print("Proximity Value: %d" % proxValue)
		time.sleep(.4)
    
runExample()

```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
