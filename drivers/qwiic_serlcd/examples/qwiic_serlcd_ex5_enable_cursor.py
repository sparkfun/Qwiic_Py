#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_serlcd_ex5_enable_cursor.py
#
# Simple Example demonstrating the enable and disable cursor controls on the SerLCD (Qwiic).
#
# This example prints "Hello World!" to the LCD and
# uses the cursor()  and noCursor() methods to turn
# on and off the cursor.
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
# Example 5
#

import qwiic_serlcd
import qwiic_i2c
import sys

def run_example():

	print("\nSparkFun Qwiic SerLCD   Example 5\n")
	myLCD = qwiic_serlcd.QwiicSerLCD()

	if not myLCD.is_connected():
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLCD.set_backlight(255, 255, 255) # Set backlight to bright white
	myLCD.set_contrast(5) # set contrast. Lower to 0 for higher contrast.
	myLCD.clear_screen()
	myLCD.cursor() # Turn on the underline cursor

	qwiic_i2c.delay_ms(1000) # give a sec for system messages to complete
	myLCD.print("Hello World!")
	
	while True:
		# turn off the cursor
		print("Cursor OFF")
		myLCD.no_cursor()
		qwiic_i2c.delay_ms(1000)
		
		# turn on the cursor
		print("Cursor ON")

		myLCD.cursor()
		qwiic_i2c.delay_ms(1000)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 5")
		sys.exit(0)


