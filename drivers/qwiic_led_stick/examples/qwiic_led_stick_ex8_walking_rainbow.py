# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex8_walking_rainbow.py
#
# This example makes a moving rainbow on the LED Stick.
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
# Example 8

import qwiic_led_stick
import math
import time
import sys

def walking_rainbow(LED_stick, rainbow_length, LED_length, delay):
    red_array = [None] * LED_length
    blue_array = [None] * LED_length
    green_array = [None] * LED_length

    for j in range(0, rainbow_length):

        for i in range(0, LED_length):
            # There are n colors generated for the rainbow
            # The value of n determins which color is generated at each pixel
            n = i + 1 - j

            # Loop n so that it is always between 1 and rainbow_length
            if n <= 0:
                n = n + rainbow_length

            # The nth color is between red and yellow
            if n <= math.floor(rainbow_length / 6):
                red_array[i] = 255
                green_array[i] = int(math.floor(6 * 255 / rainbow_length * n))
                blue_array[i] = 0
            
            # The nth color is between yellow and green
            elif n <= math.floor(rainbow_length / 3):
                red_array[i] = int(math.floor(510 - 6 * 255 / rainbow_length * n))
                green_array[i] = 255
                blue_array[i] = 0
            
            # The nth color is between green and cyan
            elif n <= math.floor(rainbow_length / 2):
                red_array[i] = 0
                green_array[i] = 255
                blue_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 510))
            
            # The nth color is between blue and magenta
            elif n <= math.floor(5 * rainbow_length / 6):
                red_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 1020))
                green_array[i] = 0
                blue_array[i] = 255
            
            # The nth color is between magenta and red
            else:
                red_array[i] = 255
                green_array[i] = 0
                blue_array[i] = int(math.floor(1530 - (6 *255 / rainbow_length * n)))

        # Set all the LEDs to the color values accordig to the arrays
        LED_stick.set_all_LED_unique_color(red_array, green_array, blue_array, LED_length)
        time.sleep(delay)

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 8")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    while True:
        walking_rainbow(my_stick, 20, 10, 0.3)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 8")
        sys.exit(0)
