#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_max1704x_ex1_simple.py 
#
# This file demonstrates the simple API of the SparkFun MAX17043 Arduino library.

# This example will print the gauge's voltage and state-of-charge (SOC) readings
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

import qwiic_max1704x
import sys
import time

def runExample():
	print("\nQwiic MAX1704X Example 1 - Simple\n")

	# Create instance of device
	myLipo = qwiic_max1704x.QwiicMAX1704X() # defaults to the MAX17043 device

	# Comment out above line and comment out below line if not using MAX17043. 
	# You can pass any of the following device types: 
	#	kDeviceTypeMAX17043,
	# 	kDeviceTypeMAX17044, 
	# 	kDeviceTypeMAX17048, 
	# 	kDeviceTypeMAX17049
	#
	# myLipo = qwiic_max1704x.QwiicMAX1704X(qwiic_max1704x.QwiicMAX1704X.kDeviceTypeMAX17048)

	# Check if it's connected
	if myLipo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myLipo.begin()

	myLipo.quick_start()

	# We can set an interrupt to alert when the battery SoC gets too low.
	# We can alert at anywhere between 1% - 32%:
	myLipo.set_threshold(20)

	while True:
		# get_voltage() returns a voltage value (e.g. 3.93)
		voltage = myLipo.get_voltage()
		print("Voltage: %.2fV" % voltage)

		# get_soc() returns the estimated state of charge (e.g. 79%)
		soc = myLipo.get_soc()
		print("State of Charge: %.2f%%" % soc)

		# get_alert() returns True if the battery SoC is below the threshold
		if myLipo.get_alert():
			print("Battery SoC is below threshold!")
		else:
			print("Battery SoC is above threshold.")

		# Delay so as to not spam prints
		time.sleep(0.500)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)