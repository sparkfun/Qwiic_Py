#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_nau7802_ex2_complete_scale.py
#
# Demonstrates how to calibrate the Qwiic Scale to measure weight
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2023
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
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

import qwiic_nau7802
import sys

def runExample():
	print("\nQwiic NAU7802 Example 2 - Complete Scale\n")

	# Create instance of device
	my_scale = qwiic_nau7802.QwiicNAU7802()

	# Check if it's connected
	if my_scale.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_scale.begin()

	# Ask user for automatic or manual calibration
	print("Would you like to automatically calibrate? Enter 'Y' for yes, or anything else to manually enter calibration values.")
	user_input = input()

	if user_input == 'Y':
		print("Automatic calibration!")
		
		print("Set up scale with no weight on it. Enter anything when ready")
		input()

		# Calculate zero offset averaged over 64 readings
		my_scale.calculate_zero_offset(64)

		print("Now place a known weight on the scale. When it's stable, enter the weight without units")
		user_input = input()
		weight = float(user_input)

		# Calculate calibration factor averaged over 64 readings
		my_scale.calculate_calibration_factor(weight, 64)

		print("Calibration complete! Here are your calibration values:")
		print("Zero offset:", my_scale.get_zero_offset())
		print("Calibration factor:", my_scale.get_calibration_factor())
		
		print("Enter anything when ready to continue")
		input()
	else:
		print("Manual calibration!")

		print("Enter zero offset")
		user_input = input()
		zero_offset = int(user_input)
		my_scale.set_zero_offset(zero_offset)

		print("Enter calibration factor")
		user_input = input()
		calibration_factor = float(user_input)
		my_scale.set_calibration_factor(calibration_factor)

	# Loop forever
	while True:
		# Check if data is available
		if my_scale.available():
			# Print measurement
			print("Weight:", my_scale.get_weight())

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)