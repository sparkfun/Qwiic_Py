# Sparkfun CAP1203 Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_cap1203_py/issues). 

## Example 1: Basic Readings
This example demonstrates basic bringup of the CAP1203 to print which of the three touch segments is currently being touched.

The key methods showcased by this example are: 

- [is_left_touched()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a7a1307b3e8b0cd900eb776475c039fba)
- [is_middle_touched()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a068039889d14e252847fe4c54ae87200)
- [is_right_touched()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a6768f8409a08208e4508991a4ef5e333)

## Example 2: Detect Any Touch
This example demonstrates how to sense if any of the three touch segments are currently touched.

The key method showcased by this example is [is_touched()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a729adf5df541b199c7188934c1d7640c)

## Example 3: Detect Swipe
This example demonstrates how to detect a left or right swipe. It prints if either swipe event occurs. 

The key methods showcased by this example are: 

- [is_right_swipe_pulled()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#aab739fa0e1f9e8d8b33b28d5953abc86)
- [is_left_swipe_pulled()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#af751cc20ac0497ca202c1dc6b8294cf2)

## Example 4: Power Button
This example shows how to set one of the 3 touch segments/pads to act as a power button. The middle button is set as the power button and then is formatted with the amount of time it must be pressed before a "power button touch" event occurs. When the middle sector is pressed, then "Power Button" will be printed.

The key methods showcased by this example are:

- [set_power_button_pad()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#ad87fe518392f9298e6088320493547a3)
- [get_power_button_pad()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#afcb8e20b14eb298b93268dc1e34868ce)
- [set_power_button_time()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#aa1a664fa2c81f3e52c445dcd44f7166b)
- [get_power_button_time()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a4514a98453e1dad81f2dc746b35b1002)
- [set_power_button_enabled()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#af27e9985bb3b2d4244ee2d829fdb4f6d)
- [is_power_button_enabled()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a0d91de909e5517344fce97fa0490914d)
- [is_power_button_touched()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a760ab74de0de685b00aafd465ddca067)

## Example 5: Detect Current Touch
This example prints "Left", "Middle", or "Right" once when one of the pads is touched and then waits until the user removes their finger before printing anything else.

## Example 6: Disable Interrupt
This example shows how to disable interrupts on the Qwiic CAP1203. It disables the interrupt and then checks to see that the setting has taken effect.

The key methods showcased by this example are:

- [set_interrupt_disabled()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a7e9cb8d56cde66c78d93d15361548b09)
- [is_interrupt_enabled()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#a70b5f0e935bb28cc9c93c16e171f0011)

## Example 7: Set Sensitivity
This example demonstrates how to set the sensitivity of the Qwiic CAP1203. It first sets the sensitivity multiplier and then checks to make sure that the setting has taken effect.

The key methods showcased by this example are:

- [set_sensitivity()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#aacfe116ef2504f14665a68beb0cf73b9)
- [get_sensitivity()](https://docs.sparkfun.com/qwiic_cap1203_py/classqwiic__cap1203_1_1_qwiic_c_a_p1203.html#ae8d71b450ad20b0e28a9b78f703aa737)
