#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cy8cmbr3_ex6_set_range.py
#
# Shows how to set up and use the Qwiic CY8CMBR3 Capacitive Soil Moisture Sensor
# for reading of raw counts with range setting options.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, January 2026
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2026 SparkFun Electronics
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

from random import choice
import qwiic_cy8cmbr3
import sys
import time

def runExample():
	print("\nQwiic Template Example 6 - Set Range\n")

	# Create instance of device
	mySoilSensor = qwiic_cy8cmbr3.QwiicCY8CMBR3()

	# Check if it's connected
	if mySoilSensor.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	mySoilSensor.begin()

	# Capacitance PF is great, easy to use, and standard/objective accross all soil types, densities, and conditions.
	# However, it has limited resolution (1 count / pF) and range (0-255pF). Depending on your application, you may want to use
	# raw counts instead for higher resolution and range.

	# The sensor will automatically configure the range of its "Raw Count" Readings based on 
	# the capacitance that it senses during power up/initialization. This allows it to maximize
	# resolution for the expected capacitance range. However, if the capacitance changes significantly
	# (for example, a moisture sensor going from dry to very wet), the raw count readings may saturate
	# and get stuck at a maximum value. You can run reset() again to reconfigure the raw count range if needed.

	# The range setting is volatile (it will be reset when power is removed from the sensor or the sensor is reset) 

	prompting = True
	autoRangeSet = False

	# Infinite loop reading data
	while True:
		for i in range (5):
			# Read and print the soil capacitance
			# "raw" counts is what we're setting the range of, capacitance pF behaves the same regardless of range setting
			capacitance = mySoilSensor.get_capacitance_pf()
			print("Soil Capacitance: " + str(capacitance) + " pF")

			# We can pass a boolean "True" value to get_raw_count() to have the sensor
			# automatically adjust the raw count range if it detects saturation.

			# Don't touch the active part of the sensor (the bottom with the ruler) while auto-range setting is enabled
			# Or it will configure to a very high capacitance value, 
			# and auto-range setting will be ineffective until a manual reconfiguration is done.
			raw_counts = mySoilSensor.get_raw_count(autoRangeSet)
			print("Soil Raw Counts: " + str(raw_counts) + " counts\n")

			if mySoilSensor.check_saturation(raw_counts):
				print("WARNING: Raw counts are saturated! Consider recalibrating the sensor to adjust the range.\n")
			
			# Sleep for a second to avoid spamming the output
			time.sleep(1)
		if prompting:
			choice = input(
				"\nSelect one of the following:\n"
				"1) Manually Reconfigure Range\n"
				"2) Continue for 5 more readings with current range setting\n"
				"3) Turn on auto-range setting (Don't touch the sensor while this is enabled)\n"
				"4) Turn off auto-range setting\n"
				"5) Do not prompt again\n"
				"6) Exit\n\n"
				"Enter choice (1, 2, 3, 4, 5, or 6): "
			)
			if choice == '1':
				input("Place the sensor in the wettest possible state (i.e. soil fully saturated) and press Enter to reconfigure the range...")
				print("Reconfiguring sensor range...")
				mySoilSensor.reset()
				print("Range reconfiguration complete.")
			elif choice == '2':
				continue
			elif choice == '3':
				autoRangeSet = True
				print("Auto-range setting enabled.")
			elif choice == '4':
				autoRangeSet = False
				print("Auto-range setting disabled.")
			elif choice == '5':
				prompting = False
				print("Prompting disabled.")
			elif choice == '6':
				print("Exiting example.")
				return
			else:
				print("Invalid choice. Continuing with current range setting.")

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)