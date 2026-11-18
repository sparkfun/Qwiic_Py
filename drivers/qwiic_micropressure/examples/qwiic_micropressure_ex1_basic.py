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
import qwiic_i2c
def run_example():
	print("\nQwiic MicroPressure Example 1 - Basic Readings\n")

	# Create instance of device
	my_micro_pressure = qwiic_micropressure.QwiicMicroPressure()

	# Check if it's connected
	if not my_micro_pressure.is_connected():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_micro_pressure.begin()

	while True:
		# The micropressure sensor outputs pressure readings in pounds per square inch (PSI).
		#  Optionally, if you prefer pressure in another unit, the library can convert the
		#  pressure reading to: pascals, kilopascals, bar, torr, inches of murcury, and
		#  atmospheres.

		# Get the pressure
		print("Pressure(PSI): ", my_micro_pressure.read_pressure())
		print("Pressure(Pa): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_PA))
		print("Pressure(kPa): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_KPA))
		print("Pressure(Torr): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_TORR))
		print("Pressure(InHg): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_INHG))
		print("Pressure(Atm): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_ATM))
		print("Pressure(Bar): ", my_micro_pressure.read_pressure(my_micro_pressure.PRESSURE_BAR))

		# Wait a bit before reading again
		qwiic_i2c.delay_ms(500)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example 1")
		sys.exit(0)