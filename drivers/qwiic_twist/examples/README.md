# Sparkfun Twist Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Basic Readings
`qwiic_twist_ex1_basic_readings.py`

Simple Example for the Qwiic Twist Device that displays count and pressed status.

The key methods showcased by this example are:

- `get_count()`
- `is_pressed()`

## Example 2: Crazy Color
`qwiic_twist_ex2_crazy_color.py`

Simple Example for the Qwiic Twist Device with random colors.

The key methods showcased by this example are:

- `set_color()`

## Example 3: Connect Colors
`qwiic_twist_ex3_connect_colors.py`

Simple Example for the Qwiic Twist Device that changes the knob color as it turns: red goes down and blue goes up with each encoder tick.

The key methods showcased by this example are:

- `set_connect_red()`
- `set_connect_blue()`
