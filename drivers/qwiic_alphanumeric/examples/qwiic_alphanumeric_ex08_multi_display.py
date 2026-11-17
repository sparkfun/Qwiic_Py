# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_alphanumeric_ex8_multi_display.py
#
# This example demonstrates how to connect multiple displays to the bus
# to print longer strings.
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
# Example 8

import qwiic_alphanumeric
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Alphanumeric - Example 8: Multi Display")
    my_display = qwiic_alphanumeric.QwiicAlphanumeric()

    if my_display.begin(0x70, 0x71) == False:
        print("\nThe Qwiic Alhanumerics aren't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nQwiic Alphanumerics ready!")

    my_display.print("Get Milk")

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 8")
        sys.exit(0)
