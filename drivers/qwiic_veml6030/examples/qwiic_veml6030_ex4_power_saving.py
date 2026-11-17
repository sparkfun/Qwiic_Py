#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_veml6030_ex4_power_saving.py
#
# Demonstrates how to set power saving mode of the Qwiic Ambient Light Sensor
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
	print("\nQwiic Ambient Light Sensor Example 4 - Power Saving\n")

	# Create instance of device
	light_sensor = qwiic_veml6030.QwiicVEML6030()

	# Check if it's connected
	if light_sensor.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	light_sensor.begin()

	# The datsheet has a table on page 9 listing the tpical current consumption
	# with various settings. The settings below are for the minimum current
	# consumption of 2uA. Note that this alo result in the longest refresh time
	# of 4.1s, so there's a tradeoff between current and measurement time
	gain = 2
	integ_time = 100
	power_mode = 4
	light_sensor.set_gain(gain)
	light_sensor.set_integ_time(integ_time)
	light_sensor.set_pow_sav_mode(power_mode)

	# Enable power saving mode
	light_sensor.enable_pow_save()

	# Read back the settings and print to confirm they were set correctly
	power_mode = light_sensor.read_pow_sav_mode()
	power_save_enabled = light_sensor.read_pow_sav_enabled()
	print("Power save mode:", power_mode)
	print("Power save enabled:", power_save_enabled)
	
	# Extra space for some visual separation
	print()

	# Loop forever
	while True:
		# Wait for the refresh time specified in page 9 of the datasheet
		time.sleep(4.1)

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