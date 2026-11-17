#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_button_ex5.py
#
# Simple Example for the Qwiic Button. Shows how to use he FIFO Queue on the Qwiic Button.
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, January 2021
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
# Example 5

import qwiic_button
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 5")
    my_button = qwiic_button.QwiicButton()

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nButton ready!")

    while True:
        
        print("Type 'p' to pop a value from the pressed queue.")
        val = input("Type 'c' to pop a value from the clicked queue: ")
        # If the character is c or C, then pop a value off of the clicked queue
        if val == "c" or val == "C":
            print("Popped Clicked Queue! The first value of clicked queue was: ")
            print(str(my_button.pop_clicked_queue() / 1000.0))
        # If the character is p or P, then pop a value off of the pressed queue
        if val == "p" or val == "P":
            print("Popped Pressed Queue!")
            print(str(my_button.pop_clicked_queue() / 1000.0))

        time.sleep(0.1)    # Let's not hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 5")
        sys.exit(0)
