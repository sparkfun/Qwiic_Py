# SparkFun CAP1203 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

## Example 1: Basic Readings
`qwiic_cap1203_ex1_basic_readings.py`

This example demonstrates basic bringup of the CAP1203 to print which of the three touch segments is currently being touched.

The key methods showcased by this example are: 

- `is_left_touched()`
- `is_middle_touched()`
- `is_right_touched()`

## Example 2: Detect Any Touch
`qwiic_cap1203_ex2_detect_any_touch.py`

This example demonstrates how to sense if any of the three touch segments are currently touched.

The key method showcased by this example is `is_touched()`

## Example 3: Detect Swipe
`qwiic_cap1203_ex3_detect_swipe.py`

This example demonstrates how to detect a left or right swipe. It prints if either swipe event occurs. 

The key methods showcased by this example are: 

- `is_right_swipe_pulled()`
- `is_left_swipe_pulled()`

## Example 4: Power Button
`qwiic_cap1203_ex4_power_button.py`

This example shows how to set one of the 3 touch segments/pads to act as a power button. The middle button is set as the power button and then is formatted with the amount of time it must be pressed before a "power button touch" event occurs. When the middle sector is pressed, then "Power Button" will be printed.

The key methods showcased by this example are:

- `set_power_button_pad()`
- `get_power_button_pad()`
- `set_power_button_time()`
- `get_power_button_time()`
- `set_power_button_enabled()`
- `is_power_button_enabled()`
- `is_power_button_touched()`

## Example 5: Detect Current Touch
`qwiic_cap1203_ex5_detect_current_touch.py`

This example prints "Left", "Middle", or "Right" once when one of the pads is touched and then waits until the user removes their finger before printing anything else.

## Example 6: Disable Interrupt
`qwiic_cap1203_ex6_disable_interrupt.py`

This example shows how to disable interrupts on the Qwiic CAP1203. It disables the interrupt and then checks to see that the setting has taken effect.

The key methods showcased by this example are:

- `set_interrupt_disabled()`
- `is_interrupt_enabled()`

## Example 7: Set Sensitivity
`qwiic_cap1203_ex7_set_sensitivity.py`

This example demonstrates how to set the sensitivity of the Qwiic CAP1203. It first sets the sensitivity multiplier and then checks to make sure that the setting has taken effect.

The key methods showcased by this example are:

- `set_sensitivity()`
- `get_sensitivity()`
