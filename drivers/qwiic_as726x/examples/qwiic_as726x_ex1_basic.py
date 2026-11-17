#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_as726x_ex1_basic.py
#
# This example prints all measurements based on whether the device is AS7262 or AS7263
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

import qwiic_as726x
import sys

def runExample():
	print("\nQwiic AS726x Example 1 - Basic\n")

	# Create instance of device
	myAS726x = qwiic_as726x.QwiicAS726x()

	# Check if it's connected
	if myAS726x.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myAS726x.begin()

	while True:
		myAS726x.take_measurements()
		# Check which device is connected
		if myAS726x.get_version() == myAS726x.kSensorTypeAs7262:
			# Visible readings
			print(" Reading: V[{}] B[{}] G[{}] Y[{}] O[{}] R[{}]".format(
				myAS726x.get_calibrated_violet(),
				myAS726x.get_calibrated_blue(),
				myAS726x.get_calibrated_green(),
				myAS726x.get_calibrated_yellow(),
				myAS726x.get_calibrated_orange(),
				myAS726x.get_calibrated_red()
			), end="")
		
		elif myAS726x.get_version() == myAS726x.kSensorTypeAs7263:
			# Near IR readings
			print(" Reading: R[{}] S[{}] T[{}] U[{}] V[{}] W[{}]".format(
				myAS726x.get_calibrated_r(),
				myAS726x.get_calibrated_s(),
				myAS726x.get_calibrated_t(),
				myAS726x.get_calibrated_u(),
				myAS726x.get_calibrated_v(),
				myAS726x.get_calibrated_w()
			), end="")

		print(" tempF[{}]".format(myAS726x.get_temperature_f()))

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)