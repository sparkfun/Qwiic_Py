# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_alphanumeric_ex6_colon_and_decimal .py
#
# This example tests the library's response to printing colons or decimal points.
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
# Example 6

import qwiic_alphanumeric
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Alphanumeric - Example 6: Colon and Decimal")
    my_display = qwiic_alphanumeric.QwiicAlphanumeric()

    if my_display.begin() == False:
        print("\nThe Qwiic Alphanumeric isn't connected to the system. Please check your connections.", \
            file=sys.stderr)
        return
    
    print("\nQwiic Alphanumeric ready!")

    # You can print colons and decimals
    # NOTE: they can only go in the character position deterined by the layout of the display
    my_display.print("12:3.4")
    
    # You can also turn decimals and colon on and off manually
    # my_display.decimal_on() # Turn all decimals on  
    # my_display.decimal_off()    # Turn all decimals off
    # my_display.decimal_on_single(1) # Turn decimal on for display one
    # my_display.decimal_off_single(1)    # Turn decimal off for display one
    # my_display.colon_on()  # Turn all colons on
    # my_display.colon_off()  # Turn all the colons off
    # my_display.colon_on_single(1)   # Turn colon on for display one
    # my_display.colon_off_single(1)  # Turn colon off for display one

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 6")
        sys.exit(0)
