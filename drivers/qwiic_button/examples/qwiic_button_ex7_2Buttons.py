#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_button_ex7.py
#
# Simple Example for the Qwiic Button. Daisy chain together two Qwiic Buttons 
# with different I2C addresses. This example works for a Qwiic Button with the 
# default address of 0x6F and one with an address changed to 0x5B. To change 
# the address of a Qwiic Button, please visit example 6.
#------------------------------------------------------------------------
#
# Written by Priynka Makin @ SparkFun Electronics, January 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
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
# Example 7

import qwiic_button
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 7")
    my_button1 = qwiic_button.QwiicButton()
    my_button2 = qwiic_button.QwiicButton(0x5B)

    if my_button1.begin() == False:
        print("\nThe Qwiic Button 1 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    if my_button2.begin() == False:
        print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nButton's ready!")

    while 1:

        # Check if button 1 is pressed
        if my_button1.is_button_pressed() == True:
            print("Button 1 is pressed!")
        
        # Check if button2 is pressed
        if my_button2.is_button_pressed() == True:
            print("Button 2 is pressed!")
        
        time.sleep(0.1)    # Don't hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 7")
        sys.exit(0)
