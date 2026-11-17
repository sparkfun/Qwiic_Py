# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex3_set_brightness.py
#
# This example changes brightness of the LED Stick in different ways, then stops 
# through each available brightness setting.
# --------------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# 
# This python library supports the SpakrFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatible) board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 4

import qwiic_led_stick
import time
import sys

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 3")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    # Initialize LEDs as a rainbow followed by 1 white pixel
    red_list = [255, 255, 170, 0, 0, 0, 0, 170, 255, 255]
    green_list = [0, 170, 255, 255, 255, 170, 0, 0, 0, 255]
    blue_list = [0, 0, 0, 0, 170, 255, 255, 255, 170, 255]

    # Turn on the LED Stick according to the 3 arrays
    my_stick.set_all_LED_unique_color(red_list, green_list, blue_list, 10)

    while True:

        # This will step through each available brightness setting
        # Brightness values can be from 0 - 31
        for i in range(0, 32):
            my_stick.set_all_LED_brightness(i)

            print("\nBrightness level: " + str(i))
            time.sleep(1)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 4")
        sys.exit(0)
