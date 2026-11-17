#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cap1203_ex4_power_button.py
#
# Demonstrates how to get basic readings from the Qwiic CAP1203
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
	print("\nQwiic CAP1203 Example 4 - Power Button\n")

	# Create instance of device
	myDevice = qwiic_cap1203.QwiicCAP1203()

	# Check if it's connected
	if myDevice.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myDevice.begin()

	# Set which pad acts as the power button: PAD_LEFT, PAD_MIDDLE, PAD_RIGHT
	# myDevice.set_power_button_pad(myDevice.PAD_LEFT)
	myDevice.set_power_button_pad(myDevice.PAD_MIDDLE)
	# myDevice.set_power_button_pad(myDevice.PAD_RIGHT)

    # Get the current pad which acts as the power button.
    # The function returns the pad as an interger which
    # maps to a specific position.
	# 
    # PAD   POSITION
    # 1     Left
    # 2     Middle
    # 3     Right
	pad = myDevice.get_power_button_pad()
	if pad == 1:
		print("Power Button Pad: Left")
	elif pad == 2:
		print("Power Button Pad: Middle")
	elif pad == 3:
		print("Power Button Pad: Right")

	# Set the length of time (in ms) which the designated
	# power button must indicate a touch before being
	# recognized as a power button touch.
	# sensor.set_power_button_time(myDevice.PWR_TIME_280_MS)    # 280 ms
	# sensor.set_power_button_time(myDevice.PWR_TIME_560_MS)    # 560 ms
	# sensor.set_power_button_time(myDevice.PWR_TIME_1120_MS)   # 1120 ms
	myDevice.set_power_button_time(myDevice.PWR_TIME_2240_MS)  # 2240 ms

	# Get the length of time the designated power button
	# must indicate a touch before being recognized as a
	# power button touch.
	print("Power Button Time: " + str(myDevice.get_power_button_time()) + " ms")

	# Enable or disable the power button functionality.
	# When the power button is ENABLED, the specified pad
	# (from setPowerButtonPad() function) acts as a power
	# button. When the power button is DISABLED, all pads
	# act as regular capacitive touch sensors.
	myDevice.set_power_button_enabled()  # Enable power button
	# myDevice.set_power_button_disabled()  # Disable power button

	# Returns the state of the power button. Returns true
	# if ENABLED, otherwise returns false.
	if myDevice.is_power_button_enabled() == True:
		print("Power Button: ENABLED")
	else:
		print("Power Button: DISABLED")

	while True:
		if myDevice.is_power_button_touched():
			print("Power Button")
			while myDevice.is_power_button_touched():
				# Wait until user removes finger
				pass

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)