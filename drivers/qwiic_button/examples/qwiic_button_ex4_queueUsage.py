#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_button_ex4.py
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
# Example 4

import qwiic_button
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 4")
    my_button = qwiic_button.QwiicButton()

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nButton ready!")

    while True:
            
        # If the queue of pressed events is not empty
        if my_button.is_pressed_queue_empty() == False:
            # Then print the time since the last and first button press
            print(str(my_button.time_since_last_press() / 1000.0) + "s since he button was last pressed   ")
            print(str(my_button.time_since_first_press() / 1000.0) +"s since the button was first pressed ")
        # If the queue is empty
        else: 
            print("Button Pressed Queue is empty! ")

        # If the queue of clicked events is not empty
        if my_button.is_clicked_queue_empty() == False:
            # Then print the time since the last and first button click
            print(str(my_button.time_since_last_click() / 1000.0) + "s since the button was last clicked  ")
            print(str(my_button.time_since_first_click() / 1000.0) + "s since the button was first clicked")
        # If the queue is empty
        else:
            print("Button Clicked Queue is empty!")

        # Add some visual separation
        print()

        time.sleep(0.1)    # Let's not hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 4")
        sys.exit(0)
