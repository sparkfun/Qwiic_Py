![Qwiic PIR](https://cdn.sparkfun.com/assets/parts/1/6/4/0/7/17375-SparkFun_Qwiic_PIR_-_1uA__EKMB1107112_-01.jpg "SparkFun Qwiic PIR")

# SparkFun Qwiic PIR - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-pir)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_pir/)

The SparkFun Qwiic PIR boards detect motion with a passive infrared sensor and report detect and remove events, with timestamps, over I2C. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is the Python driver for the Qwiic PIR. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package is a port of the [SparkFun Qwiic PIR Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_PIR_Arduino_Library). It reads the raw and debounced PIR state, the detect and remove event queues with their timestamps, configures the debounce time and interrupt, and changes the I2C address. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Qwiic PIR - 1 uA (EKMB1107112)](https://www.sparkfun.com/products/17375)
* [SparkFun Qwiic PIR - 170 uA (EKMC4607112K)](https://www.sparkfun.com/products/17374)

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
~/sparkfun_venv/bin/pip install sparkfun-qwiic-pir
```

Run any example or script that does `import qwiic_pir` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_pir
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_pir/examples
```

Add `@qwiic_pir-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_pir
```

To copy an example to the board:

```sh
circup example qwiic_pir/qwiic_pir_ex1_raw_reading
```

## Example Use

Below is a quickstart program that prints whether the PIR sees an object. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_pir
import qwiic_i2c


def run_example():
    print("\nSparkFun Qwiic PIR Example 1\n")
    my_pir = qwiic_pir.QwiicPIR()

    if not my_pir.begin():
        print("The Qwiic PIR isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    print("Waiting 30 seconds for PIR to stabilize")
    for i in range(0, 30):
        print(i)
        qwiic_i2c.delay_ms(1000)

    print("Device Stable")

    while True:
        if my_pir.raw_reading():
            print("Object Detected")
        else:
            print("Object Removed")
        qwiic_i2c.delay_ms(200)


if __name__ == "__main__":
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example 1")
        sys.exit(0)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_pir](https://docs.sparkfun.com/Qwiic_Py/qwiic_pir/).

## Migrating from 2.x

Version 3 has one name per method, and runs on MicroPython and CircuitPython as well as Linux.

| 2.x | 3.0 |
| --- | --- |
| `set_I2C_address(a)` (returned `None`) | `set_i2c_address(a)` (returns `True`, or `False` for an invalid address) |
| `get_I2C_address()` | `get_i2c_address()` |
| `available_addresses` held `0x12` twice and was missing `0x09` | `available_addresses` is `0x12`, then every other address from `0x08` to `0x77` |
| `QwiicPIR(address=a)` accepted any value | an address outside `available_addresses` falls back to the default `0x12` |
| Linux only (`setup.py`) | CPython, MicroPython and CircuitPython |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
