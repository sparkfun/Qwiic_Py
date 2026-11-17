#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_veml6030_ex2_settings.py
#
# Demonstrates how to change basic settings of the Qwiic Ambient Light Sensor
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2023
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

import qwiic_veml6030
import time
import sys

def runExample():
	print("\nQwiic Ambient Light Sensor Example 2 - Settings\n")

	# Create instance of device
	light_sensor = qwiic_veml6030.QwiicVEML6030()

	# Check if it's connected
	if light_sensor.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	light_sensor.begin()

	# Set the gain, can be any of the following:
	# 1/8, 1/4, 1, and 2
	gain = 1
	light_sensor.set_gain(gain)

	# Set the integration time in ms, can be any of the following:
	# 25, 50, 100, 200, 400, and 800
	integ_time = 200
	light_sensor.set_integ_time(integ_time)

	# Read back the settings and print to confirm they were set correctly
	gain = light_sensor.read_gain()
	integ_time = light_sensor.read_integ_time()
	print("Gain set:", gain)
	print("Integration time set:", integ_time)
	
	# Extra space for some visual separation
	print()

	# Loop forever
	while True:
		# Wait for 1 integration time period to synchronize measurements
		time.sleep(integ_time / 1000)

		# Get light measured by sensor in lux
		ambient_light = light_sensor.read_light()

		# Print measurement
		print("Lux:\t%.1f" % ambient_light)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)