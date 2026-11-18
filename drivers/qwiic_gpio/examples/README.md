# SparkFun Qwiic GPIO Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues).

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1A: Write
`qwiic_gpio_ex1a_write.py`

This example sets up GPIO 0 as an output and toggles the output HIGH and LOW. This device sinks current: when an output is LOW, current will flow.

The key methods showcased by this example are:

- `pin_mode()`
- `digital_write()`

## Example 1B: Write Port
`qwiic_gpio_ex1b_write_port.py`

This example flips all 8 outputs on and off every second.

The key methods showcased by this example are:

- `pin_mode_port()`
- `digital_write_port()`

## Example 2A: Read
`qwiic_gpio_ex2a_read.py`

This example reads a value from GPIO 0.

The key methods showcased by this example are:

- `pin_mode()`
- `digital_read()`

## Example 2B: Read Port
`qwiic_gpio_ex2b_read_port.py`

This example reads the status of all 8 GPIO simultaneously.

The key methods showcased by this example are:

- `pin_mode_port()`
- `digital_read_port()`

## Example 3A: Inversion
`qwiic_gpio_ex3a_inversion.py`

This example shows how to invert the input signal on a pin.

The key methods showcased by this example are:

- `invert_pin()`
- `digital_read()`

## Example 3B: Inversion Port
`qwiic_gpio_ex3b_inversion_port.py`

This example shows how to invert the input signal on multiple pins.

The key methods showcased by this example are:

- `invert_pin_port()`
- `digital_read_port()`
