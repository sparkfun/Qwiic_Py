![Qwiic BUTTON - Python Package](docs/images/gh-banner.png "qwiic BUTTON Python Package")

# SparkFun Qwiic Button - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_button)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_button_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_button_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html)

The SparkFun Qwiic Button Module provides a simple and cost effective solution for adding Button capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic BUTTON. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_button_py/classqwiic__button_1_1_qwiic_button.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the button via a single Qwiic cable. This includes checking button state, configuring button LED, change I2C address and more. The capabilities of the BUTTON are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Qwiic Button Red LED](https://www.sparkfun.com/sparkfun-qwiic-button-red-led.html)
* [SparkFun Qwiic Button Green LED](https://www.sparkfun.com/sparkfun-qwiic-button-green-led.html)
* [SparkFun Qwiic Button Breakout](https://www.sparkfun.com/sparkfun-qwiic-button-breakout.html)

### Supported Platforms

| Python | Platform | Boards |
|--|--|--|
| Python | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html) , [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi - RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)
|CircuitPython | Raspberry Pi - RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html)

> [!NOTE]
> The listed supported platforms and boards are the primary platform targets tested. It is fully expected that this package will work across a wide variety of Python enabled systems. 

## Installation 

The first step to using this package is installing it on your system. The install method depends on the python platform. The following sections outline installation on Python, MicroPython and CircuitPython.

### Python 

#### PyPi Installation

The package is primarily installed using the `pip3` command, downloading the package from the Python Index - "PyPi". 

Note - the below instructions outline installation on a Linux-based (Raspberry Pi) system.

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv path/to/venv
```
You can pass any path as path/to/venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
path/to/venv/bin/pip3 install sparkfun-qwiic-button
```
Now you should be able to run any example or custom python scripts that have `import qwiic_button` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_button_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_button_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_button
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_button\qwiic_button_ex1_buttonPress
circup example qwiic_button\qwiic_button_ex2_LEDon
circup example qwiic_button\qwiic_button_ex3_LEDconfig
circup example qwiic_button\qwiic_button_ex4_queueUsage
circup example qwiic_button\qwiic_button_ex5_popQueue
circup example qwiic_button\qwiic_button_ex6_changeI2CAddress
circup example qwiic_button\qwiic_button_ex7_2Buttons
```

Example Use
 ---------------
Below is a quickstart program to print readings from the BUTTON.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_button_py/blob/main/examples/README.md) for a summary of the available examples.

```python

import qwiic_button 
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 1")
    my_button = qwiic_button.QwiicButton()

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nButton ready!")
    
    while True:   
        
        if my_button.is_button_pressed() == True:
            print("The button is pressed!")

        else:    
            print("The button is not pressed!")
            
        time.sleep(0.1)

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
