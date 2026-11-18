# SparkFun Top pHAT Button - Python Package

![PyPI Version](https://img.shields.io/pypi/v/sparkfun-top-phat-button)
![License](https://img.shields.io/badge/license-MIT-blue)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/Qwiic_Py/top_phat_button/)

The SparkFun Top pHAT for Raspberry Pi has a 5-way joystick and A and B buttons, read by an ATtiny84 button controller on its I2C bus. Its firmware is in the [SparkFun Top pHAT repository](https://github.com/sparkfun/Top_pHat).

This package is the Python driver for the Top pHAT buttons. It works on CPython (Linux), MicroPython and CircuitPython, and is part of the [SparkFun Qwiic Python package](https://github.com/sparkfun/Qwiic_Py).

## Contents

* [About the Package](#about-the-package)
* [Supported Platforms](#supported-platforms)
* [Installation](#installation)
* [Example Use](#example-use)
* [Documentation](#documentation)
* [Migrating from 2.x](#migrating-from-2x)

## About the Package

This package reads which buttons are pressed and which have been clicked (pressed and released), and turns the pressed and clicked interrupts on and off. Each feature is demonstrated in the [examples](examples/README.md).

New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

* [SparkFun Top pHAT for Raspberry Pi](https://www.sparkfun.com/products/16301)

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
~/sparkfun_venv/bin/pip install sparkfun-top-phat-button
```

Run any example or script that does `import top_phat_button` with `~/sparkfun_venv/bin/python3 example_script.py`.

### MicroPython (mip)

Install [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), connect your board, then install the driver (this also installs `qwiic_i2c`):

```sh
mpremote mip install github:sparkfun/Qwiic_Py/drivers/top_phat_button
```

To install the examples too:

```sh
mpremote mip install --target "" github:sparkfun/Qwiic_Py/drivers/top_phat_button/examples
```

Add `@top_phat_button-<version>` to either command to install a specific release.

### CircuitPython (circup)

Install [CircUp](https://docs.circuitpython.org/projects/circup/en/latest/#installation), add the SparkFun Qwiic bundle once, then install the driver:

```sh
circup bundle-add sparkfun/Qwiic_Py
circup install top_phat_button
```

To copy an example to the board:

```sh
circup example top_phat_button/top_phat_button_ex1_polling
```

## Example Use

Below is a quickstart program that prints when the A or center button is pressed or released. See the [examples directory](examples) for more, and [examples/README.md](examples/README.md) for a summary of each.

```python
import sys
import top_phat_button
import qwiic_i2c


print("\nSparkFun Top pHAT Button Example 1\n")
my_buttons = top_phat_button.TopPHATButton()

if not my_buttons.is_connected():
    print("The Top pHAT Button device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(1)

my_buttons.set_pressed_interrupt(False)
my_buttons.set_clicked_interrupt(False)

while True:
    # Update the button variables (a_pressed, a_clicked, ...)
    my_buttons.get_button_pressed()
    my_buttons.get_button_clicked()
    if my_buttons.a_pressed:
        print("A Pressed")
    if my_buttons.a_clicked:
        print("A Released")
    if my_buttons.center_pressed:
        print("Center Pressed")
    if my_buttons.center_clicked:
        print("Center Released")
    qwiic_i2c.delay_ms(100)
```

## Documentation

The API reference is at [docs.sparkfun.com/Qwiic_Py/top_phat_button](https://docs.sparkfun.com/Qwiic_Py/top_phat_button/).

## Migrating from 2.x

Version 3 has one name per method and no properties, so it also runs on MicroPython builds without `property()`. Version 2.x of this driver ran only on Linux; version 3 also runs on MicroPython and CircuitPython.

| 2.x | 3.0 |
| --- | --- |
| `ToppHATButton` | `TopPHATButton` |
| `buttons.connected` | `buttons.is_connected()` |
| `buttons.button_pressed`, `buttons.button_clicked` | `buttons.get_button_pressed()`, `buttons.get_button_clicked()` |
| `buttons.version` | `buttons.get_version()` |
| `buttons.pressed_interrupt_enable` (get / set) | `buttons.get_pressed_interrupt()`, `buttons.set_pressed_interrupt(enable)` |
| `buttons.clicked_interrupt_enable` (get / set) | `buttons.get_clicked_interrupt()`, `buttons.set_clicked_interrupt(enable)` |
| `top_phat_button.BUTTON_CHANGE_ADDREESS` | `top_phat_button.BUTTON_CHANGE_ADDRESS` |
| `get_version()` returned minor.major | `get_version()` returns major.minor |
| `set_pressed_interrupt()`, `set_clicked_interrupt()` also cleared the low byte of the debounce time | they write only the interrupt register |

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
