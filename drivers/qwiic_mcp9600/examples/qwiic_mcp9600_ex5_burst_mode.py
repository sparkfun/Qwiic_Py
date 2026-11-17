#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp9600_ex5_burst_mode.py
#
#   This example configures the shutdown (or "operating") mode that the MCP9600 runs in. Shutdown mode disables all
#   power consuming activities on the MCP9600, including measurements, but it will still respond to I2C commands sent
#   over Qwiic. Burst mode is similar, where the MCP9600 is shutdown until the Arduino asks it to wake up and take a 
#   number of samples, apply any filtering, update any outputs, and then enter shutdown mode. This example walks
#   through that process!
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

# Change the mode and sample number of the thermocouple here!
mode = qwiic_mcp9600.QwiicMCP9600.kShutdownModeBurst
samples = qwiic_mcp9600.QwiicMCP9600.kBurstSample8

def runExample():

	print("\nQwiic MCP9600 Example 5 - Burst Mode\n")

	# Create instance of device
	myThermo = qwiic_mcp9600.QwiicMCP9600()

	# Check if it's connected
	if myThermo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myThermo.begin()

	# Set the MCP9600 to burst mode!
	myThermo.set_burst_samples(samples)
	myThermo.set_shutdown_mode(mode)

	while True:
		if myThermo.available():
			# Read temperatures
			thermocouple_temp = myThermo.get_thermocouple_temp()
			ambient_temp = myThermo.get_ambient_temp()
			temp_delta = myThermo.get_temp_delta()

			# Print temperatures
			print(f"Thermocouple: {thermocouple_temp}C   Ambient: {ambient_temp}C   Temperature Delta: {temp_delta}C")
			
			# clear the register and start a new burst cycle!
			myThermo.start_burst()

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)