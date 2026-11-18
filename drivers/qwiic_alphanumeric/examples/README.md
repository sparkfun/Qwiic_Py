# Sparkfun Alphanumeric Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Example 1: Print String
`qwiic_alphanumeric_ex1_print_string.py`

This example shows how to use the print() function to illuminate strings
on the alphanumeric display.

The key methods showcased by this example are: 

- `print()`

## Example 2: Turn On One Segment
`qwiic_alphanumeric_ex2_turn_on_one_segment.py`

This example tests illuminating individual segments of the display. Pass
in the segment and digit you wish to illuminate into illuminate_segment().

The key methods showcased by this example are: 

- `illuminate_segment()`
- `update_display()`

## Example 3: Print Char
`qwiic_alphanumeric_ex3_print_char.py`

This example tests illuminating a whole character on the 14-segment display.

The key methods showcased by this example are: 

- `print_char()`

## Example 4: Set Brightness
`qwiic_alphanumeric_ex4_set_brightness.py`

This example sets the brightness of the Qwiic Alphanumeric display.

The key methods showcased by this example are: 

- `set_brightness()`

## Example 5: Set Blink Rate
`qwiic_alphanumeric_ex5_set_blink_rate.py`

This example sets the blink rate of the display.

The key methods showcased by this example are: 

- `set_blink_rate()`

## Example 6: Colon and Decimal
`qwiic_alphanumeric_ex6_colon_and_decimal.py`

This example tests the library's response to printing colons or decimal points.
The commented-out lines show `decimal_on()`, `decimal_off()`, `colon_on()`,
`colon_off()` and their `_single()` versions.

## Example 7: Unknown Char
`qwiic_alphanumeric_ex7_unknown_char.py`

This example demonstrates what the library does when the user tries to 
print an unknown character.

## Example 8: Multi Display
`qwiic_alphanumeric_ex8_multi_display.py`

This example demonstrates how to connect multiple displays to the bus
to print longer strings.

The key methods showcased by this example are: 

- `begin()` with the address of each display
- `print()`

## Example 9: Scrolling String
`qwiic_alphanumeric_ex9_scrolling_string.py`

This example tests the scrolling functionality of the display.

The key methods showcased by this example are: 

- `shift_left()`
