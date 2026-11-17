![Qwiic OTOS - Python Package](docs/images/gh-banner.png "qwiic OTOS Python Package")

# SparkFun Qwiic OTOS - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_otos)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_otos_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_otos_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html)

The SparkFun Qwiic Opitical Tracking Odometry Sensor OTOS Module provides a simple and cost effective solution for adding Opitical Tracking Odometry Sensor capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic OTOS. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_otos_py/classqwiic__otos_1_1_qwiic_o_t_o_s.html)
* [Examples](#example-use)

## About the Package

This python package enables the user to access the features of the OTOS via a single Qwiic cable. This includes odometry tracking, reading velocity and acceleration, performing calibration and more. The capabilities of the OTOS are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Opitical Tracking Odometry Sensor Sensor - OTOS](https://www.sparkfun.com/products/24904)

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
path/to/venv/bin/pip3 install sparkfun-qwiic-otos
```
Now you should be able to run any example or custom python scripts that have `import qwiic_otos` by running e.g.:
```sh
path/to/venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_otos_py
```

If you would also like to install the examples for this repository, issue the following mip command as well:
```sh
mpremote mip install --target "" github:sparkfun/qwiic_otos_py@examples
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_otos
```

If you would like to install any of the examples from this repository, issue the corresponding circup command from below. (NOTE: The below syntax assumes you are using CircUp on Windows. Linux and Mac will have different path seperators. See the [CircUp "example" command documentation](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/example-command) for more information)

```sh
circup example qwiic_otos\qwiic_otos_ex1_basic_readings
circup example qwiic_otos\qwiic_otos_ex2_set_units
circup example qwiic_otos\qwiic_otos_ex3_calibration
circup example qwiic_otos\qwiic_otos_ex4_set_offsets_and_position
circup example qwiic_otos\qwiic_otos_ex5_velocity_and_acceleration
circup example qwiic_otos\qwiic_otos_ex6_standard_deviation
circup example qwiic_otos\qwiic_otos_ex7_get_version
circup example qwiic_otos\qwiic_otos_ex8_self_test
```

Example Use
 ---------------
Below is a quickstart program to print readings from the OTOS.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_otos_py/blob/master/examples/README.md) for a summary of the available examples.

```python

import qwiic_otos
import sys
import time

def runExample():
    print("\nQwiic OTOS Example 1 - Basic Readings\n")

    myOtos = qwiic_otos.QwiicOTOS()

    if myOtos.is_connected() == False:
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    myOtos.begin()

    print("Ensure the OTOS is flat and stationary during calibration!")
    for i in range(5, 0, -1):
        print("Calibrating in %d seconds..." % i)
        time.sleep(1)

    print("Calibrating IMU...")

    myOtos.calibrateImu()

    myOtos.resetTracking()

    while True:
        myPosition = myOtos.getPosition()

        print()
        print("Position:")
        print("X (Inches): {}".format(myPosition.x))
        print("Y (Inches): {}".format(myPosition.y))
        print("Heading (Degrees): {}".format(myPosition.h))

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
