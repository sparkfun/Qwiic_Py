#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_serlcd_ex8_autoscroll_with_text.py
#
# Simple example demonstrating the autoscroll feature on the SerLCD (Qwiic).
#
# This example demonstrates the use of the autoscroll()
# and noAutoscroll() functions to make new text scroll or not.
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, August 2020
#
# Ported from Arduino Library code with many contributions from
# Gaston Williams - August 29, 2018
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
# Copyright (c) 2020 SparkFun Electronics
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
# Example 8
#

import qwiic_serlcd
import qwiic_i2c
import sys


print("\nSparkFun Qwiic SerLCD   Example 8\n")
myLCD = qwiic_serlcd.QwiicSerLCD()

if not myLCD.is_connected():
	print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

myLCD.set_backlight(255, 255, 255) # Set backlight to bright white
myLCD.set_contrast(5) # set contrast. Lower to 0 for higher contrast.
myLCD.begin() # call this for default settings (no
myLCD.left_to_right()
qwiic_i2c.delay_ms(1000) # give a sec for system messages to complete

while True:
	myLCD.set_cursor(0, 0) # set the cursor to (0,0)

	for thisChar in range(10): # print from 0 to 9
		myLCD.print(str(thisChar))
		qwiic_i2c.delay_ms(500)

	myLCD.autoscroll() # set the display to automatically scroll

	for thisChar in range(0,10): # print from 0 to 9
		myLCD.set_cursor(10+thisChar,1)
		myLCD.print(str(thisChar))
		qwiic_i2c.delay_ms(500)

	myLCD.no_autoscroll() # turn off automatic scrolling	
	myLCD.clear_screen() # clear screen for the next loop
