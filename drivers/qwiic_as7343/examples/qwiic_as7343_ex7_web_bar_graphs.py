#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_as7343_ex7_web_bar_graphs.py
#
# This example shows how to setup the AS7343 sensor with the SparkFun Web Serial
# Bar Graphs Demo. It will print out the spectral data from the sensor in a format
# that can be read by the web terminal and displayed as bar graphs.

# Find the web terminal demo code here:
# https://github.com/sparkfun/SparkFun_WebSerialPlotter
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, May 2024
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

import qwiic_as7343 
import sys
import time

def runExample():
	print("\nQwiic AS7343 Example 7 - Web Terminal Bar Graphs\n")

	# Create instance of device
	myAS7343 = qwiic_as7343.QwiicAS7343()

	# Check if it's connected
	if myAS7343.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	if not myAS7343.begin():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	
	# Power on the device
	myAS7343.power_on()
	print("Device powered on")

	# Set AutoSmux to output all 18 channels
	if not myAS7343.set_auto_smux(myAS7343.kAutoSmux18Channels):
		print("Failed to set AutoSmux", file=sys.stderr)
		return
	print("AutoSmux set to 18 channels")

	# Enable spectral measurements
	if not myAS7343.spectral_measurement_enable():
		print("Failed to enable spectral measurements", file=sys.stderr)
		return
	print("Spectral measurements enabled")

	while True:
		myAS7343.set_led_drive(0) # 0 = 4mA
		myAS7343.set_led_on()

		time.sleep(0.100) # Wait 100 ms for LED to fully illuminate our target
		
		# Read the spectral data
		myAS7343.read_all_spectral_data()

		myAS7343.set_led_off()

		# Print our comma-separated spectral data in the format expected by the web terminal
		print(f"{myAS7343.get_data(myAS7343.kChPurpleF1405nm)},"
			  f"{myAS7343.get_data(myAS7343.kChDarkBlueF2425nm)},"
			  f"{myAS7343.get_data(myAS7343.kChBlueFz450nm)},"
			  f"{myAS7343.get_data(myAS7343.kChLightBlueF3475nm)},"
			  f"{myAS7343.get_data(myAS7343.kChBlueF4515nm)},"
			  f"{myAS7343.get_data(myAS7343.kChGreenF5550nm)},"
			  f"{myAS7343.get_data(myAS7343.kChGreenFy555nm)},"
			  f"{myAS7343.get_data(myAS7343.kChOrangeFxl600nm)},"
			  f"{myAS7343.get_data(myAS7343.kChBrownF6640nm)},"
			  f"{myAS7343.get_data(myAS7343.kChRedF7690nm)},"
			  f"{myAS7343.get_data(myAS7343.kChDarkRedF8745nm)},"
			  f"{myAS7343.get_data(myAS7343.kChVis1)},"
			  f"{myAS7343.get_data(myAS7343.kChNir855nm)}\n", end='')

		time.sleep(0.500) # Wait 500 ms before next reading

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)