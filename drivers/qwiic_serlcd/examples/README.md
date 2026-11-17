# Sparkfun SerLCD Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [file an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_serlcd_py/issues)

## Example 1: Hello World
This example demonstrates basic bringup of the LCD to print "Hello World!".

It showcases the following methods: 

- [setBacklight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a81afb76ad0cc0b03b2def16c29ceaf06)
- [setContrast()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a2dea2487f84df67519f61ff3004c7d12)
- [clearScreen()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a35e73e1105f1db0be89372a5f4500714)
- [print()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a30a4a9383c96b81763c6a32fa8b3f8dc)
- [setCursor()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#ab62f2dd063749b4418373f3320f2a38a)


## Example 2: Backlight
This example shows how to change the color of the backlight by cycling through backlight colors and printing the name of the current backlight color to the display. 

The key method showcased by this example is [setBacklight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a81afb76ad0cc0b03b2def16c29ceaf06)

## Example 3: Set Cursor Position
This example shows how to set the cursor to a specific column and row to print a character. It cycles through the lowercase letters of the alphabet (a-z) and prints each to a random row and column of the display.

The key method showcased by this example is [setCursor()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#ab62f2dd063749b4418373f3320f2a38a)

## Example 4: Move Cursor
This example shows how to manually move the cursor left or right. It cycles between moving the cursor left three spaces and then moving it right three spaces. 

The key methods showcased by this example are [moveCursorLeft()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#ac6dda0410878a153b193b05d4eeb62ee) and [moveCursorRight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a7d8891c7fb78d2e684c7cdf38556b813)

## Example 5: Enable Cursor
This example shows how to turn the cursor on and off. It prints "Hello World!" to the LCD and then cycles between turning the cursor on for a second and off for a second.

The key methods showcased by this example are [cursor()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#ab11b11f6eaca0dd22e7c14b816e10bed) and [noCursor()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#abafa73de35582185e9db2c74f91df116)

## Example 6: Blink Cursor
This example shows how to turn blinking of the cursor on and off. It prints "Hello World!" to the LCD and then cycles between turning the blinking on for 5 seconds and off for 5 seconds.

The key methods showcased by this example are [blink()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a4c92d4fa2a89bbda03bcca43d82cd95a) and [noBlink()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#aae22aaee6f6d748c2921fc7b3008014b)

## Example 7: Scroll
This example demonstrates the scrolling controls on the SerLCD. It prints "Hello World!" to the LCD and then cycles between scrolling it offscreen to the left, then offscreen to the right before finally centering it again.

The key methods showcased by this example are [scrollDisplayLeft()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a5770a90358b2bad368e67aa23f8d0148) and [scrollDisplayRight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#abcb7784572d86a1ca3beec4b73481a6f)

## Example 8: Autoscroll Text
This example demonstrates the autoscroll feature on the SerLCD. It cycles between printing the characters 0 to 9 and turning on and off autoscroll.

The key methods showcased by this example are:

- [leftToRight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a3a1c4c6cf831084a78f09fb535fb69fc)
- [autoScroll()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a1ed67c384ab25e363e8129bc4d5c37e8)
- [noAutoScroll()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#abbbd2c0c047d37f88209b6dd27a34359)


## Example 9: Custom Character
This example demonstrates how to print custom characters to the LCD. It demonstrates printing a heart and a smiley face and then a little man waving his arms up and down.

The key methods showcased by this example are [createChar()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#af75050abc733dd3ada34e79bd9a3b21b) and [writeChar()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a1b7e9f17fd0f061eef860416ce846783)

## Example 10: Turn off Display
This example prints "Hello World!" to the LCD and turns on and off
the display for a second each.

The key methods showcased by this example are [display()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#acef2bfe9d6a0b2629150f0d18bf6849d) and [noDisplay()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#ae5db2e051be1530b742aacef0b4ccd3f)

## Example 11: Text Direction
This example demonstrates how to change where the next character will be printed. It walks through the alphabet and cycles between printing characters from right to left then left to right. 

The key methods showcased by this example are [rightToLeft()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#add5f1d9c4796f5f73d8944eb1e825575), [leftToRight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a3a1c4c6cf831084a78f09fb535fb69fc) and [home()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a26bb593af77460f92a2dc1791096c294).

## Example 12: Console Input to Display
This example demonstrates printing arbitrary strings to the LCD. It takes user input from the Python repl until the user presses "enter" and then prints it to the LCD.

The key method showcased by this example is [print()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a30a4a9383c96b81763c6a32fa8b3f8dc)


## Example 13: Fast Backlight
This example shows how to set the backlight fast. It is advantageous because using this method doesn't show any system messages and sends the values in one concatenated block of data (a single command for all 3 values). It alternates between turning the backlight red for a second an then orange for a second.

The key method showcased by this example is [setFastBacklight()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#afbc44537d3f324299f6a94433e338ef1)

## Example 14: Show Firmware Version
This example shows how to get the devices firmware version. It repeatedly sends the command to display the firmware version.

The key method showcased by this example is [command()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#aed9378ca8da9030c62fe29ac96513cf4)

## Example 15: Message Enable
This example demonstrates how to turn off the system messages displayed when
the user changes a setting. For instance 'Contrast: 5' or 'Backlight: 100%' is
no longer displayed. It first sets the backlight and contrast while system messages are enabled, and then disables them and repeatedly changes the backlight color to demonstrate that the system messages are no longer printed.

The key method showcased by this example is [disableSystemMessages()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a748362f1dfd4a4af65a19e1c07c6fbca)

## Example 16: Set Splash
This example demonstrates how to create your own custom splash screen.

This is done by first writing the text you want as your splash to the display,
then 'saving' it as a splash screen.

You can also disable or enable the displaying of the splash screen.

Note - The disableSplash() and enableSplash() commands  
are only supported on SerLCD v1.2 and above. But you can still use the
toggle splash command (Ctrl+i) to enable/disable the splash.

The example sets the custom splash screen to "Tea-O-Matic".

The key methods showcased by this example are [saveSplash()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#ae80dc2c1c37bd22f8aba75336ea9cedb) and [enableSplash()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a4783eaf3f021b51e0c8b877d64742063)

## Example 17: Change I2C Address
This example demonstrates how to change the I2C address on your LCD. 

The key method showcased by this example is [setAddress()](https://docs.sparkfun.com/qwiic_serlcd_py/classqwiic__serlcd_1_1_qwiic_serlcd.html#a4783eaf3f021b51e0c8b877d64742063)