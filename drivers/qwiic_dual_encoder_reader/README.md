# SparkFun Qwiic Dual Encoder Reader - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-dual-encoder-reader)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_dual_encoder_reader/)

The Qwiic Dual Encoder Reader is an ATtiny84 that reads two quadrature motor encoders and reports their counts over I2C. It is built into the SparkFun Auto pHAT for Raspberry Pi. Its firmware is in the [SparkFun Dual Encoder Reader firmware repository](https://github.com/sparkfun/Qwiic_Dual_Encoder_Reader).

This package is the Python driver for the Qwiic Dual Encoder Reader. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads and sets the counts of both encoders, reads the change since the last check and the time since the last movement, and sets the count limit and interrupt timeout over a single Qwiic cable. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Auto pHAT for Raspberry Pi](https://www.sparkfun.com/products/16328)

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
~/sparkfun_venv/bin/pip install sparkfun-qwiic-dual-encoder-reader
```

Run any example or script that does `import qwiic_dual_encoder_reader` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_dual_encoder_reader
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_dual_encoder_reader/examples
```

Add `@qwiic_dual_encoder_reader-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_dual_encoder_reader
```

To copy an example to the board:

```sh
circup example qwiic_dual_encoder_reader/qwiic_dual_encoder_reader_ex1_read_counts
```

## Example Use

Below is a quickstart program that prints the counts of both encoders. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_dual_encoder_reader
import qwiic_i2c


print("\nSparkFun Qwiic Dual Encoder Reader Example 1\n")
my_encoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

if not my_encoders.is_connected():
    print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(1)

my_encoders.begin()

while True:
    print("Count1: %d, Count2: %d" % (my_encoders.get_count1(), my_encoders.get_count2()))
    qwiic_i2c.delay_ms(300)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_dual_encoder_reader](https://docs.sparkfun.com/Qwiic_Py/qwiic_dual_encoder_reader/).

## Migrating from 2.x

Version 3 has one name per method and no properties, so it also runs on MicroPython builds without `property()`. Version 2.x of this driver ran only on Linux; version 3 also runs on MicroPython and CircuitPython.

| 2.x | 3.0 |
| --- | --- |
| `encoders.connected` | `encoders.is_connected()` |
| `encoders.count1`, `encoders.count2` (get / set) | `encoders.get_count1()`, `encoders.set_count1(n)`, `encoders.get_count2()`, `encoders.set_count2(n)` |
| `encoders.limit` (get / set) | `encoders.get_limit()`, `encoders.set_limit(n)` |
| `encoders.int_timeout` (get / set) | `encoders.get_int_timeout()`, `encoders.set_int_timeout(ms)` |
| `encoders.moved` | `encoders.has_moved()` |
| `encoders.version` | `encoders.get_version()` |
| `since_last_movement()` raised an error when clearing the value (the default) | `since_last_movement()` clears the value |
| `get_diff()` returned the difference unsigned (0 to 65535) | `get_diff()` returns it signed (-32768 to 32767), like `get_count1()` |
| `set_count1()`, `set_count2()` failed for negative counts | they accept counts from -32768 to 32767 |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
