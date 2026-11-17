#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ultrasonic_ex2_basic_readings.py
#
# Demosntrates how to change the address of the Qwiic Ultrasonic Sensor
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2023
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

import qwiic_ultrasonic
import sys
import time

# Here we set the device address. Note that an older version of the Qwiic
# Ultrasonic firmware used a default address of 0x00. If yours uses 0x00,
# you'll need to change the address below. It is also recommended to run
# Example 2 to change the address to the new default.
deviceAddress = qwiic_ultrasonic.QwiicUltrasonic.kDefaultAddress
# deviceAddress = 0x00

def runExample():
	print("\nQwiic Ultrasonic Example 1 - Basic Readings\n")

	# Create instance of device
	my_ultrasonic = qwiic_ultrasonic.QwiicUltrasonic(address=deviceAddress)

	# Check if it's connected
	if my_ultrasonic.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_ultrasonic.begin()

	# Repeat until the address has been successfully changed
	addressChanged = False
	while not addressChanged:
		# Print instructions
		print()
		print("Please enter a new address for the sensor.")
		print("Any value between 0x20 and 0x2F is valid.")
		print("Enter the address in hexadecimal without the `0x`.")
		print()

		# Read input from user
		newAddress = input("New address: ")

		try:
			# Parse input using int() function
			newAddress = int(newAddress, 16)

			print("Parsed address:", hex(newAddress))

			# Check if the address is valid
			if newAddress < my_ultrasonic.kMinAddress or newAddress > my_ultrasonic.kMaxAddress:
				print("Invalid address!")
				continue

			# Address is valid, attempt to change it on the device
			result = my_ultrasonic.change_address(newAddress)

			# Check whether the address was changed successfully
			if result == False:
				print("Failed to change address!")
				continue
			
			# Success, we're done here!
			addressChanged = True

		except ValueError:
			print("Invalid address format!")

	print("Address changed successfully! Continuing...")

	# Wait a moment so user can read the messages
	time.sleep(1)

	# Loop forever
	while True:
		# Get measurement from sensor. Note that the measured distance actually
		# comes from the previous trigger, so measurements will be slightly delayed
		distance = my_ultrasonic.trigger_and_read()

		# Print measurement
		print("Distance (mm):", distance)

		# Wait a bit
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)