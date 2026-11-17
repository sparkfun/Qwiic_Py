#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mmc5983ma_ex1_basic_readings.py
#
# Demonstrates how to get basic data from the MMC5983MA Magnetometer
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

import qwiic_mmc5983ma
import sys
import time

def runExample():
	print("\nQwiic MMC5983MA Example 1 - Basic Readings\n")

	# Create instance of device
	my_mag = qwiic_mmc5983ma.QwiicMMC5983MA()

	# Check if it's connected
	if my_mag.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_mag.begin()

	# Loop forever
	while True:
		# Read each axis one by one, or all together
		# x = my_mag.get_measurement_x_gauss()
		# y = my_mag.get_measurement_y_gauss()
		# z = my_mag.get_measurement_z_gauss()
		x, y, z = my_mag.get_measurement_xyz_gauss()

		# Print them out
		print("X: %f" % x)
		print("Y: %f" % y)
		print("Z: %f" % z)

		# Extra space to keep numbers separate
		print()

		# Delay for a moment
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)