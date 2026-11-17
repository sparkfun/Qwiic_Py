#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cap1203_ex6_disable_interrupt.py
#
# Demonstrates how to disable interrupts from the Qwiic CAP1203
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

import qwiic_cap1203
import sys

def runExample():
	print("\nQwiic CAP1203 Example 6 - Disable Interrupt\n")

	# Create instance of device
	myDevice = qwiic_cap1203.QwiicCAP1203()

	# Check if it's connected
	if myDevice.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myDevice.begin()

	# Interrupt is ENABLED as default.
	# When the interrupt pin is DISABLED, the alert LED
	# does not turn on. When the interrupt pin is ENABLED,
	# the alert LED turns on when a touch is detected.
	myDevice.set_interrupt_disabled()  # Disable Interrupt
	# myDevice.set_interrupt_enabled()   # Enable Interrupt

	# Check the current status of the interrupt pin.
	# Returns True if interrupt pin is enabled and
	# False if disabled.
	if myDevice.is_interrupt_enabled():
		print("Interrupt: ENABLED")
	else:
		print("Interrupt: DISABLED")

	while True:
		if myDevice.is_touched():
			print("Touch")
			while myDevice.is_touched():
				pass

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)