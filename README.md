# Qwiic_Py

<p align="center" valign="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>

An overall Python package to provide a single entry point for the [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

<p align="center" valign="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-products-hooked-up.jpg"  width=600>  
  
</p>

The SparkFun qwiic python package aggregates all python qwiic drivers/modules to provide a single entity for qwiic within a python environment. The qwiic package delivers the high-level functionality needed to dynamically discover connected qwiic devices and construct their associated driver object.

## Contents
* [Structure]()
* [Dependent Modules]()
* [Checkout Commands]()
* [Installation]()
* [Example Use]()

## Structure
Each qwiic board has an independent driver library that implements the required logic for the specific board. This driver implementation is structured as a python package that supports standard python package management operations and tools. Additionally, each driver is deployed in a distinct GitHub repository which provides a central area for package management and development.

To provide dynamic discovery and instantiation capabilities, the qwiic package imports all the underlying qwiic driver packages at runtime. As such the qwiic driver packages must be installed prior to using this package. These packages can be installed manually, or the overall package will install them automatically when using a PyPi based package manger (aka pip).

### Dependent Modules
To make development and evaluation easer, the modules this package is dependent on are including in this repository as git submodules. This allows rapid checkout and access to the entire qwiic python ecosystem if needed. 

This structure has the following layout:
```
Qwiic_Py/
	Drivers/
		- Qwiic Board Driver Submodules
	qwiic_i2c/ 
		- The cross platform I2C bus access driver. 
	qwiic/
		- Package Implementation

```

#### Dependencies
The qwiic package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

This package is also dependent on the driver packages contained in the [drivers directory](https://github.com/sparkfun/Qwiic_Py/tree/master/drivers).

## Checkout Commands
To clone this repository, a standard git clone command will create a local copy of this repository:
```
	git clone https://github.com/sparkfun/Qwiic_Py
```

This will create a local version of this repository, but the submodule directories (drivers/*, and qwiic_i2c/ ) will be empty. To clone the git repository and include the submodule contents, use the following command:
```
	git clone --recurse-submodules https://github.com:sparkfun/Qwiic_Py.git 
```
## Installation
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

## Example Use
```python
#TBD
```

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
