#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_bmp581_ex8_low_power.py
#
# This example demonstrates how to read basic temperature and pressure values from the Qwiic BMP581
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

import qwiic_bmp581
import sys
import time

def runExample():
	print("\nQwiic Template Example 8 - Low Power\n")

	# Create instance of device
	myBMP581 = qwiic_bmp581.QwiicBMP581()

	# Check if it's connected
	if myBMP581.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	# Initialize the device
	if myBMP581.begin() == False:
		print("Unable to Initialize device! Please check your connection and try again.", file=sys.stderr)
		return
	
	print("BMP581 connected!")

	# Calling begin() puts the sensor into normal mode, but we want the sensor to
    # sleep for the majority of the time to minimize power consumption. The BMP581
    # support 2 sleep modes, namely standby (1 uA) and deep standby (0.55 uA).
    # Note - setting deep standby will affect the sensor configuration, see the
    # datasheet for more information
	myBMP581.set_power_mode(myBMP581.kPowerModeDeepStandby)

	while True:
		# Wait until next measurement. For low power applications, this could be
		# replaced by setting the microcontroller into a sleep state
		time.sleep(1)

		# Transition from sleep mode into forced mode. This will trigger a single
		# measurement, after which the sensor automatically returns to sleep mode
		# Note - the sensor can only enter forced mode from sleep mode. Transitions
		# between forced and normal modes are ignored
		myBMP581.set_power_mode(myBMP581.kPowerModeForced)

		# Wait for the measurement to complete
		time.sleep(1)

		# Get the measurements
		data = myBMP581.get_sensor_data()
		print("Temperature (C): ", data.temperature, end='\t\t')
		print("Pressure (Pa): ", data.pressure)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)