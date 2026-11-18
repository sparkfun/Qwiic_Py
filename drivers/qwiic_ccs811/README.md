<img src="https://cdn.sparkfun.com//assets/parts/1/2/3/2/9/14348-01.jpg" align="right" width=300 alt="SparkFun Qwiic Environmental Combo Breakout">

# SparkFun Qwiic CCS811 - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-ccs811)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_ccs811/)

The CCS811 is a digital gas sensor that measures equivalent CO2 (eCO2) and total volatile organic compounds (TVOC). Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is the Python driver for the CCS811, ported from the [SparkFun CCS811 Arduino Library](https://github.com/sparkfun/SparkFun_CCS811_Arduino_Library). It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads equivalent CO2 and TVOC from the CCS811 over a single Qwiic cable, and sets its drive mode, interrupts, baseline and temperature and humidity compensation. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Environmental Combo Breakout - CCS811/BME280](https://www.sparkfun.com/products/14348)
* [SparkFun Air Quality Breakout - CCS811](https://www.sparkfun.com/products/14193)

> [!NOTE]
> Both boards are retired, and their product pages now open the successor, the Environmental Combo Breakout - ENS160/BME280. That board uses the [qwiic_ens160](https://github.com/sparkfun/Qwiic_Py/tree/main/drivers/qwiic_ens160) and [qwiic_bme280](https://github.com/sparkfun/Qwiic_Py/tree/main/drivers/qwiic_bme280) drivers, not this one.

## Supported Platforms

| Python | Platform | Boards |
| --- | --- | --- |
| CPython | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html), [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) |
| CircuitPython | Raspberry Pi RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) |

> [!NOTE]
> These are the primary platforms tested. The package is expected to work on most Python-enabled systems.

### Raspberry Pi

The CCS811 stretches the I2C clock, which the Raspberry Pi only handles with a slower I2C clock. Add this line to `/boot/firmware/config.txt` (`/boot/config.txt` before Raspberry Pi OS Bookworm), then reboot:

```ini
# Enable I2C clock stretching
dtparam=i2c_arm_baudrate=10000
```

`QwiicCCS811.is_rpi_i2c_baudrate_ok()` returns `False` on a Raspberry Pi without this setting, and `True` on every other system.

## Installation

### CPython (pip)

```sh
python3 -m venv ~/sparkfun_venv
~/sparkfun_venv/bin/pip install sparkfun-qwiic-ccs811
```

Run any example or script that does `import qwiic_ccs811` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_ccs811
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_ccs811/examples
```

Add `@qwiic_ccs811-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_ccs811
```

To copy an example to the board:

```sh
circup example qwiic_ccs811/qwiic_ccs811_ex1_basic_readings
```

## Example Use

Below is a quickstart program that prints the equivalent CO2 and TVOC readings. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_ccs811
import qwiic_i2c


print("\nSparkFun CCS811 Sensor Basic Example\n")
my_sensor = qwiic_ccs811.QwiicCCS811()

if not my_sensor.is_connected():
    print("The Qwiic CCS811 device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(1)

if not my_sensor.begin():
    print("Unable to initialize the CCS811. Please check your connection", file=sys.stderr)
    sys.exit(1)

while True:
    my_sensor.read_algorithm_results()
    print("CO2:\t%.3f" % my_sensor.get_co2())
    print("tVOC:\t%.3f\n" % my_sensor.get_tvoc())
    qwiic_i2c.delay_ms(1000)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_ccs811](https://docs.sparkfun.com/Qwiic_Py/qwiic_ccs811/).

## Migrating from 2.x

Version 3 has one name per method and no properties, so it also runs on MicroPython builds without `property()`. It is no longer Linux only.

| 2.x | 3.0 |
| --- | --- |
| `QwiicCcs811` | `QwiicCCS811` |
| `sensor.connected` | `sensor.is_connected()` |
| `begin()` returned `SENSOR_SUCCESS` (0) or an error code, and printed "Invalid Chip ID" | `begin()` returns `True` or `False` without printing |
| `sensor.CO2`, `sensor.TVOC` | `sensor.get_co2()`, `sensor.get_tvoc()` |
| `sensor.resistance`, `sensor.temperature` | `sensor.get_resistance()`, `sensor.get_temperature()` |
| `sensor.baseline` (get / set) | `sensor.get_baseline()`, `sensor.set_baseline(b)` |
| `sensor.error_register` | `sensor.get_error_register()` |
| `sensor.referance_resistance` (get / set) | `sensor.get_reference_resistance()`, `sensor.set_reference_resistance(r)` |
| `sensor.refResistance`, `sensor.vrefCounts`, `sensor.ntcCounts` | `sensor.ref_resistance`, `sensor.vref_counts`, `sensor.ntc_counts` |
| `set_environmental_data(relativeHumidity, temperature)` | `set_environmental_data(relative_humidity, temperature)` |
| `read_ntc()` printed an error and returned 1 on a zero reading | `read_ntc()` returns `SENSOR_GENERIC_ERROR` without printing |
| The constructor printed a warning on a Raspberry Pi without `i2c_arm_baudrate=10000` | `QwiicCCS811.is_rpi_i2c_baudrate_ok()` returns `False` instead; it also reads `/boot/firmware/config.txt` (Bookworm) |
| Linux only (`setup.py`) | CPython, MicroPython and CircuitPython |
| `begin()` raised `OSError` when no device answered | `begin()` returns `False` |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
