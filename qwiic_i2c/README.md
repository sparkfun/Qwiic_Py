![Qwiic I2C Python Package](docs/images/i2c-gh-banner-py.png "qwiic IC Python Package" )

Sparkfun Qwiic I2C - Python Package
==============

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_i2c)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_i2c_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_i2c_py)
![X](https://img.shields.io/twitter/follow/sparkfun)

Python package to support multi platform I2C bus integrations for the SparkFun [qwiic ecosystem](https://www.sparkfun.com/qwiic)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Documentation](#documentation)
* [Installation](#installation)

### Supported Platforms
See the [MicroPython Downloads Page](https://micropython.org/download/?vendor=Sparkfun) for more boards compatible with MicroPython.
| Python | Platform | Boards |
|--|--|--|
| Python | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html) , [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi - RP2, ESP32 | [SparkFun RP2040 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html), [SparkFun RP2350 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2350.html), [SparkFun ESP32 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-usb-c.html)
|CircuitPython | Raspberry Pi - RP2, ESP32 | [SparkFun RP2040 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html), [SparkFun RP2350 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2350.html), [SparkFun ESP32 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-usb-c.html)

> [!NOTE]
> The listed supported platforms and boards are the primary platform targets tested. It is fully expected that this package will work across a wide variety of Python enabled systems. 

Dependencies 
---------------
The Raspberry Pi/Single Board Computer Linux driver of this package is dependent on 
[smbus](https://pypi.org/project/smbus/)

Documentation
-------------
The SparkFun qwiic I2C module documentation is hosted at [ReadTheDocs](https://qwiic-i2c-py.readthedocs.io/en/latest/index.html)

# Installation 

The first step to using this package is installing it on your system. The install method depends on the python platform. The following sections outline installation on Python, MicroPython and CircuitPython.

### Python 

#### PyPi Installation

The package is primarily installed using the `pip3` command, downloading the package from the Python Index - "PyPi". 

Note - the below instructions outline installation on a Linux-based (Raspberry Pi) system.

First, setup a virtual environment from a specific directory using venv:
```sh
python3 -m venv ~/sparkfun_venv
```
You can pass any path instead of ~/sparkfun_venv, just make sure you use the same one for all future steps. For more information on venv [click here](https://docs.python.org/3/library/venv.html).

Next, install the qwiic package with:
```sh
~/sparkfun_venv/bin/pip3 install sparkfun-qwiic-i2c
```
Now you should be able to run any example or custom python scripts that have `import qwiic_i2c` by running e.g.:
```sh
~/sparkfun_venv/bin/python3 example_script.py
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_i2c_py
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/qwiic_py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_i2c
```

Examples
---------------
This package is used extensively by the python modules for the SparkFun qwiic ecosystem. References to the modules can be found in the [sparkfun-python github topic](https://github.com/topics/sparkfun-python) or in the [drivers directories of Qwiic Py](https://github.com/sparkfun/Qwiic_Py/tree/main/qwiic/drivers).

General package use examples:

```python
# Import the package
import qwiic_i2c

# Get the default I2C bus
my_bus = qwiic_i2c.get_i2c_driver()

# Linux (Raspberry Pi) - Specify I2C bus index
my_bus = qwiic_i2c.get_i2c_driver(iBus = 1)

# MicroPython and CircuitPython - Specify SDA and SCL pins, and frequency
my_bus = qwiic_i2c.get_i2c_driver(sda=0, scl=1, freq=100000)

# Any platform - Use an I2C bus object you have already created
# MicroPython: machine.I2C or machine.SoftI2C
import machine
my_bus = qwiic_i2c.get_i2c_driver(machine.SoftI2C(sda=machine.Pin(0), scl=machine.Pin(1)))
# CircuitPython: busio.I2C, bitbangio.I2C, or board.I2C()
import board
my_bus = qwiic_i2c.get_i2c_driver(board.I2C())
# Linux: smbus2.SMBus
import smbus2
my_bus = qwiic_i2c.get_i2c_driver(smbus2.SMBus(1))

# The resulting bus can be passed to any qwiic device driver
# my_device = qwiic_device.QwiicDevice(i2c_driver=my_bus)

# Perform scan of I2C bus
scan_list = my_bus.scan()
print("Bus scan:", scan_list)

# Check if a device with the specified address is connected
ping_result = my_bus.ping(device_address)
print("Device is connected:", ping_result)

# Read one byte from the specified address
read_data = my_bus.read_byte(device_address, register_address)
print("Read byte:", read_data)

# Read one word (2 bytes) from the specified address
read_data = my_bus.read_word(device_address, register_address)
print("Read word:", read_data)

# Read several bytes from the specified address
read_data = my_bus.read_block(device_address, register_address, num_bytes_to_read)
print("Read block:", read_data)

# Write one byte to the specified address
my_bus.write_byte(device_address, register_address, write_data)

# Write one word (2 bytes) to the specified address
my_bus.write_word(device_address, register_address, write_data)

# Write several bytes to the specified address
my_bus.write_block(device_address, register_address, write_data)
```

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
