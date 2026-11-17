Qwiic_Dual_Encoder_Reader_Py
==============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-dual-encoder-reader/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_qwiic_dual_encoder_reader.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Dual_Encoder_Reader_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Dual_Encoder_Reader_Py.svg" /></a>
	<a href="https://qwiic-dual-encoder-reader-py.readthedocs.io/en/latest/" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-dual-encoder-reader-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Dual_Encoder_Reader_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/5/0/3/5/16328-SparkFun_Auto_pHAT_for_Raspberry_Pi-01.jpg"  align="right" width=300 alt="SparkFun Auto pHAT for Raspberry Pi">

Python module for the qwiic dual encoder reader (ATTINY84), which is included on the [SparkFun Auto pHAT for Raspberry Pi](https://www.sparkfun.com/products/16328)

This python package enables the user to take count readings from the on-board ATTINY84 that handles reading the dual motor encoders. The firmware that is used on the ATTiny84 is located in a separate repository here: [SparkFun Dual Encoder Reader Firmware Repository](https://github.com/sparkfun/Qwiic_Dual_Encoder_Reader)

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
The qwiic ICM20948 Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies 
---------------
This driver package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun qwiic Dual Encoder Reader documentation is hosted at [ReadTheDocs](https://qwiic-dual-encoder-reader-py.readthedocs.io/en/latest/)

Installation
-------------

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic-dual-encoder-reader](https://pypi.org/project/sparkfun-qwiic-dual-encoder-reader/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-dual-encoder-reader
```
For the current user:

```sh
pip install sparkfun-qwiic-dual-encoder-reader
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
pip install sparkfun_qwiic_dual_encoder_reader-<version>.tar.gz
  
```
Example Use
 ---------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_dual_encoder_reader
import time
import sys

def runExample():

	print("\nSparkFun Qwiic Dual Encoder Reader   Example 1\n")
	myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

	if myEncoders.connected == False:
		print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myEncoders.begin()

	while True:

		print("Count1: %d, Count2: %s" % (myEncoders.count1, \
			myEncoders.count2, \
			))

		time.sleep(.3)

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
