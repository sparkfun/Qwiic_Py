Qwiic_Py
========

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Py.svg" /></a>
	<a href="https://qwiic-py.readthedocs.io/en/latest/" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Py/blob/main/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
</p>

Every SparkFun [Qwiic](https://www.sparkfun.com/qwiic) Python driver, in one repository. The drivers run on CPython (Linux single board computers), MicroPython and CircuitPython. Each one is a separate package, so you install only the drivers you need.

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Choosing the Bus](#choosing-the-bus)
* [Finding Connected Devices](#finding-connected-devices)
* [Repository Structure](#repository-structure)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)
* [Contributing](#contributing)

## Supported Platforms

| Python | Platform | Boards tested |
| --- | --- | --- |
| CPython 3.8+ | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html), [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) |
| CircuitPython | RP2, ESP32 | [SparkFun Pro Micro RP2350](https://www.sparkfun.com/sparkfun-pro-micro-rp2350.html), [SparkFun IoT RedBoard ESP32](https://www.sparkfun.com/sparkfun-iot-redboard-esp32-development-board.html), [SparkFun IoT RedBoard RP2350](https://www.sparkfun.com/sparkfun-iot-redboard-rp2350.html) |

A few drivers for serial or SPI devices are CPython-only; the [driver list](docs/drivers.md) shows each driver's platforms.

## Installation

Every driver installs on its own and pulls in [qwiic_i2c](https://github.com/sparkfun/Qwiic_Py/tree/main/qwiic_i2c), the shared I2C layer. The commands below use the BME280 as an example; each driver's README has its own.

### CPython (pip)

```sh
python3 -m venv ~/sparkfun_venv
~/sparkfun_venv/bin/pip install sparkfun-qwiic-bme280     # one driver
~/sparkfun_venv/bin/pip install sparkfun-qwiic            # every driver, plus the qwiic module
```

### MicroPython (mip)

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_bme280
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_bme280/examples
```

Add `@qwiic_bme280-<version>` to install a specific release.

### CircuitPython (circup)

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_bme280
circup example qwiic_bme280/qwiic_bme280_ex1_basic_readings
```

## Choosing the Bus

Every driver uses the board's default Qwiic bus unless you give it one. The bus can be the first argument, or `i2c_bus=`, and can be the platform's own bus object:

```python
sensor = qwiic_bme280.QwiicBME280()                            # default bus
sensor = qwiic_bme280.QwiicBME280(machine.I2C(1))              # MicroPython
sensor = qwiic_bme280.QwiicBME280(busio.I2C(board.SCL, board.SDA))  # CircuitPython
sensor = qwiic_bme280.QwiicBME280(smbus2.SMBus(7))             # Linux, /dev/i2c-7
sensor = qwiic_bme280.QwiicBME280(bus, 0x76)                   # a bus and an address
```

To change the default bus for every driver created after that, use `qwiic_i2c.set_default_i2c_bus()`. This is useful for a SoftI2C port, or on a board where the automatic choice is wrong:

```python
qwiic_i2c.set_default_i2c_bus(machine.SoftI2C(scl=machine.Pin(5), sda=machine.Pin(4)))
sensor = qwiic_bme280.QwiicBME280()                            # uses the SoftI2C bus
```

## Finding Connected Devices

The `qwiic` module (installed with `sparkfun-qwiic`) finds connected devices and creates their driver objects:

```python
import qwiic

print(qwiic.list_devices())                  # [(0x77, 'Qwiic BME280', 'QwiicBME280'), ...]
sensor = qwiic.create_device("QwiicBME280")
```

See [qwiic/README.md](https://github.com/sparkfun/Qwiic_Py/blob/main/qwiic/README.md) for the full API.

## Repository Structure

```text
Qwiic_Py/
├── qwiic_i2c/                the I2C layer every driver uses
├── drivers/
│   └── qwiic_<chip>/         one directory per device driver: module, examples, README, pyproject.toml
├── qwiic/                    the sparkfun-qwiic meta-package and its generated driver registry
├── tools/                    generators, checks, bundle and docs builders used by CI
├── tests/                    tests that need no hardware
└── docs/                     the Read the Docs site and the shared Doxygen config
```

Each driver is released on its own, with a tag named `<driver>-<version>` (for example `qwiic_bme280-3.0.0`) that CI publishes to PyPI. The CircuitPython bundle is a GitHub Release named by date.

## Documentation

* [qwiic-py.readthedocs.io](https://qwiic-py.readthedocs.io/en/latest/): this overview and the [list of drivers](docs/drivers.md)
* [docs.sparkfun.com/Qwiic_Py](https://docs.sparkfun.com/Qwiic_Py/): each driver's API reference
* Each driver's README and `examples/README.md`

## Migrating from 2.x

Version 3 moved every driver into this repository and gave them one consistent API:

* One name per method, following PEP 8. The camelCase duplicates are gone (`readByte` is now `read_byte`), and classes use the part number in capitals (`QwiicBME280`).
* No properties: `sensor.connected` is now `sensor.is_connected()`, `sensor.pressure` is `sensor.read_pressure()`, and so on.
* Drivers no longer print or use the `time` module, and run on MicroPython builds without `property()` or packages.
* mip installs move from `github:sparkfun/<repo>` to `github:sparkfun/Qwiic_Py/drivers/<driver>`. PyPI names don't change.

[MIGRATION.md](https://github.com/sparkfun/Qwiic_Py/blob/main/MIGRATION.md) lists every renamed class and method, driver by driver. Version 2 stays on the [2.x tags](https://github.com/sparkfun/Qwiic_Py/tree/20260227) and PyPI for Python 3.6 and 3.7 users.

## Contributing

Bug reports, fixes and new drivers are welcome. [CONTRIBUTING.md](https://github.com/sparkfun/Qwiic_Py/blob/main/CONTRIBUTING.md) describes the driver conventions, the tools and how to release.

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
