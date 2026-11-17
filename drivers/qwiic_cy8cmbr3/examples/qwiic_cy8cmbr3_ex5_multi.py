#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cy8cmbr3_ex5_multi.py
#
# Shows how to interact with multiple Qwiic CY8CMBR3 Capacitive Soil Moisture Sensors
# 
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

import qwiic_cy8cmbr3
import sys
import time

# NOTE: Before running this example, ensure you have cut the pull-up traces on all but one of the sensors

# Example I2C addresses for multiple sensors. You can set these addresses using the I2C
# address example script (qwiic_cy8cmbr3_ex4_i2c_addr.py)
addresses = [0x30, 0x31] # Add more addresses as needed

def runExample():
	print("\nQwiic Template Example 5 - Multiple Sensors\n")

	sensors = []

	# Create a device instance for each address (Note the "address" parameter)
	for addr in addresses:
		sensors.append(qwiic_cy8cmbr3.QwiicCY8CMBR3(address=addr))

	# Check if each sensor is connected
	for sensor in sensors:
		if sensor.is_connected() == False:
			print("The device at address " + hex(sensor.address) + " isn't connected to the system. Please check your connection", \
				file=sys.stderr)
			print("Make sure you have already set the I2C address correctly for each sensor with the address example script (qwiic_cy8cmbr3_ex4_i2c_addr.py)", \
				file=sys.stderr)
			return

	# Initialize the devices 
	for sensor in sensors:
		if not sensor.begin():
			print("Failed to initialize sensor at address: " + hex(sensor.address), file=sys.stderr)
			return

	# Infinite loop reading data
	while True:
		# Read and print the soil capacitance from each sensor
		for sensor in sensors:
			capacitance = sensor.get_capacitance_pf()
			print("Sensor 0x" + hex(sensor.address) + " Soil Capacitance: " + str(capacitance) + " pF")
		print("")  # Blank line between readings
		# Sleep for a second to avoid spamming the output
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)