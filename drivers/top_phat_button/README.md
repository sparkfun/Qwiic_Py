Top_pHAT_Button_Py
==================
<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-top-phat-button/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-top-phat-button.svg" /></a>
	<a href="https://github.com/sparkfun/Top_pHAT_Button_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Top_pHAT_Button_Py.svg" /></a>
	<a href="https://sparkfun-top-phat-button.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/sparkfun-top-phat-button/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Top_pHAT_Button_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>
	
</p>

<img src="https://cdn.sparkfun.com/assets/parts/1/5/0/0/3/16301-SparkFun_Top_pHAT_for_Raspberry_Pi-01.jpg"  align="right" width=300 alt="SparkFun Top pHAT">

Python module for the buttons aboard the [SparkFun Top pHAT](https://www.sparkfun.com/products/16301)

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
The Top pHAT Button Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)

Dependencies 
---------------
This driver package depends on the qwiic I2C driver: 
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Top pHAT Button module documentation is hosted at [ReadTheDocs](https://sparkfun-top-phat-button.readthedocs.io/en/latest/?)

Installation
-------------

### PyPi Installation
This repository is hosted on PyPi as the [sparkfun-top-phat-button](https://pypi.org/project/sparkfun-top-phat-button/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-top-phat-button
```
For the current user:

```sh
pip install sparkfun-top-phat-button
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
pip install sparkfun_top_phat_button-<version>.tar.gz
  
```
Example Use
 ---------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import top_phat_button
import time
import sys

myButtons = top_phat_button.ToppHATButton()

def runExample():

    print("\nSparkFun Top pHAT Button  Example 1\n")

    if myButtons.is_connected() == False:
        print("The Top pHAT Button device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    myButtons.pressed_interrupt_enable = False
    myButtons.clicked_interrupt_enable = False
    
    while True:
        myButtons.button_pressed #These functions must be called to update button variables to their latest setting
        myButtons.button_clicked #These functions must be called to update button variables to their latest setting  
        if myButtons.a_pressed == True:
            print("A Pressed")
        if myButtons.a_clicked == True:
            print("A Released")
        if myButtons.b_pressed == True:
            print("B Pressed")
        if myButtons.b_clicked == True:
            print("B Released")
        if myButtons.up_pressed == True:
            print("Up Pressed")
        if myButtons.up_clicked == True:
            print("Up Released")
        if myButtons.down_pressed == True:
            print("Down Pressed")
        if myButtons.down_clicked == True:
            print("Down Released")
        if myButtons.left_pressed == True:
            print("Left Pressed")
        if myButtons.left_clicked == True:
            print("Left Released")
        if myButtons.right_pressed == True:
            print("Right Pressed")
        if myButtons.right_clicked == True:
            print("Right Released")
        if myButtons.center_pressed == True:
            print("Center Pressed")
        if myButtons.center_clicked == True:
            print("Center Released")
    
        time.sleep(.1)


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
