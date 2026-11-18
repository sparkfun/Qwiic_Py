# SparkFun Qwiic EEPROM - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-eeprom)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_eeprom/)

The SparkFun Qwiic EEPROM Breakout gives your project 512 kbit (64 kbyte) of non-volatile storage. Implementing a SparkFun Qwiic I2C interface, it can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is the Python driver for the SparkFun Qwiic EEPROM (24512C, 512 kbit). It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads and writes bytes, 32-bit ints, floats, strings and byte lists to the EEPROM over a single Qwiic cable, handling page boundaries and write-complete polling. The memory size, page size and write time can be set for other I2C EEPROMs. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Qwiic EEPROM Breakout - 512Kbit](https://www.sparkfun.com/products/18355)

## Supported Platforms

| Python | Platform | Boards |
| --- | --- | --- |
| CPython | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html), [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) |
| CircuitPython | Raspberry Pi RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) |

> [!NOTE]
> These are the primary platforms tested. The package is expected to work on most Python-enabled systems.

## Installation

### CPython (pip)

```sh
python3 -m venv ~/sparkfun_venv
~/sparkfun_venv/bin/pip install sparkfun-qwiic-eeprom
```

Run any example or script that does `import qwiic_eeprom` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_eeprom
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_eeprom/examples
```

Add `@qwiic_eeprom-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_eeprom
```

To copy an example to the board:

```sh
circup example qwiic_eeprom/qwiic_eeprom_ex1_basic_read_write
```

## Example Use

Below is a quickstart program that writes and reads back a byte, an int and a float. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_eeprom


print("\nSparkFun Qwiic EEPROM, Example 1\n")
my_eeprom = qwiic_eeprom.QwiicEEPROM()

if not my_eeprom.begin():
    print("The Qwiic EEPROM isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(1)

print("Mem size in bytes: " + str(my_eeprom.length()))

my_eeprom.write_byte(300, 200)
print("I read: " + str(my_eeprom.read_byte(300)))       # 200

my_eeprom.write_int(10, -366)
print("I read: " + str(my_eeprom.read_int(10)))         # -366

my_eeprom.write_float(9, -7.35)
print("I read: " + str(round(my_eeprom.read_float(9), 2)))  # -7.35
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_eeprom](https://docs.sparkfun.com/Qwiic_Py/qwiic_eeprom/).

## Choosing the I2C Bus

On Linux the driver uses the board's Qwiic bus: `/dev/i2c-1` on a Raspberry Pi and `/dev/i2c-7` on a Jetson Orin Nano. On other boards, such as a Jetson Orin NX on a custom carrier ([Qwiic_EEPROM_Py#1](https://github.com/sparkfun/Qwiic_EEPROM_Py/issues/1)), pass the bus the EEPROM is on:

```python
import qwiic_i2c
import qwiic_eeprom

my_eeprom = qwiic_eeprom.QwiicEEPROM(i2c_bus=qwiic_i2c.get_i2c_bus(bus_id=7))  # /dev/i2c-7
```

## Migrating from 2.x

Version 2.x ran only on Linux (it used smbus2 directly). Version 3 runs on CPython, MicroPython and CircuitPython through qwiic_i2c.

| 2.x | 3.0 |
| --- | --- |
| `set_I2C_buffer_size()`, `get_I2C_buffer_size()` | `set_i2c_buffer_size()`, `get_i2c_buffer_size()` |
| `is_connected(i2c_address=255)`, `is_busy(i2c_address=255)` | `is_connected(i2c_address=None)`, `is_busy(i2c_address=None)` (both default to the driver's address) |
| `is_connected()` checked the platform default bus, not the driver's bus | `is_connected()` checks the bus the driver was given |
| Linux only (`setup.py`, smbus2) | CPython, MicroPython and CircuitPython (`pip`, `mip`, `circup`) |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
