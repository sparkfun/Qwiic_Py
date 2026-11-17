# Sparkfun LED_STICK Examples Reference
Below is a brief summary of each of the example programs included in this repository. To report a bug in any of these examples or to request a new feature or example [submit an issue in our GitHub issues.](https://github.com/sparkfun/qwiic_led_stick_py/issues). 

NOTE: Any numbering of examples is to retain consistency with the Arduino library from which this was ported. 

## Qwiic Led Stick Ex1 Blink
This example blinks the entire LED stick.

The key methods showcased by this example are:
- [set_all_LED_brightness()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#a0e8a29f5752bdf7cc651c551ba24cc3f)
- [set_all_LED_color()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#ac8bcdb7c6ca8e632b674bf585847929b)
- [LED_off()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#a918f81caf123e4be60a571163de1ad89)

## Qwiic Led Stick Ex2 Single Pixel
This example will alternate blinking two single LEDs on the LED Stick.
- [set_single_LED_color()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#aa625b99d7e8745105b18826886e0b374)

## Qwiic Led Stick Ex3 Single Pixel2
This example changes each LED of the LED Stick to an arbitrary color.

The key methods showcased by this example are:
- [set_all_LED_unique_color()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#aa427d38d1fb2e1e5fabc2ec5757b0f39)

## Qwiic Led Stick Ex4 Set Brightness
This example changes brightness of the LED Stick in different ways, then stops 
 through each available brightness setting.

The key methods showcased by this example are:
- [set_all_LED_brightness()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#a0e8a29f5752bdf7cc651c551ba24cc3f)

## Qwiic Led Stick Ex5 Binary Counter
This example counts up from 0 to 1023 and displays the number in binary on the 
 LED Stick.
 

## Qwiic Led Stick Ex6 Color Gradient
This example will display a linear gradient from one color to another on the LED
 Stick.

## Qwiic Led Stick Ex7 Cycle Rainbow
This example ake the LED Stick smoothly change through the colors of the rainbow.

## Qwiic Led Stick Ex8 Walking Rainbow
This example makes a moving rainbow on the LED Stick.

## Qwiic Led Stick Ex9 Change Length
This example changes the length of the attached LED strip and shows the results 
 by writing the whole strip white. Length will not reset on restart, change back
 to 10 if necessary with my_stick.change_length(10);
 If you add LEDs to the end of the sitck, you must change the length to be able to
 use them.

The key methods showcased by this example are:
- [change_length()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#aa8e99783231d2c08b155ca6eb73236e9)

## Qwiic Led Stick Ex10 Change Address
This example changes the address of the LED stick and shows the results by writing
 the whole strip white. Address will not reset on restart. Change the address back 
 to default with my_stick.change_address(0x23).

The key methods showcased by this example are:
- [change_address()](https://docs.sparkfun.com/qwiic_led_stick_py/classqwiic__led__stick_1_1_qwiic_l_e_d_stick.html#af1261865746ea71ee1eaf92f17781311)

## Qwiic Led Stick Ex11 2 Led Sticks
This example shows how to use two LED Sticks on the same I2C bus.
