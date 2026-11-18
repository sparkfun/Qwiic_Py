#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ultrasonic_ex2_change_address.py
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
import qwiic_i2c
# Here we set the device address. Note that an older version of the Qwiic
# Ultrasonic firmware used a default address of 0x00. If yours uses 0x00,
# you'll need to change the address below. It is also recommended to run
# Example 2 to change the address to the new default.
device_address = qwiic_ultrasonic.QwiicUltrasonic.DEFAULT_ADDRESS
# device_address = 0x00

def run_example():
	print("\nQwiic Ultrasonic Example 2 - Change Address\n")

	# Create instance of device
	my_ultrasonic = qwiic_ultrasonic.QwiicUltrasonic(address=device_address)

	# Check if it's connected
	if not my_ultrasonic.is_connected():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_ultrasonic.begin()

	# Repeat until the address has been successfully changed
	address_changed = False
	while not address_changed:
		# Print instructions
		print()
		print("Please enter a new address for the sensor.")
		print("Any value between 0x20 and 0x2F is valid.")
		print("Enter the address in hexadecimal without the `0x`.")
		print()

		# Read input from user
		new_address = input("New address: ")

		try:
			# Parse input using int() function
			new_address = int(new_address, 16)

			print("Parsed address:", hex(new_address))

			# Check if the address is valid
			if new_address < my_ultrasonic.MIN_ADDRESS or new_address > my_ultrasonic.MAX_ADDRESS:
				print("Invalid address!")
				continue

			# Address is valid, attempt to change it on the device
			result = my_ultrasonic.change_address(new_address)

			# Check whether the address was changed successfully
			if not result:
				print("Failed to change address!")
				continue
			
			# Success, we're done here!
			address_changed = True

		except ValueError:
			print("Invalid address format!")

	print("Address changed successfully! Continuing...")

	# Wait a moment so user can read the messages
	qwiic_i2c.delay_ms(1000)

	# Loop forever
	while True:
		# Get measurement from sensor. Note that the measured distance actually
		# comes from the previous trigger, so measurements will be slightly delayed
		distance = my_ultrasonic.trigger_and_read()

		# Print measurement
		print("Distance (mm):", distance)

		# Wait a bit
		qwiic_i2c.delay_ms(100)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example")
		sys.exit(0)