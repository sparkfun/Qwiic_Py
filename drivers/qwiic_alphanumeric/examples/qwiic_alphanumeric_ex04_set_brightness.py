# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_alphanumeric_ex4_set_brightness.py
#
# This example sets the brightness of the Qwiic Alphanumeric display.
# ----------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, September 2021
#
# This python library supports the SparkFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatable) single board 
# computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
# ======================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================
# Example 4

import qwiic_alphanumeric
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Alphanumeric - Example 4: Set Brightness")
    my_display = qwiic_alphanumeric.QwiicAlphanumeric()

    if my_display.begin() == False:
        print("\nThe Qwiic Alphanumeric isn't connected to the system. Please check your wiring.", \
            file=sys.stderr)
        return

    print("\nQwiic Alphanumeric Ready!")
    
    my_display.print("Milk")
    
    # Repeat a few times
    for i in range(4):
        # Loop through all brightness settings
        for i in range(0, 16):
            # The input to set_brightness() is a duty cycle over 16
            # So, the acceptable inputs to this function are ints between 0
            # (1/16 brightness) and 15 (full brightness)
            my_display.set_brightness(i)
            time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 4")
        sys.exit(0)
