#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp9600_ex1_basic.py
#
# This example outputs the ambient and thermocouple temperatures from the MCP9600 sensor.
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

def runExample():

	print("\nQwiic MCP9600 Example 1 - Basic Readings\n")

	# Create instance of device
	myThermo = qwiic_mcp9600.QwiicMCP9600()

	# Check if it's connected
	if myThermo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myThermo.begin()

	while True:
		if myThermo.available():
			# Read temperatures
			thermocouple_temp = myThermo.get_thermocouple_temp()
			ambient_temp = myThermo.get_ambient_temp()
			temp_delta = myThermo.get_temp_delta()

			# Print temperatures
			print(f"Thermocouple: {thermocouple_temp}C   Ambient: {ambient_temp}C   Temperature Delta: {temp_delta}C")
			
		# Delay to avoid hammering the I2C bus
		time.sleep(0.02)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)