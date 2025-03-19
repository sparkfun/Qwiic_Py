Qwiic_Py
========

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun_qwiic.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Py.svg" /></a>
	<a href="https://qwiic-py.readthedocs.io/en/latest/index.html" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-py/badge/?version=latest&style=flat" /></a>
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

* [Supported Platforms](#supported-platforms)
* [Structure](#structure)
* [Dependent Modules](#dependent-modules)
* [MicroPython and CircuitPython](#micropython-and-circuitpython)
* [Checkout Commands](#checkout-commands)
* [Installation](#installation)
* [Documentation](#documentation)

Supported Platforms
--------------------
The qwiic Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)


Structure
-------------
Each qwiic board has an independent driver library that implements the required logic for the specific board. This driver implementation is structured as a python package that supports standard python package management operations and tools. Additionally, each driver is deployed in a distinct GitHub repository which provides a central area for package management and development.

To provide dynamic discovery and instantiation capabilities, the qwiic package imports all the underlying qwiic driver packages at runtime. As such the qwiic driver packages must be installed prior to using this package. These packages can be installed manually, or the overall package will install them automatically when using a PyPi based package manger (aka pip).

Dependent Modules
------------------
To make development and evaluation easer, the modules this package is dependent on are included in this repository as git submodules. This allows rapid checkout and access to the entire qwiic python ecosystem if needed. 

This structure has the following layout:
```
Qwiic_Py/
   |
   +--- qwiic_i2c/                                   --> Link to the qwiic_i2c submodule repository
   |      |--- __index__.py
   |      `--- ... The cross platform I2C bus access driver 
   |
   +--- qwiic/
   |      |--- __index__.py
   |      +--- ... Package Implementation
   |      `--- drivers/
   |            |--- qwiic_bme280	             --> The qwiic_bme280 submodule
   |            |--- qwiic_micro_oled		     --> The qwiic_micro_oled submodule
   |            `--- ... links to qwiic driver submodule repositories
   |
   +--- README.md
   +--- setup.py
   `--- ...etc

```

Micropython and CircuitPython
------------------
The drivers in the [drivers directory](https://github.com/sparkfun/Qwiic_Py/tree/master/qwiic/drivers) are supported on Linux, MicroPython and CircuitPython. The drivers in the [drivers_linux_only directory](https://github.com/sparkfun/Qwiic_Py/tree/master/qwiic/drivers_linux_only) are currently only supported for Linux. To learn more about MicroPython and CircuitPython, and for install instructions for your specific driver, see the README file of each supported driver.

Dependencies
-------------
The qwiic package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

This package is also dependent on the driver packages contained in the [drivers directory](https://github.com/sparkfun/Qwiic_Py/tree/master/qwiic/drivers).

Documentation
--------------
The SparkFun qwiic package documentation is hosted at [ReadTheDocs](https://qwiic-py.readthedocs.io/en/latest/index.html)


Checkout Commands
------------------
To clone this repository, a standard git clone command will create a local copy of this repository:
```sh
git clone https://github.com/sparkfun/Qwiic_Py
```

This will create a local version of this repository, but the submodule directories (drivers/*, and qwiic_i2c/ ) will be empty. To clone the git repository and include the submodule contents, use the following command:
```sh
git clone --recurse-submodules https://github.com/sparkfun/Qwiic_Py.git 
```

Installation
-------------
### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-qwiic](https://pypi.org/project/sparkfun-qwiic/) package. 

Note - the below instructions outline installation on a Linux-based (Raspberry Pi) system and will install all the drivers in this package. **To install for MicroPython or CircuitPython, see the instructions in each driver's README.** 

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv ~/sparkfun_venv
```

You can pass any path instead of ~/sparkfun_venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
~/sparkfun_venv/bin/pip3 install sparkfun-qwiic
```
Now you should be able to run any example or custom python scripts that have `import qwiic` by running e.g.:
```sh
~/sparkfun_venv/bin/python3 example_script.py
```

This process will install all drivers and modules the qwiic package requires for operation. If you are only working with one driver, it is recommended to download that driver directly (see instructions in each driver's README) rather than from this large meta-package.

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
