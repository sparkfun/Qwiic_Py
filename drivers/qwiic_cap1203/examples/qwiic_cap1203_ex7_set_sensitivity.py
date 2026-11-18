#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cap1203_ex7_set_sensitivity.py
#
# Demonstrates how to set sensitivity of the Qwiic CAP1203
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2023
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

import qwiic_cap1203
import sys

def run_example():
	print("\nQwiic CAP1203 Example 7 - Set Sensitivity\n")

	# Create instance of device
	my_device = qwiic_cap1203.QwiicCAP1203()

	# Check if it's connected
	if my_device.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_device.begin()

	# Set the sensitivity multiplier for different applications,
	# such as different sized touch pads. The default sensitivity 
	# multiplier is set to 2x.
	#
	# Different sensitivity settings:
	# SENSITIVITY_128X  # Most sensitive
	# SENSITIVITY_64X
	# SENSITIVITY_32X
	# SENSITIVITY_16X
	# SENSITIVITY_8X
	# SENSITIVITY_4X
	# SENSITIVITY_2X
	# SENSITIVITY_1X    # Least sensitive
	my_device.set_sensitivity(my_device.SENSITIVITY_4X)

	# Returns the sensitivity multiplier for the
	# current sensitivity settings.
	print("Sensitivity Multiplier:", my_device.get_sensitivity(), "x")

	while True:
		if my_device.is_touched():
			print("Touch")
			while my_device.is_touched():
				pass

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example")
		sys.exit(0)