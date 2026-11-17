# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex5_binary_counter.py
#
# This example counts up from 0 to 1023 and displays the number in binary on the 
# LED Stick.
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
# Example 5

import qwiic_led_stick
import time
import sys

def binary_LED_display(LED_stick, count, LED_length):
    # Create color arrays because we want to turn on whole string of LEDs at one time
    red_list = [0] * LED_length
    green_list = [0] * LED_length
    blue_list = [0] * LED_length
    
    # This for loop will repeat for each pixel of the LED Stick
    for i in range(0, LED_length):
        # For ith_bit, we use the bitshift operator. count >> i takes the binary
        # representation of count and shifts it to the right i times. For example, 
        # if count was 10, 0b1010, and i was 2, we get 0b10. This aligns with the 
        # ith bit of count to the 0th bit of ith_bit
        ith_bit = count >> i
        # This will resolve to the oth bit of ith_bit
        ith_bit_true = ith_bit & 0b1
        # Write the color red to the current LED if the ith_bit_true
        # LED_stick.set_single_LED_color(10 - i, 255 * ith_bit_true, 0, 0)
        red_list[LED_length - i - 1] = 255 * ith_bit_true
    
    LED_stick.set_all_LED_unique_color(red_list, green_list, blue_list, LED_length)

def binary_serial_display(count, bit_length):
    print(str(count) + "\t" + str(bin(count)))

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 5")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")
    
    # Reset the state of LEDs
    my_stick.LED_off()

    while True:
        # This loop counts from 0 to 1023 and displays the binary over the 
        # serial port and the LED stick
        for i in range(0, 1024):
            binary_LED_display(my_stick, i, 10)
            binary_serial_display(i, 10)
            time.sleep(1)
    
if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 5")
        sys.exit(0)
