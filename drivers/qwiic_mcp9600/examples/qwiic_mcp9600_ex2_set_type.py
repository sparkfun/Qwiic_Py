#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp9600_ex2_set_type.py
#
#   This example outputs the ambient and thermocouple temperatures from the MCP9600 sensor, but allows for a non
#   K-type thermocouple to be used.
#   The Qwiic MCP9600 supports K/J/T/N/S/E/B/R type thermocouples, and the type can be configured below!
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

# Change the type of the thermocouple here!
therm_type = qwiic_mcp9600.QwiicMCP9600.kTypeS
# Other options are:
	# qwiic_mcp9600.QwiicMCP9600.kTypeK
	# qwiic_mcp9600.QwiicMCP9600.kTypeJ
	# qwiic_mcp9600.QwiicMCP9600.kTypeT
	# qwiic_mcp9600.QwiicMCP9600.kTypeN
	# qwiic_mcp9600.QwiicMCP9600.kTypeE
	# qwiic_mcp9600.QwiicMCP9600.kTypeB
	# qwiic_mcp9600.QwiicMCP9600.kTypeR

def runExample():

	print("\nQwiic MCP9600 Example 2 - Set Type\n")

	# Create instance of device
	myThermo = qwiic_mcp9600.QwiicMCP9600()

	# Check if it's connected
	if myThermo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myThermo.begin()
	
	# Change the thermocouple type being used
	print("Changing thermocouple type!")
	myThermo.set_thermocouple_type(therm_type)

	got_type = myThermo.get_thermocouple_type()
	if got_type == therm_type:
		print("Thermocouple type set successfully!")
	else:
		print("Failed to set thermocouple type! Wanted type:", therm_type, "but got type:", got_type)
		return

	if myThermo.get_thermocouple_type() == therm_type:
		print("Thermocouple type set successfully!")
	else:
		print("Failed to set thermocouple type!")

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