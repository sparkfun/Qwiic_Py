#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex2_qwiic_serlcd_backlight.py
#
# Simple Example demonstrating various backlight controls on the SerLCD (Qwiic).
#
# This sketch changes the backlight color and displays text using
# the OpenLCD functions. This works with the original version of 
# SerLCD. See FastBacklight example for version 1.1 and later.
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
# Example 2
#

import qwiic_serlcd
import time
import sys

def runExample():

	print("\nSparkFun Qwiic SerLCD   Example 2\n")
	myLCD = qwiic_serlcd.QwiicSerlcd()

	if myLCD.connected == False:
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLCD.setBacklight(255, 255, 255) # Set backlight to bright white
	myLCD.setContrast(5) # set contrast. Lower to 0 for higher contrast.

	time.sleep(1) # give a sec for system messages to complete
	
	while True:
		myLCD.setBacklight(0, 0, 0) # black is off
		myLCD.clearScreen() # Clear the display - this moves the cursor to home position as well
		myLCD.print("Black (off)")
		time.sleep(5)

		myLCD.setBacklight(255, 0, 0) # bright red
		myLCD.clearScreen()
		myLCD.print("Red")
		time.sleep(5)

		myLCD.setBacklight(0xFF, 0x8C, 0x00) # orange
		myLCD.clearScreen()
		myLCD.print("Orange")
		time.sleep(5)

		myLCD.setBacklight(255, 255, 0) # bright yellow
		myLCD.clearScreen()
		myLCD.print("Yellow")
		time.sleep(5)

		myLCD.setBacklight(0, 255, 0) # bright green
		myLCD.clearScreen()
		myLCD.print("Green")
		time.sleep(5)

		myLCD.setBacklight(0, 0, 255) # bright blue
		myLCD.clearScreen()
		myLCD.print("Blue")
		time.sleep(5)

		myLCD.setBacklight(0x4B, 0x00, 0x82) # indigo, a kind of dark purplish blue
		myLCD.clearScreen()
		myLCD.print("Indigo")
		time.sleep(5)

		myLCD.setBacklight(0xA0, 0x20, 0xF0) # violet
		myLCD.clearScreen()
		myLCD.print("Violet")
		time.sleep(5)

		myLCD.setBacklight(0x80, 0x80, 0x80) # grey
		myLCD.clearScreen()
		myLCD.print("Grey")
		time.sleep(5)

		myLCD.setBacklight(255, 255, 255) # bright white
		myLCD.clearScreen()
		myLCD.print("White")
		time.sleep(5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 2")
		sys.exit(0)


