#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_serlcd_ex6_blink_cursor.py
#
# Simple example demonstrating the blinking cursor controls on the SerLCD (Qwiic).
#
# This example prints "Hello World!" to the LCD and
# uses the blink()  and noBlink() methods to turn
# on and off the blinking.
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
# Example 6
#

import qwiic_serlcd
import qwiic_i2c
import sys


print("\nSparkFun Qwiic SerLCD   Example 6\n")
myLCD = qwiic_serlcd.QwiicSerLCD()

if not myLCD.is_connected():
	print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

myLCD.set_backlight(255, 255, 255) # Set backlight to bright white
myLCD.set_contrast(5) # set contrast. Lower to 0 for higher contrast.
myLCD.clear_screen()
myLCD.cursor() # Turn on the underline cursor

qwiic_i2c.delay_ms(1000) # give a sec for system messages to complete
myLCD.print("Hello World!")

while True:
	# turn off the blinking cursor
	print("Cursor blinking OFF")
	myLCD.no_blink()
	qwiic_i2c.delay_ms(5000)

	# turn on the blinking cursor
	print("Cursor blinking ON")
	myLCD.blink()
	qwiic_i2c.delay_ms(5000)
