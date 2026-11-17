#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cy8cmbr3_ex3_led.py
#
# Shows how to set up and use the Qwiic CY8CMBR3 Capacitive Soil Moisture Sensor
# for LED control based on soil moisture readings.
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

# Define soil moisture threshold for LED control
threshold = 8 # Example threshold for dry soil

def runExample():
	print("\nQwiic Template Example 3 - LED Control\n")

	# Create instance of device
	mySoilSensor = qwiic_cy8cmbr3.QwiicCY8CMBR3()

	# Check if it's connected
	if mySoilSensor.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	mySoilSensor.begin()

	# Infinite loop reading data
	while True:
		# Read and print the soil capacitance
		capacitance = mySoilSensor.get_capacitance_pf()
		print("Soil Capacitance: " + str(capacitance) + " pF")
		print("Threshold: " + str(threshold) + " pF")
		# Control LED based on soil moisture threshold
		if capacitance < threshold:
			mySoilSensor.led_on()  # Turn LED on for dry soil
			print("LED ON - Capacitance below threshold\n")
		else:
			mySoilSensor.led_off()  # Turn LED off for moist soil
			print("LED OFF - Capacitance above threshold\n")
		# Sleep for a second to avoid spamming the output
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)