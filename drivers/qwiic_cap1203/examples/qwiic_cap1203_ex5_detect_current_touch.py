#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cap1203_ex5_detect_current_touch.py
#
# Demonstrates how to current touch from the Qwiic CAP1203
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


print("\nQwiic CAP1203 Example 5 - Detect Current Touch\n")

# Create instance of device
my_device = qwiic_cap1203.QwiicCAP1203()

# Check if it's connected
if my_device.is_connected() == False:
	print("The device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

# Initialize the device
my_device.begin()

while True:
	if my_device.is_left_touched():
		print("Left")
		while my_device.is_left_touched():
			# Wait until user removes finger
			pass
	if my_device.is_middle_touched():
		print("Middle")
		while my_device.is_middle_touched():
			# Wait until user removes finger
			pass
	if my_device.is_right_touched():
		print("Right")
		while my_device.is_right_touched():
			# Wait until user removes finger
			pass
