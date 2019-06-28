Qwiic_Py
========

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://test.pypi.org/project/sparkfun-qwiic/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_qwiic.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Py/issues.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com//assets/parts/1/3/8/7/9/Qwiic_pHAT_Pi-3-B-Plus.jpg"  align="right" width=340> 

The SparkFun qwiic python package aggregates all python qwiic drivers/modules to provide a single entity for qwiic within a python environment. The qwiic package delivers the high-level functionality needed to dynamically discover connected qwiic devices and construct their associated driver object.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents


* [Structure](#structure)
* [Dependent Modules](#dependent-modules)
* [Checkout Commands](#checkout-commands)
* [Installation](#installation)
* [Example Use](#example-use)

Structure
-------------
Each qwiic board has an independent driver library that implements the required logic for the specific board. This driver implementation is structured as a python package that supports standard python package management operations and tools. Additionally, each driver is deployed in a distinct GitHub repository which provides a central area for package management and development.

To provide dynamic discovery and instantiation capabilities, the qwiic package imports all the underlying qwiic driver packages at runtime. As such the qwiic driver packages must be installed prior to using this package. These packages can be installed manually, or the overall package will install them automatically when using a PyPi based package manger (aka pip).

### Dependent Modules
To make development and evaluation easer, the modules this package is dependent on are included in this repository as git submodules. This allows rapid checkout and access to the entire qwiic python ecosystem if needed. 

This structure has the following layout:
```
Qwiic_Py/
   +--- drivers/
   |       |--- qwiic_bme280			--> The qwiic_bme280 submodule
   |       |--- qwiic_micro_oled		--> The qwiic_micro_oled submodule
   |       `--- ... links to qwiic driver submodule repositories
   |
   +--- qwiic_i2c/        --> Link to the qwiic_i2c submodule repository
   |      |--- __index__.py
   |      `--- ... The cross platform I2C bus access driver 
   |
   +--- qwiic/
   |      |--- __index__.py
   |      `--- ... Package Implementation
   |
   +--- README.rd
   +--- setup.py
   `--- ...etc

```

#### Dependencies
The qwiic package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

This package is also dependent on the driver packages contained in the [drivers directory](https://github.com/sparkfun/Qwiic_Py/tree/master/drivers).

Checkout Commands
-----------------
To clone this repository, a standard git clone command will create a local copy of this repository:
```
	git clone https://github.com/sparkfun/Qwiic_Py
```

This will create a local version of this repository, but the submodule directories (drivers/*, and qwiic_i2c/ ) will be empty. To clone the git repository and include the submodule contents, use the following command:
```
	git clone --recurse-submodules https://github.com:sparkfun/Qwiic_Py.git 
```
Installation
-------------
### PyPi Installation
On systems that support PyPi installation via pip, this package is installed using the following commands. 

For all users (note: the user must have sudo privileges):
```
  sudo pip install sparkfun_qwiic
```
For the current user:

```
  pip install sparkfun_qwiic
```

This process will also install all modules the qwiic package requires for operation, including the needed qwiic driver packages.

### Local Installation
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```
  $ python setup.py install
```

To build a package for use with pip:
```
  $ python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```
  cd dist
  pip install sparkfun_qwiic_-<version>.tar.gz
```

Example Use
------------
```python
#TBD
```

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
