#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex3_qwiic_serlcd_set_cursor_position.py
#
# Simple Example demonstrating cursor posistion controls on the SerLCD (Qwiic).
#
# This sketch randomly picks a cursor position, goes to
# that position using the setCursor() method, and prints a character
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
# Example 3
#

import qwiic_serlcd
import time
import sys
import random


def runExample():

	print("\nSparkFun Qwiic SerLCD   Example 3\n")
	myLCD = qwiic_serlcd.QwiicSerlcd()

	if myLCD.connected == False:
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLCD.setBacklight(255, 255, 255) # Set backlight to bright white
	myLCD.setContrast(5) # set contrast. Lower to 0 for higher contrast.
	myLCD.clearScreen()

	time.sleep(1) # give a sec for system messages to complete

	# These constants won't change. But you can change the size of
	# your LCD using them:
	numRows = 2
	# numRows = 4
	numCols = 16
	# numCols = 20

	thisLetter = "a"
	
	while True:
		randomColumn = random.randint(0, numCols)
		randomRow = random.randint(0, numRows)

		# set the cursor position:
		myLCD.setCursor(randomColumn, randomRow)

		# print the letter:
		myLCD.print(thisLetter) # print to screen
		time.sleep(0.2)

		thisLetter = chr(ord(thisLetter) + 1)
		if thisLetter > "z":
			thisLetter = "a" # Wrap the variable

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


