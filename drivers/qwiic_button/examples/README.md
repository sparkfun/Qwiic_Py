# SparkFun Qwiic Button Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

NOTE: The numbering of examples is to retain consistency with the Arduino library from which this was ported.

## Example 1: Button Press
`qwiic_button_ex1_button_press.py`

Checks whether the button is pressed and prints its status.

The key methods showcased by this example are:

- `is_button_pressed()`

## Example 2: LED On
`qwiic_button_ex2_led_on.py`

Turns on the button's built-in LED while the button is pressed and prints its status.

The key methods showcased by this example are:

- `led_on()`
- `led_off()`

## Example 3: LED Config
`qwiic_button_ex3_led_config.py`

Checks whether the button is pressed, and pulses the LED while it is.

The key methods showcased by this example are:

- `led_config()`

## Example 4: Queue Usage
`qwiic_button_ex4_queue_usage.py`

Shows how to use the FIFO queues of button presses and clicks on the Qwiic Button.

The key methods showcased by this example are:

- `is_pressed_queue_empty()`
- `time_since_last_press()`
- `time_since_first_press()`
- `is_clicked_queue_empty()`
- `time_since_last_click()`
- `time_since_first_click()`

## Example 5: Pop Queue
`qwiic_button_ex5_pop_queue.py`

Pops the oldest value off the pressed or clicked queue when you type `p` or `c`.

The key methods showcased by this example are:

- `pop_pressed_queue()`
- `pop_clicked_queue()`

## Example 6: Change I2C Address
`qwiic_button_ex6_change_i2c_address.py`

Shows how to change the I2C address of the Qwiic Button.

The key methods showcased by this example are:

- `set_i2c_address()`

## Example 7: Two Buttons
`qwiic_button_ex7_two_buttons.py`

Daisy chains two Qwiic Buttons with different I2C addresses. This example works with one Qwiic Button at the default address of 0x6F and one changed to 0x5B. To change the address of a Qwiic Button, see Example 6.

The key methods showcased by this example are:

- `begin()`
- `is_button_pressed()`
