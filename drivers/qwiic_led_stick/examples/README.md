# Sparkfun LED Stick Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Blink
`qwiic_led_stick_ex1_blink.py`

This example blinks the entire LED stick.

The key methods showcased by this example are:

- `set_all_led_brightness()`
- `set_all_led_color()`
- `led_off()`

## Example 2: Single Pixel
`qwiic_led_stick_ex2_single_pixel.py`

This example will alternate blinking two single LEDs on the LED Stick.

The key methods showcased by this example are:

- `set_single_led_color()`

## Example 3: Single Pixel 2
`qwiic_led_stick_ex3_single_pixel2.py`

This example changes each LED of the LED Stick to an arbitrary color.

The key methods showcased by this example are:

- `set_all_led_unique_color()`

## Example 4: Set Brightness
`qwiic_led_stick_ex4_set_brightness.py`

This example changes brightness of the LED Stick in different ways, then steps
through each available brightness setting.

The key methods showcased by this example are:

- `set_all_led_brightness()`

## Example 5: Binary Counter
`qwiic_led_stick_ex5_binary_counter.py`

This example counts up from 0 to 1023 and displays the number in binary on the 
LED Stick.

## Example 6: Color Gradient
`qwiic_led_stick_ex6_color_gradient.py`

This example will display a linear gradient from one color to another on the LED
Stick.

## Example 7: Cycle Rainbow
`qwiic_led_stick_ex7_cycle_rainbow.py`

This example makes the LED Stick smoothly change through the colors of the rainbow.

## Example 8: Walking Rainbow
`qwiic_led_stick_ex8_walking_rainbow.py`

This example makes a moving rainbow on the LED Stick.

## Example 9: Change Length
`qwiic_led_stick_ex9_change_length.py`

This example changes the length of the attached LED strip and shows the results 
by writing the whole strip white. Length will not reset on restart, change back
to 10 if necessary with `my_stick.change_length(10)`.
If you add LEDs to the end of the stick, you must change the length to be able to
use them.

The key methods showcased by this example are:

- `change_length()`

## Example 10: Change Address
`qwiic_led_stick_ex10_change_address.py`

This example changes the address of the LED stick and shows the results by writing
the whole strip white. Address will not reset on restart. Change the address back 
to default with `my_stick.change_address(0x23)`.

The key methods showcased by this example are:

- `change_address()`

## Example 11: Two LED Sticks
`qwiic_led_stick_ex11_2_led_sticks.py`

This example shows how to use two LED Sticks on the same I2C bus.
