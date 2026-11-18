# SparkFun u-blox GPS - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-ublox-gps)
![License](https://img.shields.io/badge/license-GPL--3.0-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/ublox_gps/)

SparkFun's u-blox GPS boards give your project position, time, high-precision RTK and dead reckoning. This package talks to them over a serial port (UART or USB) or SPI and parses the UBX protocol, using the parsing capabilities of [ubxtranslator](https://github.com/dalymople/ubxtranslator) by [dalymople](https://github.com/dalymople).

This package is the Python driver for u-blox GPS modules. It runs on CPython on Linux (it needs `pyserial`, and `spidev` for SPI); I2C is not supported. It is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [License](#license)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

A background thread reads the port, collects UBX packets and NMEA sentences, and the methods poll the module for a message and return it as a named tuple scaled to real units: position and heading (`geo_coords()`, `hp_geo_coords()`), time (`date_time()`), dilution of precision (`get_dop()`), satellites, vehicle attitude and sensor fusion (`veh_attitude()`, `esf_*()`), raw measurements (`rawx_measurements()`), module information (`module_software_version()`, ...) and configuration (`ubx_get_val()`, `ubx_set_val()`, `set_auto_msg()`). `stream_nmea()` returns the NMEA sentences. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun GPS-RTK2 - ZED-F9P (GPS-15136)](https://www.sparkfun.com/products/15136)
* [SparkFun GPS-RTK - NEO-M8P-2 (GPS-15005)](https://www.sparkfun.com/products/15005)
* [SparkFun ZOE-M8Q Breakout (GPS-15193)](https://www.sparkfun.com/products/15193)
* [SparkFun SAM-M8Q Breakout (GPS-15210)](https://www.sparkfun.com/products/15210)
* [SparkFun GPS-RTK Dead Reckoning - ZED-F9R (GPS-22693)](https://www.sparkfun.com/products/22693)
* [SparkFun GPS-RTK Dead Reckoning pHAT - ZED-F9R (GPS-21305)](https://www.sparkfun.com/products/21305)
* [SparkFun GPS Dead Reckoning - NEO-M9N (GPS-15733)](https://www.sparkfun.com/products/15733)

## Supported Platforms

| Python | Platform | Boards |
| --- | --- | --- |
| CPython | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html), [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) |

> [!NOTE]
> This package uses a serial port or SPI, so it is not available for MicroPython or CircuitPython.

## Installation

### CPython (pip)

```sh
python3 -m venv ~/sparkfun_venv
~/sparkfun_venv/bin/pip install sparkfun-ublox-gps
```

This also installs `pyserial`, and `spidev` on Linux. Run any example or script that does `import ublox_gps` with `~/sparkfun_venv/bin/python3 example_script.py`.

On a Raspberry Pi, enable the serial port (or SPI) with `sudo raspi-config` under **Interface Options**.

## Example Use

Below is a quickstart program that prints the longitude and latitude. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import serial
from ublox_gps import UbloxGPS
# SPI also works: pass a spidev.SpiDev() instead. I2C is not supported.

port = serial.Serial("/dev/serial0", baudrate=38400, timeout=1)
gps = UbloxGPS(port)


def run():
    try:
        print("Listening for UBX Messages.")
        while True:
            try:
                coords = gps.geo_coords()
                print(coords.lon, coords.lat)
            except (ValueError, IOError) as err:
                print(err)
    finally:
        port.close()


if __name__ == "__main__":
    run()
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/ublox_gps](https://docs.sparkfun.com/Qwiic_Py/ublox_gps/).

## License

GPL-3.0-or-later (unlike the other Qwiic drivers, which are MIT). See [LICENSE](LICENSE).

## Migrating from 2.x

Version 3 renames the classes to PEP 8 names and has no properties.

| 2.x | 3.0 |
| --- | --- |
| `UbloxGps` | `UbloxGPS` |
| `sfeSpiWrapper` (module `ublox_gps.sfeSpiWrapper`) | `SPIWrapper` (module `ublox_gps.spi_wrapper`, also `ublox_gps.SPIWrapper`) |
| `gps.get_DOP()` | `gps.get_dop()` |
| `UbloxGps.device_name`, `UbloxGps.available_addresses` (`0x42`) | removed: the driver doesn't use I2C, so it isn't listed as a Qwiic I2C device |
| `core.*.repeated_block`, `core.*.fmt` (properties) | `is_repeated_block()`, `get_fmt()` |
| `Message.id_`, `Cls.id_` (properties) | `get_id()` |
| `Parser.receive_from(stream, skippreamble, ignoreunsupported)` | `receive_from(stream, skip_preamble, ignore_unsupported)` |
| `UbloxGps(spidev_port)` failed (`sfeSpiWrapper` module called as a class) | `UbloxGPS(spidev_port)` wraps the port in `SPIWrapper` |
| `UbloxGps()` opened `/dev/serial0/` (trailing slash, always failed) | `UbloxGPS()` opens `/dev/serial0` |
| `import ublox_gps` needed `spidev` | `spidev` is needed only for SPI, and is a Linux-only dependency |
| `veh_attitude().accRoll` was not scaled | scaled to degrees like `accPitch` and `accHeading` |
| `R8` fields raised `NameError` (`double`) | parsed as `float` |
| - | new `rawx_measurements()` (UBX-RXM-RAWX) |
| `test_script.py` (called a missing `ublox_debug()`) | removed; see the examples |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
