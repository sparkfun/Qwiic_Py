# Sparkfun Qwiic Keypad Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_keypad_py/issues). 

## Example 1: Basic Readings
This example demonstrates basic bringup of the Qwiic Keypad to print which button was pressed or a space if '*' is pressed and a newline if '#' is pressed

The key methods showcased by this example are:
- [update_fifo()](https://docs.sparkfun.com/qwiic_keypad_py/classqwiic__keypad_1_1_qwiic_keypad.html#a9029aec36abfb17315cf2747f43a33c1)
- [get_button()](https://docs.sparkfun.com/qwiic_keypad_py/classqwiic__keypad_1_1_qwiic_keypad.html#a2803d3a99b6f92befb6a6459be6c65cf)
    
## Example 2: Button Press Time
This example prints which button was pressed as well as the time of how long ago it was pressed.

The key method showcased by this example is [time_since_pressed()](https://docs.sparkfun.com/qwiic_keypad_py/classqwiic__keypad_1_1_qwiic_keypad.html#a58e82d1c12a242f7dfdcb57232365185)

## Example 3: 
This example waits for the user to input the correct 4 digit keycode and responds with a nice message on serial if they get it right. It demonstrates how to ignore startup noise and then check user input against a stored keycode.