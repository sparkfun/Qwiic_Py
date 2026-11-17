# !/usr/bin/env python
# ---------------------------------------------------------------------------------
# qwiic_led_stick_ex9_change_length.py
#
# This example changes the length of the attached LED strip and shows the results 
# by writing the whole strip white. Length will not reset on restart, change back
# to 10 if necessary with my_stick.change_length(10);
# If you add LEDs to the end of the sitck, you must change the length to be able to
# use them.
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
# Example 9

import qwiic_led_stick
import time
import sys

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 9")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")
    
    # First, turn all LEDs off
    my_stick.LED_off()
    # Give stick time to turn all LEDs off
    time.sleep(0.5)
    
    # Change LED length to 5
    # This will allow you to write to a maximum of 5 LEDs
    my_stick.change_length(5)
    # Set all LEDs to dim white, notice only 5 are lit.
    my_stick.set_all_LED_color(10, 10, 10)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
