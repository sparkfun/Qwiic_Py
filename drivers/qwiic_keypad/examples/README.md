# Sparkfun Qwiic Keypad Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

## Example 1: Basic Readings
`qwiic_keypad_ex1_basic_readings.py`

This example demonstrates basic bringup of the Qwiic Keypad to print which button was pressed or a space if '*' is pressed and a newline if '#' is pressed

The key methods showcased by this example are:

- `update_fifo()`
- `get_button()`
    
## Example 2: Button Press Time
`qwiic_keypad_ex2_button_press_time.py`

This example prints which button was pressed as well as the time of how long ago it was pressed.

The key method showcased by this example is `time_since_pressed()`

## Example 3: Keycode
`qwiic_keypad_ex3_keycode.py`

This example waits for the user to input the correct 4 digit keycode and responds with a nice message on serial if they get it right. It demonstrates how to ignore startup noise and then check user input against a stored keycode.
