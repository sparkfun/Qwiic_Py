#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_tmp117_ex4_set_conv_mode.py
#
# This script can get and set the conversion mode to
# Continuous Conversion, Shutdown, or One-Shot
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

def conv_mode_to_string(mode):
	if mode == qwiic_tmp117.QwiicTMP117.kContinuousConversionMode:
		return "Continuous Conversion Mode"
	elif mode == qwiic_tmp117.QwiicTMP117.kShutdownMode:
		return "Shutdown Mode"
	elif mode == qwiic_tmp117.QwiicTMP117.kOneShotMode:
		return "One-Shot Mode"
	else:
		return "Invalid Conversion Mode"

def runExample():
	print("\nQwiic TMP117 Example 4 - Set Conversion Mode\n")

	# Create instance of device
	myTMP117 = qwiic_tmp117.QwiicTMP117()

	# Check if it's connected
	if myTMP117.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myTMP117.begin()

	print("Conversion Modes: ")
	print("1: Continuous Conversion Mode")
	print("2: Shutdown Mode")
	print("3: One-Shot Mode")

	currentMode = myTMP117.get_conversion_mode()
	print("Current Mode:", conv_mode_to_string(currentMode))

	while True:
		print("Please Enter a Conversion Mode from above (number 1-3): ")
		newMode = int(input())
		if newMode == 1:
			myTMP117.set_continuous_conversion_mode()
		elif newMode == 2:
			myTMP117.set_shutdown_mode()
		elif newMode == 3:
			myTMP117.set_one_shot_mode()
		else:
			print("Invalid Conversion Mode (must be a number between 1-3)")
			continue
		
		print("New Conversion Mode:", conv_mode_to_string(myTMP117.get_conversion_mode()))

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)