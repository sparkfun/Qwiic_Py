#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_tmp117_ex3_set_offset_temp.py
#
# This sketch configures the TMP117 temperature sensor and allows the user to
# set the offset temperature for System Correction.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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
#===============================================================================

import qwiic_tmp117
import sys
import time

def runExample():
	print("\nQwiic TMP117 Example 3 - Set Offset Temperature Value\n")

	# Create instance of device
	myTMP117 = qwiic_tmp117.QwiicTMP117()

	# Check if it's connected
	if myTMP117.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myTMP117.begin()

	# Set the offset temperature value
	tempOffset = myTMP117.get_temperature_offset()
	print("Current Offset Temperature (in C):", tempOffset)

	while True:
		if myTMP117.data_ready():
			print("Please enter a new temperature offset between -255.98 and +255.98 (in C): ")
			tempOffset = float(input())
			if tempOffset < -255.98 or tempOffset > 255.98:
				print("Invalid temperature offset. Please enter a value between -255.98 and +255.98 (in C).")
			else:
				myTMP117.set_temperature_offset(tempOffset)
				print("New Offset Temperature (in C):", myTMP117.get_temperature_offset())
				time.sleep(1) # Wait for the offset to be set
				print("Temperature with Offset (C):", myTMP117.read_temp_c())

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)