![Qwiic AS6212 Python Package](https://cdn.sparkfun.com//assets/parts/1/7/9/7/0/18521-SparkFun_Digital_Temperature_Sensor_Breakout_-_AS6212__Qwiic_-01.jpg "Qwiic AS6212 Python Package")

# SparkFun Qwiic AS6212 - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-as6212)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_as6212/)

The SparkFun Digital Temperature Sensor Breakout - AS6212 (Qwiic) provides a simple, low power and high accuracy solution for adding temperature sensing to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is a port of the [SparkFun AS6212 Qwiic Arduino Library](https://github.com/sparkfun/SparkFun_AS6212_Qwiic_Arduino_Library).

This package is the Python driver for the AS6212. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads temperature from the AS6212 over a single Qwiic cable, and configures its alert thresholds and polarity, consecutive faults, interrupt mode, conversion cycle time, sleep mode and single-shot conversions. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Digital Temperature Sensor Breakout - AS6212 (Qwiic)](https://www.sparkfun.com/products/18521)

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
~/sparkfun_venv/bin/pip install sparkfun-qwiic-as6212
```

Run any example or script that does `import qwiic_as6212` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_as6212
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_as6212/examples
```

Add `@qwiic_as6212-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_as6212
```

To copy an example to the board:

```sh
circup example qwiic_as6212/qwiic_as6212_ex1_basic_readings
```

## Example Use

Below is a quickstart program that prints the temperature in Fahrenheit once a second. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_as6212
import qwiic_i2c


def run_example():
    print("\nSparkFun Qwiic AS6212 Sensor Example\n")
    my_sensor = qwiic_as6212.QwiicAS6212()

    if not my_sensor.is_connected():
        print("The Qwiic AS6212 Sensor device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    my_sensor.begin()

    while True:
        print("Temperature: %.2fF" % my_sensor.read_temp_f())
        qwiic_i2c.delay_ms(1000)


if __name__ == "__main__":
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example")
        sys.exit(0)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_as6212](https://docs.sparkfun.com/Qwiic_Py/qwiic_as6212/).

## Migrating from 2.x

Version 3 has one name per method and no properties, so it also runs on MicroPython builds without `property()`.

| 2.x | 3.0 |
| --- | --- |
| `QwiicAs6212Sensor` | `QwiicAS6212` |
| `sensor.connected` | `sensor.is_connected()` |
| `sensor.tempC`, `sensor.tempF` (last reading) | `sensor.temp_c`, `sensor.temp_f` |
| `write_config(targetState=...)` | `write_config(target_state=...)` |
| `print_config_binary()` (printed) | `get_config_binary()` (returns a string) |
| `print_binary(data)` (printed) | `format_binary(data)` (returns a string) |
| `set_consecutive_faults()`, `set_conversion_cycletime()` raised `NameError` for an invalid value | raise `ValueError` |
| `read_temp_c()`, `read_temp_f()` returned wrong values below 0 C | fixed (two's complement) |
| `get_conversion_cycletime()` raised `NameError` (and would have returned 4000 for 250 ms) | fixed |
| `is_connected()` used the default bus even when an `i2c_driver` was given | `is_connected()` uses the driver's own bus |
| Linux only (Raspberry Pi) | CPython, MicroPython and CircuitPython |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
