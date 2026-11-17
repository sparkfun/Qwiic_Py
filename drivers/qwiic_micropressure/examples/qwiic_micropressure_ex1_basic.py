#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_micropressure_ex1_basic.py 
# 
# Basic test of the Qwiic MicroPressure Sensor
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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

import qwiic_micropressure
import sys
import time

def runExample():
	print("\nQwiic MicroPressure Example 1 - Basic Readings\n")

	# Create instance of device
	myMicroPressure = qwiic_micropressure.QwiicMicroPressure()

	# Check if it's connected
	if myMicroPressure.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myMicroPressure.begin()

	while True:
		# The micropressure sensor outputs pressure readings in pounds per square inch (PSI).
		#  Optionally, if you prefer pressure in another unit, the library can convert the
		#  pressure reading to: pascals, kilopascals, bar, torr, inches of murcury, and
		#  atmospheres.

		# Get the pressure
		print("Pressure(PSI): ", myMicroPressure.read_pressure())
		print("Pressure(Pa): ", myMicroPressure.read_pressure(myMicroPressure.kPressurePa))
		print("Pressure(kPa): ", myMicroPressure.read_pressure(myMicroPressure.kPressureKpa))
		print("Pressure(Torr): ", myMicroPressure.read_pressure(myMicroPressure.kPressureTorr))
		print("Pressure(InHg): ", myMicroPressure.read_pressure(myMicroPressure.kPressureInHg))
		print("Pressure(Atm): ", myMicroPressure.read_pressure(myMicroPressure.kPressureAtm))
		print("Pressure(Bar): ", myMicroPressure.read_pressure(myMicroPressure.kPressureBar))

		# Wait a bit before reading again
		time.sleep(0.500)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)