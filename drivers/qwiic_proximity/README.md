![Qwiic Proximity Python Package](https://cdn.sparkfun.com//assets/parts/1/3/5/9/2/15177-SparkFun_Proximity_Sensor_Breakout_-_20cm__VCNL4040__Qwiic_-01.jpg "Qwiic Proximity Python Package")

# SparkFun Qwiic Proximity - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-qwiic-proximity)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/qwiic_proximity/)

The SparkFun Proximity Sensor Breakout uses the VCNL4040 to sense proximity up to 20 cm, ambient light and white light. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This package is a port of the [SparkFun VCNL4040 Proximity Sensor Arduino Library](https://github.com/sparkfun/SparkFun_VCNL4040_Arduino_Library).

This package is the Python driver for the VCNL4040 proximity sensor. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads proximity, ambient light and white light from the VCNL4040 over a single Qwiic cable, and configures its IR LED, integration times, resolution, thresholds and interrupts. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Proximity Sensor Breakout - 20cm, VCNL4040 (Qwiic)](https://www.sparkfun.com/products/15177)

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
~/sparkfun_venv/bin/pip install sparkfun-qwiic-proximity
```

Run any example or script that does `import qwiic_proximity` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/qwiic_proximity
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/qwiic_proximity/examples
```

Add `@qwiic_proximity-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install qwiic_proximity
```

To copy an example to the board:

```sh
circup example qwiic_proximity/qwiic_proximity_ex1_basic_readings
```

## Example Use

Below is a quickstart program that prints the proximity value. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import qwiic_proximity
import qwiic_i2c


def run_example():
    print("\nSparkFun Proximity Sensor VCN4040 Example 1\n")
    prox = qwiic_proximity.QwiicProximity()

    if not prox.is_connected():
        print("The Qwiic Proximity device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    prox.begin()

    while True:
        print("Proximity Value: %d" % prox.get_proximity())
        qwiic_i2c.delay_ms(400)


if __name__ == "__main__":
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example 1")
        sys.exit(0)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/qwiic_proximity](https://docs.sparkfun.com/Qwiic_Py/qwiic_proximity/).

## Migrating from 2.x

Version 3 has one name per method and no properties, so it also runs on MicroPython builds without `property()`.

| 2.x | 3.0 |
| --- | --- |
| `sensor.connected` | `sensor.is_connected()` |
| `sensor.proximity`, `sensor.ambient`, `sensor.white_light`, `sensor.sensor_id` | `sensor.get_proximity()`, `sensor.get_ambient()`, `sensor.get_white()`, `sensor.get_id()` |
| `sensor.is_close`, `sensor.is_away`, `sensor.is_light`, `sensor.is_dark` (properties) | `sensor.is_close()`, `sensor.is_away()`, `sensor.is_light()`, `sensor.is_dark()` |
| `sensor.duty_cycle = v` | `sensor.set_ir_dutycycle(v)` |
| `sensor.led_current = v` | `sensor.set_led_current(v)` |
| `sensor.ambient_integration_time = v`, `sensor.prox_integration_time = v` | `sensor.set_ambient_integration_time(v)`, `sensor.set_prox_integration_time(v)` |
| `sensor.prox_resolution = v`, `sensor.prox_interrupt_type = v` | `sensor.set_prox_resolution(v)`, `sensor.set_prox_interrupt_type(v)` |
| `sensor.prox_cancellation = v` | `sensor.set_prox_cancellation(v)` |
| `sensor.als_high_threshold = v`, `sensor.als_low_threshold = v` | `sensor.set_als_high_threshold(v)`, `sensor.set_als_low_threshold(v)` |
| `sensor.prox_high_threshold = v`, `sensor.prox_low_threshold = v` | `sensor.set_prox_high_threshold(v)`, `sensor.set_prox_low_threshold(v)` |
| `sensor.prox_interrupt_persistance = v`, `set_prox_interrupt_persistance(v)` | `sensor.set_prox_interrupt_persistence(v)` |
| `sensor.ambient_interrupt_persistance = v`, `set_ambient_interrupt_persistance(v)` | `sensor.set_ambient_interrupt_persistence(v)` |
| `enable_smart_persistance()`, `disable_smart_persistance()` | `enable_smart_persistence()`, `disable_smart_persistence()` |
| Setter arguments `dutyValue`, `persValue`, `timeValue`, `resolutionValue`, `interruptValue`, `currentValue`, `cancelValue` | `duty_value`, `pers_value`, `time_value`, `resolution_value`, `interrupt_value`, `current_value`, `cancel_value` |
| `disable_white_channel()` enabled the white channel | `disable_white_channel()` disables it |
| `is_connected()` used the default bus even when an `i2c_driver` was given | `is_connected()` uses the driver's own bus |
| `take_single_prox_measurement()` also turned active force mode off (wrong bit mask) | it sets only the trigger bit |
| `enable_smart_persistence()` set a reserved bit, so it had no effect | it sets the smart persistence bit |
| Linux only (Raspberry Pi, Jetson, Coral) | CPython, MicroPython and CircuitPython |
| `set_ambient_integration_time(160)` set 320 ms and `(320)` set 160 ms | each sets the time asked for |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
