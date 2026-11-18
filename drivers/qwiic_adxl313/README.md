# SparkFun Qwiic ADXL313 - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-adxl313)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_adxl313/)

The SparkFun Triple Axis Digital Accelerometer Breakout - ADXL313 (Qwiic) provides a simple and cost effective solution for adding low power acceleration sensing to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is the Python driver for the ADXL313. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads 3-axis acceleration from the ADXL313, and configures its range, bandwidth, low power mode, activity and inactivity detection, autosleep, interrupts and FIFO over a single Qwiic cable. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Triple Axis Digital Accelerometer Breakout - ADXL313 (Qwiic)](https://www.sparkfun.com/products/17241)

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
~/sparkfun_venv/bin/pip install sparkfun-qwiic-adxl313
```

Run any example or script that does `import qwiic_adxl313` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_adxl313
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_adxl313/examples
```

Add `@qwiic_adxl313-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_adxl313
```

To copy an example to the board:

```sh
circup example qwiic_adxl313/qwiic_adxl313_ex1_basic_readings
```

## Example Use

Below is a quickstart program that prints the raw acceleration on each axis. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_adxl313
import qwiic_i2c


print("\nSparkFun ADXL313 Example 1 - Basic Readings\n")
my_adxl = qwiic_adxl313.QwiicADXL313()

if not my_adxl.is_connected():
    print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(1)

my_adxl.measure_mode_on()

while True:
    if my_adxl.data_ready():
        my_adxl.read_accel()  # updates my_adxl.x, my_adxl.y and my_adxl.z
        print("{: 06d}\t{: 06d}\t{: 06d}".format(my_adxl.x, my_adxl.y, my_adxl.z))
        qwiic_i2c.delay_ms(30)
    else:
        print("Waiting for data")
        qwiic_i2c.delay_ms(500)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_adxl313](https://docs.sparkfun.com/Qwiic_Py/qwiic_adxl313/).

## Migrating from 2.x

Version 3 uses snake_case names, one name per method and no properties, so it also runs on MicroPython builds without `property()`. Version 2.x of this driver ran only on Linux; version 3 also runs on MicroPython and CircuitPython. The `ADXL313_*` constants and the `x`, `y`, `z` attributes are unchanged.

| 2.x | 3.0 |
| --- | --- |
| `QwiicAdxl313` | `QwiicADXL313` |
| `adxl.connected`, `adxl.isConnected()` | `adxl.is_connected()` |
| `adxl.measureModeOn()` | `adxl.measure_mode_on()` |
| `adxl.dataReady()` | `adxl.data_ready()` |
| `adxl.readAccel()` | `adxl.read_accel()` |
| `adxl.getRange()` | `adxl.get_range()` |
| `adxl.setRange(r)` | `adxl.set_range(r)` |
| `adxl.autosleepOn()` | `adxl.autosleep_on()` |
| `adxl.autosleepOff()` | `adxl.autosleep_off()` |
| `adxl.setRegisterBit(reg, bit, state)` | `adxl.set_register_bit(reg, bit, state)` |
| `adxl.getRegisterBit(reg, bit)` | `adxl.get_register_bit(reg, bit)` |
| `adxl.setActivityX(s)`, `setActivityY(s)`, `setActivityZ(s)` | `adxl.set_activity_x(s)`, `set_activity_y(s)`, `set_activity_z(s)` |
| `adxl.setInactivityX(s)`, `setInactivityY(s)`, `setInactivityZ(s)` | `adxl.set_inactivity_x(s)`, `set_inactivity_y(s)`, `set_inactivity_z(s)` |
| `adxl.setActivityThreshold(t)`, `getActivityThreshold()` | `adxl.set_activity_threshold(t)`, `get_activity_threshold()` |
| `adxl.setInactivityThreshold(t)`, `getInactivityThreshold()` | `adxl.set_inactivity_threshold(t)`, `get_inactivity_threshold()` |
| `adxl.setTimeInactivity(t)`, `getTimeInactivity()` | `adxl.set_time_inactivity(t)`, `get_time_inactivity()` |
| `adxl.setInterruptMapping(bit, pin)` | `adxl.set_interrupt_mapping(bit, pin)` |
| `adxl.isInterruptEnabled(bit)` | `adxl.is_interrupt_enabled(bit)` |
| `adxl.setInterrupt(bit, state)` | `adxl.set_interrupt(bit, state)` |
| `adxl.ActivityINT(s)`, `InactivityINT(s)` | `adxl.activity_int(s)`, `inactivity_int(s)` |
| `adxl.DataReadyINT(s)`, `WatermarkINT(s)`, `OverrunINT(s)` | `adxl.data_ready_int(s)`, `watermark_int(s)`, `overrun_int(s)` |
| `adxl.getFifoMode()`, `setFifoMode(m)` | `adxl.get_fifo_mode()`, `set_fifo_mode(m)` |
| `adxl.getFifoSamplesThreshhold()`, `setFifoSamplesThreshhold(n)` | `adxl.get_fifo_samples_threshold()`, `set_fifo_samples_threshold(n)` |
| `adxl.getFifoEntriesAmount()` | `adxl.get_fifo_entries_amount()` |
| `adxl.clearFifo()` | `adxl.clear_fifo()` |
| `adxl.updateIntSourceStatuses()` | `adxl.update_int_source_statuses()` |
| `adxl.isLowPower()`, `setLowPower(s)` | `adxl.is_low_power()`, `set_low_power(s)` |
| `adxl.lowPowerOn()`, `lowPowerOff()` | `adxl.low_power_on()`, `low_power_off()` |
| `adxl.getBandwidth()`, `setBandwidth(bw)` | `adxl.get_bandwidth()`, `set_bandwidth(bw)` |
| `adxl.lowPower` (get / set) | `adxl.is_low_power()`, `adxl.set_low_power(s)` |
| `adxl.bandwidth` (get / set) | `adxl.get_bandwidth()`, `adxl.set_bandwidth(bw)` |
| `begin()` raised `AttributeError` | `begin()` checks the part ID and returns `True` or `False` |
| `getRange()`, `isLowPower()` raised `NameError` | `get_range()`, `is_low_power()` work |
| `begin()` raised `OSError` when no device answered | `begin()` returns `False` |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
