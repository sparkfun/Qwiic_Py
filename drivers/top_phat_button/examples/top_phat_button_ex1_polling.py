#!/usr/bin/env python
#-----------------------------------------------------------------------------
# top_phat_button_ex1_polling.py
#
# Polling example for the Top pHAT Buttons
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, April 2020
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
# Example 1
#

import top_phat_button
import qwiic_i2c
import sys

my_buttons = top_phat_button.TopPHATButton()


print("\nSparkFun Top pHAT Button Example 1\n")

if my_buttons.is_connected() == False:
    print("The Top pHAT Button device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    sys.exit(1)

my_buttons.set_pressed_interrupt(False)
my_buttons.set_clicked_interrupt(False)

while True:
    my_buttons.get_button_pressed() #These functions must be called to update button variables to their latest setting
    my_buttons.get_button_clicked() #These functions must be called to update button variables to their latest setting  
    if my_buttons.a_pressed == True:
        print("A Pressed")
    if my_buttons.a_clicked == True:
        print("A Released")
    if my_buttons.b_pressed == True:
        print("B Pressed")
    if my_buttons.b_clicked == True:
        print("B Released")
    if my_buttons.up_pressed == True:
        print("Up Pressed")
    if my_buttons.up_clicked == True:
        print("Up Released")
    if my_buttons.down_pressed == True:
        print("Down Pressed")
    if my_buttons.down_clicked == True:
        print("Down Released")
    if my_buttons.left_pressed == True:
        print("Left Pressed")
    if my_buttons.left_clicked == True:
        print("Left Released")
    if my_buttons.right_pressed == True:
        print("Right Pressed")
    if my_buttons.right_clicked == True:
        print("Right Released")
    if my_buttons.center_pressed == True:
        print("Center Pressed")
    if my_buttons.center_clicked == True:
        print("Center Released")

    qwiic_i2c.delay_ms(100)
