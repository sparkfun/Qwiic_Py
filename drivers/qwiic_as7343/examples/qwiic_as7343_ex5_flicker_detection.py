#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_as7343_ex5_flicker_detection.py
#
# This example shows how to use the Flicker Detection feature of the AS7343 sensor.
# It sets up the sensor with default settings and prints out the flicker detection
# results to the serial monitor.
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
	print("\nQwiic AS7343 Example 5 - Flicker Detection\n")

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

	myAS7343.flicker_detection_enable()

	# Enable spectral measurements
	if not myAS7343.spectral_measurement_enable():
		print("Failed to enable spectral measurements", file=sys.stderr)
		return
	print("Spectral measurements enabled")

	# Turn off the LED for use with flicker detection
	myAS7343.set_led_off()
	time.sleep(1) # Wait 1 second for the sensor to stabilize

	while True:
		fdValid = myAS7343.get_fd_valid_status()
		fdSaturation = myAS7343.get_fd_saturation_status()
		fdFrequency = myAS7343.get_fd_frequency()

		# Check if the measurement is valid
		if not fdValid:
			print("Flicker detection measurement is not valid")
			return
		
		# Check if the measurement is saturated
		if fdSaturation:
			print("Flicker detection measurement is saturated")
			return
		
		# If the measurement is valid and not saturated, print the frequency
		if fdFrequency == 0:
			print("No flicker detected")
		else:
			print("Flicker detected at frequency: {} Hz".format(fdFrequency))

		time.sleep(1) # Wait before the next reading

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)