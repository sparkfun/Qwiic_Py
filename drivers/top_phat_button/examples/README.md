# SparkFun Top pHAT Button Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

## Example 1: Polling
`top_phat_button_ex1_polling.py`

Turns off the button interrupts, then polls the buttons every 100 ms and prints each press and release.

The key methods showcased by this example are:

- `set_pressed_interrupt()`
- `set_clicked_interrupt()`
- `get_button_pressed()`
- `get_button_clicked()`

## Example 2: Interrupt
`top_phat_button_ex2_interrupt.py`

Turns on the button interrupts and prints each press and release when the Top pHAT's interrupt pin (GPIO 25) goes low. This example runs on a Raspberry Pi only, because it reads the pin with `RPi.GPIO`.

The key methods showcased by this example are:

- `set_pressed_interrupt()`
- `set_clicked_interrupt()`
- `get_button_pressed()`
- `get_button_clicked()`
