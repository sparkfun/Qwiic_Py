# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex6_color_gradient.py
#
# This example will display a linear gradient from one color to another on the LED
# Stick.
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
# Example 6

import qwiic_led_stick
import time
import sys

def color_gradient(LED_stick, r1, b1, g1, r2, g2, b2, LED_length):
    # Subtract 1 from LED_length because there is one less transition color
    # than length of LEDs
    LED_length = LED_length - 1
    # Calculate the slope of the line between r/g/b1 and r/g/b2
    r_slope = (r2 - r1) / LED_length
    g_slope = (g2 - g1) / LED_length
    b_slope = (b2 - b1) / LED_length
    # Set the color for each pixel on your LED Stick
    for i in range(0, LED_length):
        # Evaluate the ith point on the line between r/g/b1 and r/g/b2
        r_value = r1 + r_slope * i
        g_value = g1 + g_slope * i
        b_value = b1 + b_slope * i
        # Set the pixel to the calculated color
        LED_stick.set_single_LED_color(i + 1, r_value, g_value, b_value)

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 6")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    # Set the colors for the gradient
    # These are for the first color
    r1 =238
    g1 = 49
    b1 = 36
    # These are for the last color    
    r2 = 66
    g2 = 235
    b2 = 23

    color_gradient(my_stick, r1, g1, b1, r2, g2, b2, 10)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 6")
        sys.exit(0)