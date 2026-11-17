#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_bmp581_ex5_oversampling.py
#
# This example demonstrates how to use oversampling to increase resolution and decrease noise
# in temperature and pressure measurements.
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
	print("\nQwiic Template Example 5 - Oversampling\n")

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

	# Both the temperature and pressure sensors support oversampling, where
    # multiple measurements are performed to increase resolution and decrease
    # noise. By default, no oversampling is used.
	config = qwiic_bmp581.OsrOdrPressConfig()
	config.osrT = config.kOversampling8x
	config.osrP = config.kOversampling128x

	myBMP581.set_osr_multipliers(config)

	# Larger oversampling requires longer measurement times, so ODR may need
    # to be decreased. The datasheet contains a table with max ODR values for
    # given OSR settings (Table 7). You can set the ODR with this function.
	myBMP581.set_odr_frequency(myBMP581.kOdr10Hz)
	myBMP581.get_osr_odr_eff()

	# You can also verify whether your OSR and ODR are valid with this function
	osrEff = myBMP581.get_osr_odr_eff()

	# The returned object from this function contains a flag indicating validty
	if not osrEff.odrIsValid:
		# Desired OSR and ODR are invalid, so the sensor uses different
        # effective OSR. We can print those out like so
		print("OSR and ODR are invalid!")
		print("Effective Temperature OSR: ", osrEff.osrTEff)
		print("Effective Pressure OSR: ", osrEff.osrPEff)

	while True:
		data = myBMP581.get_sensor_data()
		print("Temperature (C): ", data.temperature, end='\t\t')
		print("Pressure (Pa): ", data.pressure)

		# Only print every second
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)