![Qwiic SerLCD Python Package](docs/images/gh-banner-py-qwiic-serlcd.png "qwiic SerLCD Python Package" )

# SparkFun Qwiic SerLCD - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_serlcd)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/Qwiic_SerLCD_Py)
![License](https://img.shields.io/github/license/sparkfun/Qwiic_SerLCD_Py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html)

The line of SparkFun Qwiic SerLCD products provide a simple and cost effective solution for adding a "text based" LCD display to your project. Implementing a SparkFun Qwiic interface, a SerLCD is rapidly added to any board that is part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic SerLCD series of products. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html)
* [Examples](#examples)

## About the Package

This python package enables the user to access all of the features of these LCD products via a single Qwiic cable. This includes writing text to the screen, adjusting backlight levels (color), customizing splash screen and much much more. They come pre-programmed with the fully open-sourced [OpenLCD firmware](https://github.com/sparkfun/OpenLCD). All of the capabilities of these LCD screens are each demonstrated in the included examples.


New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).
### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun SerLCD 16x2 - RGB Backlight (QWIIC)](https://www.sparkfun.com/products/16396)
* [SparkFun SerLCD 16x2 - RGB Text (QWIIC)](https://www.sparkfun.com/products/16397)
* [SparkFun SerLCD 20x4 - RGB Backlight (QWIIC)](https://www.sparkfun.com/products/16398)

### Supported Platforms

| Python | Platform | Boards |
|--|--|--|
| Python | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html) , [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi - RP2, ESP32 | [SparkFun RP2040 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html), [SparkFun RP2350 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2350.html), [SparkFun ESP32 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-usb-c.html)
|CircuitPython | Raspberry Pi - RP2, ESP32 | [SparkFun RP2040 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html), [SparkFun RP2350 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2350.html), [SparkFun ESP32 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-usb-c.html)

> [!NOTE]
> The listed supported platforms and boards are the primary platform targets tested. It is fully expected that this package will work across a wide variety of Python enabled systems. 

## Installation 

The first step to using this package is installing it on your system. The install method depends on the python platform. The following sections outline installation on Python, MicroPython and CircuitPython.

### Python 

The package is primarily installed using the `pip3` command, downloading the package from the Python Index - "PyPi". Note - the below instructions outline installation an Linux-based (Raspberry Pi) system.

#### PyPi Installation

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv path/to/venv
```
You can pass any path as path/to/venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
path/to/venv/bin/pip3 install sparkfun-qwiic-serlcd
```
Now you should be able to run any example or custom python scripts that have `import qwiic_serlcd` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

#### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_serlcd_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mprmeote mip install github:sparkfun/qwiic_serlcd_py@examples
```

#### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_serlcd
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUP on Windows. Linux and Mac will have different path seperators (i.e. "/" vs. "\"). See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)
```sh
circup example qwiic_serlcd\ex1_qwiic_serlcd_hello_world
circup example qwiic_serlcd\ex2_qwiic_serlcd_backlight
circup example qwiic_serlcd\ex3_qwiic_serlcd_set_cursor_position
circup example qwiic_serlcd\ex4_qwiic_serlcd_move_cursor
circup example qwiic_serlcd\ex5_qwiic_serlcd_enable_cursor
circup example qwiic_serlcd\ex6_qwiic_serlcd_blink_cursor
circup example qwiic_serlcd\ex7_qwiic_serlcd_scroll
circup example qwiic_serlcd\ex8_qwiic_serlcd_autoscroll_with_text
circup example qwiic_serlcd\ex9_qwiic_serlcd_custom_character
circup example qwiic_serlcd\ex10_qwiic_serlcd_turn_off_display
circup example qwiic_serlcd\ex11_qwiic_serlcd_text_direction
circup example qwiic_serlcd\ex12_qwiic_serlcd_console_input_to_display
circup example qwiic_serlcd\ex13_qwiic_serlcd_fast_backlight
circup example qwiic_serlcd\ex14_qwiic_serlcd_show_firmware_version
circup example qwiic_serlcd\ex15_qwiic_serlcd_message_enable
circup example qwiic_serlcd\ex16_qwiic_serlcd_set_splash
circup example qwiic_serlcd\ex17_qwiic_serlcd_change_i2c_address.py
```

## Examples
Below is a quickstart program to print "Hello World!" to the Serial LCD.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_serlcd_py/blob/main/examples/README.md) for a summary of the available examples.

```python
from __future__ import print_function
import qwiic_serlcd
import time
import sys

def runExample():

	print("\nSparkFun Qwiic SerLCD   Example 1\n")
	myLCD = qwiic_serlcd.QwiicSerlcd()

	if myLCD.connected == False:
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLCD.setBacklight(255, 255, 255) # Set backlight to bright white
	myLCD.setContrast(5) # set contrast. Lower to 0 for higher contrast.
	myLCD.clearScreen() # clear the screen - this moves the cursor to the home position as well

	time.sleep(1) # give a sec for system messages to complete
	
	myLCD.print("Hello World!")
	counter = 0
	while True:
		print("counter: %d" % counter)
		myLCD.setCursor(0,1)
		myLCD.print(str(counter))
		counter = counter + 1
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
```

