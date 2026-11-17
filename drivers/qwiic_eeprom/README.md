Qwiic_EEPROM_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-eeprom/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-eeprom.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_EEPROM_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_EEPROM_Py.svg" /></a>
	<a href="https://qwiic-eeprom-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-eeprom-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_EEPROM_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>

</p>

<img src="https://cdn.sparkfun.com/assets/parts/1/7/7/0/1/18355-SparkFun_Qwiic_EEPROM_Breakout_-_512Kbit-01.jpg"  align="right" width=300 alt="SparkFun Qwiic EEPROM - 512Kbit">

Python module for the [SparkFun Qwiic EEPROM Breakout - 512Kbit](https://www.sparkfun.com/products/18355)

This python package is a port of the existing [SparkFun External EEPROM Arduino Library](https://github.com/sparkfun/SparkFun_External_EEPROM_Arduino_Library)

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
The Qwiic EEPROM Python package currently supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)

Dependencies
--------------
This driver package depends on the qwiic I2C driver:
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic EEPROM module documentation is hosted at [ReadTheDocs](https://qwiic-eeprom-py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-eeprom](https://pypi.org/project/sparkfun-qwiic-eeprom/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-eeprom
```
For the current user:

```sh
pip install sparkfun-qwiic-eeprom
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
pip install sparkfun-qwiic-eeprom-<version>.tar.gz
```

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_eeprom
import time
import sys

def run_example():

    print("\nSparkFun Qwiic EEPROM, Example 1\n")
    my_eeprom = qwiic_eeprom.QwiicEEPROM()

    if my_eeprom.begin() != True:
        print("\nThe Qwiic EEPROM isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nEEPROM ready!")

    print("\nMem size in bytes: " + str(my_eeprom.length()))

    my_value1 = 200 # 0xC8
    my_eeprom.write_byte(300, my_value1)  # (location = 0x12C, data byte)
    my_read1 = my_eeprom.read_byte(300) # (location = 0x12C)
    print("\nI read: " + str(my_read1)) # Should be 0xC8 = 200
    
    my_value2 = -366
    my_eeprom.write_int(10, my_value2)
    my_read2 = my_eeprom.read_int(10)    # (location)
    print("\nI read: " + str(my_read2))

    my_value3 = -7.35
    my_eeprom.write_float(9, my_value3)
    my_read3 = my_eeprom.read_float(9)    # (location)
    # Round to 2-decimal point precision
    my_read3 = round(my_read3, 2)
    print("\nI read: " + str(my_read3))

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
