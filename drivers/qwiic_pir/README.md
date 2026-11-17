Qwiic_PIR_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-pir/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-pir.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_PIR_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_PIR_Py.svg" /></a>
	<a href="https://qwiic-pir-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-pir-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_PIR_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>

</p>

<img src="https://cdn.sparkfun.com/assets/parts/1/6/4/0/7/17375-SparkFun_Qwiic_PIR_-_1uA__EKMB1107112_-01.jpg"  align="right" width=300 alt="SparkFun Qwiic Button">

Python module for the [SparkFun Qwiic PIR - 1 uA (EKMB1107112)](https://www.sparkfun.com/products/17375) and [SparkFun Qwiic PIR - 170 uA (EKMC4607112K)](https://www.sparkfun.com/products/17374).

This python package is a port of the existing [SparkFun Qwiic PIR Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_PIR_Arduino_Library)

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
The Qwiic Button Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)

Dependencies
--------------
This driver package depends on the qwiic I2C driver:
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic PIR module documentation is hosted at [ReadTheDocs](https://qwiic-pir-py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-pir](https://pypi.org/project/sparkfun-qwiic-pir/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-pir
```
For the current user:

```sh
pip install sparkfun-qwiic-pir
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
pip install sparkfun-qwiic-pir-<version>.tar.gz
```

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_pir
import time
import sys

debounce_time = .20

def run_example():

	print("\nSparkFun Qwiic PIR  Example 1\n")
	my_PIR = qwiic_pir.QwiicPIR()

	if my_PIR.begin() == False:
		print("The Qwiic PIR isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
		
	print ("Waiting 30 seconds for PIR to stabilize")
	for i in range(0, 30):
		print(i)
		time.sleep(1)

	print("Device Stable")

	while True:
		if my_PIR.raw_reading() is True:
			print("Object Detected")
		else:
			print("Object Removed")
		time.sleep(debounce_time)


if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
