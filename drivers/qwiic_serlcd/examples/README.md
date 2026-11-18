# Sparkfun SerLCD Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [file an issue in our GitHub issues.](https://github.com/sparkfun/Qwiic_Py/issues)

## Example 1: Hello World
`qwiic_serlcd_ex1_hello_world.py`

This example demonstrates basic bringup of the LCD to print "Hello World!".

It showcases the following methods: 

- `set_backlight()`
- `set_contrast()`
- `clear_screen()`
- `print()`
- `set_cursor()`


## Example 2: Backlight
`qwiic_serlcd_ex2_backlight.py`

This example shows how to change the color of the backlight by cycling through backlight colors and printing the name of the current backlight color to the display. 

The key method showcased by this example is `set_backlight()`

## Example 3: Set Cursor Position
`qwiic_serlcd_ex3_set_cursor_position.py`

This example shows how to set the cursor to a specific column and row to print a character. It cycles through the lowercase letters of the alphabet (a-z) and prints each to a random row and column of the display.

The key method showcased by this example is `set_cursor()`

## Example 4: Move Cursor
`qwiic_serlcd_ex4_move_cursor.py`

This example shows how to manually move the cursor left or right. It cycles between moving the cursor left three spaces and then moving it right three spaces. 

The key methods showcased by this example are `move_cursor_left()` and `move_cursor_right()`

## Example 5: Enable Cursor
`qwiic_serlcd_ex5_enable_cursor.py`

This example shows how to turn the cursor on and off. It prints "Hello World!" to the LCD and then cycles between turning the cursor on for a second and off for a second.

The key methods showcased by this example are `cursor()` and `no_cursor()`

## Example 6: Blink Cursor
`qwiic_serlcd_ex6_blink_cursor.py`

This example shows how to turn blinking of the cursor on and off. It prints "Hello World!" to the LCD and then cycles between turning the blinking on for 5 seconds and off for 5 seconds.

The key methods showcased by this example are `blink()` and `no_blink()`

## Example 7: Scroll
`qwiic_serlcd_ex7_scroll.py`

This example demonstrates the scrolling controls on the SerLCD. It prints "Hello World!" to the LCD and then cycles between scrolling it offscreen to the left, then offscreen to the right before finally centering it again.

The key methods showcased by this example are `scroll_display_left()` and `scroll_display_right()`

## Example 8: Autoscroll Text
`qwiic_serlcd_ex8_autoscroll_with_text.py`

This example demonstrates the autoscroll feature on the SerLCD. It cycles between printing the characters 0 to 9 and turning on and off autoscroll.

The key methods showcased by this example are:

- `left_to_right()`
- `autoscroll()`
- `no_autoscroll()`


## Example 9: Custom Character
`qwiic_serlcd_ex9_custom_character.py`

This example demonstrates how to print custom characters to the LCD. It demonstrates printing a heart and a smiley face and then a little man waving his arms up and down.

The key methods showcased by this example are `create_char()` and `write_char()`

## Example 10: Turn off Display
`qwiic_serlcd_ex10_turn_off_display.py`

This example prints "Hello World!" to the LCD and turns on and off
the display for a second each.

The key methods showcased by this example are `display()` and `no_display()`

## Example 11: Text Direction
`qwiic_serlcd_ex11_text_direction.py`

This example demonstrates how to change where the next character will be printed. It walks through the alphabet and cycles between printing characters from right to left then left to right. 

The key methods showcased by this example are `right_to_left()`, `left_to_right()` and `home()`.

## Example 12: Console Input to Display
`qwiic_serlcd_ex12_console_input_to_display.py`

This example demonstrates printing arbitrary strings to the LCD. It takes user input from the Python repl until the user presses "enter" and then prints it to the LCD.

The key method showcased by this example is `print()`


## Example 13: Fast Backlight
`qwiic_serlcd_ex13_fast_backlight.py`

This example shows how to set the backlight fast. It is advantageous because using this method doesn't show any system messages and sends the values in one concatenated block of data (a single command for all 3 values). It alternates between turning the backlight red for a second an then orange for a second.

The key method showcased by this example is `set_fast_backlight()`

## Example 14: Show Firmware Version
`qwiic_serlcd_ex14_show_firmware_version.py`

This example shows how to get the devices firmware version. It repeatedly sends the command to display the firmware version.

The key method showcased by this example is `command()`

## Example 15: Message Enable
`qwiic_serlcd_ex15_message_enable.py`

This example demonstrates how to turn off the system messages displayed when
the user changes a setting. For instance 'Contrast: 5' or 'Backlight: 100%' is
no longer displayed. It first sets the backlight and contrast while system messages are enabled, and then disables them and repeatedly changes the backlight color to demonstrate that the system messages are no longer printed.

The key method showcased by this example is `disable_system_messages()`

## Example 16: Set Splash
`qwiic_serlcd_ex16_set_splash.py`

This example demonstrates how to create your own custom splash screen.

This is done by first writing the text you want as your splash to the display,
then 'saving' it as a splash screen.

You can also disable or enable the displaying of the splash screen.

Note - The disable_splash() and enable_splash() commands  
are only supported on SerLCD v1.2 and above. But you can still use the
toggle splash command (Ctrl+i) to enable/disable the splash.

The example sets the custom splash screen to "Tea-O-Matic".

The key methods showcased by this example are `save_splash()` and `enable_splash()`

## Example 17: Change I2C Address
`qwiic_serlcd_ex17_change_i2c_address.py`

This example demonstrates how to change the I2C address on your LCD. 

The key method showcased by this example is `set_address()`
