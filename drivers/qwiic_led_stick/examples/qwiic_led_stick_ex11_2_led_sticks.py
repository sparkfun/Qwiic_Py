# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex11_2_led_sticks.py
#
# This example shows how to use two LED Sticks on the same I2C bus.
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
# Example 11

import qwiic_led_stick
import time
import sys

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 11")
    my_stick1 = qwiic_led_stick.QwiicLEDStick()
    my_stick2 = qwiic_led_stick.QwiicLEDStick(0x29)

    if my_stick1.begin() == False:
        print("\nThe Qwiic LED Stick 1 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick 1 ready!")

    if my_stick2.begin() == False:
        print("\nThe Qwiic LED Stick 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick 2 ready!")

    # Set all of LED Stick 1 to white
    my_stick1.set_all_LED_color(10, 10, 10)
    # Set all of LED Stick 2 to red
    my_stick2.set_all_LED_color(255, 0, 0)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 11")
        sys.exit(0)
