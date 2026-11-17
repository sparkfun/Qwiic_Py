#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp9600_ex3_set_filter.py
#
#   This example outputs the ambient and thermocouple temperatures from the MCP9600 sensor, but allows the filtering
#   onboard the MCP9600 to be controlled. The MCP9600 implements an exponential running average filter, the
#   "strength" of which is programmable! The setFilterCoefficient function takes a coefficient between 0 and 7, 
#   where 0 disables the filter, 1 corresponds to minimum filtering, and 7 enables maximum filtering. The "strength"
#   of the filter just refers to how long it takes for the filter to respond to a step function input. 

#   Quick Note! For some reason the getFilterCoefficient() function is a little wierd about returning the proper
#   data. This is a known issue and while we've done our best to fix it, every once in a while it might return a 0,
#   or the wrong value entirely. We think this is an issue with the MCP9600, and there's not much we can do about it.
#   If you'd like to learn more or contact us, check out this issue on GitHub!

#   https://github.com/sparkfun/SparkFun_MCP9600_Arduino_Library/issues/1
# 
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

import qwiic_mcp9600
import sys
import time 

# Change the coefficient here!
coefficient = 3

def runExample():

	print("\nQwiic MCP9600 Example 3 - Set Filter\n")

	# Create instance of device
	myThermo = qwiic_mcp9600.QwiicMCP9600()

	# Check if it's connected
	if myThermo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myThermo.begin()
	
	# Print the filter coefficient that's about to be set
	print(f"Setting Filter coefficient to {coefficient}!")

	myThermo.set_filter_coefficient(coefficient)

	# Tell us if the coefficient was set successfully
	if myThermo.get_filter_coefficient() == coefficient:
		print("Filter Coefficient set successfully!")
	else:
		print("Setting filter coefficient failed!")
		print(f"The value of the coefficient is: {myThermo.get_filter_coefficient()}")

	while True:
		if myThermo.available():
			# Read temperatures
			thermocouple_temp = myThermo.get_thermocouple_temp()
			ambient_temp = myThermo.get_ambient_temp()
			temp_delta = myThermo.get_temp_delta()
			filter_coef = myThermo.get_filter_coefficient()

			# Print temperatures
			print(f"Thermocouple: {thermocouple_temp}C   Ambient: {ambient_temp}C   Temperature Delta: {temp_delta}C Filter Coefficient: {filter_coef}")
			
		# Delay to avoid hammering the I2C bus
		time.sleep(0.02)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)