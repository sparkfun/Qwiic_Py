#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mmc5983ma_ex3_compass.py
#
# Demonstrates how to use the MMC5983MA Magnetometer as a compass
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
import math

def runExample():
	print("\nQwiic MMC5983MA Example 3 - Compass\n")

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
		# Read only the x and y axes, z is assumeed to be pointing straight up
		x = my_mag.get_measurement_x_gauss()
		y = my_mag.get_measurement_y_gauss()

		# Compute heading, assuming the y-axis is the "forward" direction.
		#
		# Note - atan2 usually takes (y, x), but we have to account for a couple
		# things. The Earth's south pole is actually a  magnetic north pole, so
		# the field lines run from south to north, meaning we need to negate the
		# x and y values. Additionally, because the y-axis is the "forward"
		# direction, so we need to swap the x and y values and negate the x
		# value again to effectively rotate the coordinate system 90 degrees.
		heading = math.atan2(x, -y)

		# Convert to degrees
		heading = math.degrees(heading)

		# Change range from -180 to 180 to 0 to 360
		if heading < 0:
			heading = 360 + heading

		# Print compass heading
		#
		# Note - If the Earth's magnetic field points mostly straight up or down
		# where you live, this may be inaccurate!
		print("Heading:", heading)

		# Delay for a moment
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)