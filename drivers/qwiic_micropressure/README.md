![Qwiic MicroPressure Python Package](docs/images/gh-banner.png "Qwiic MicroPressure Python Package")

# SparkFun Qwiic MicroPressure - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-micropressure)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_micropressure/)

The SparkFun Qwiic MicroPressure Sensor provides a simple and cost effective solution for adding pressure sensing capabilities to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is the Python driver for the MicroPressure sensor. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads pressure from the MicroPressure sensor over a single Qwiic cable, in PSI, Pa, kPa, Torr, inHg, atm or bar. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Qwiic MicroPressure Sensor](https://www.sparkfun.com/products/16476)

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
~/sparkfun_venv/bin/pip install sparkfun-qwiic-micropressure
```

Run any example or script that does `import qwiic_micropressure` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_micropressure
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_micropressure/examples
```

Add `@qwiic_micropressure-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_micropressure
```

To copy an example to the board:

```sh
circup example qwiic_micropressure/qwiic_micropressure_ex1_basic
```

## Example Use

Below is a quickstart program that prints the pressure in several units. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_micropressure
import qwiic_i2c


def run_example():
    print("\nQwiic MicroPressure Example 1 - Basic Readings\n")
    my_micro_pressure = qwiic_micropressure.QwiicMicroPressure()

    if not my_micro_pressure.is_connected():
        print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    my_micro_pressure.begin()

    while True:
        print("Pressure(PSI): ", my_micro_pressure.read_pressure())
        print("Pressure(Pa): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_PA))
        print("Pressure(Bar): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_BAR))
        qwiic_i2c.delay_ms(500)


if __name__ == "__main__":
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example 1")
        sys.exit(0)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_micropressure](https://docs.sparkfun.com/Qwiic_Py/qwiic_micropressure/).

## Migrating from 2.x

Version 3 has one name per method and no properties, so it also runs on MicroPython builds without `property()`.

| 2.x | 3.0 |
| --- | --- |
| `sensor.connected` | `sensor.is_connected()` |
| `kPressurePsi`, `kPressurePa`, `kPressureKpa`, `kPressureTorr` | `PRESSURE_PSI`, `PRESSURE_PA`, `PRESSURE_KPA`, `PRESSURE_TORR` |
| `kPressureInHg`, `kPressureAtm`, `kPressureBar` | `PRESSURE_INHG`, `PRESSURE_ATM`, `PRESSURE_BAR` |
| `kReadPressureCommandReg`, `kReadPressureCommandData` | `READ_PRESSURE_COMMAND_REG`, `READ_PRESSURE_COMMAND_DATA` |
| `kMathSatMask`, `kMemoryIntegrityMask`, `kBusyMask`, `kPowerIndicationMask` | `MATH_SAT_MASK`, `MEMORY_INTEGRITY_MASK`, `BUSY_MASK`, `POWER_INDICATION_MASK` |
| `kOutputMin`, `kOutputMax`, `kMinPSI`, `kMaxPSI` | `OUTPUT_MIN`, `OUTPUT_MAX`, `MIN_PSI`, `MAX_PSI` |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
