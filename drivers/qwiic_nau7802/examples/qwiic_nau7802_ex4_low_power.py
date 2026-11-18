#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_nau7802_ex4_low_power.py
#
# Demonstrates how to set the Qwiic Scale into low power mode
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2023
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

import qwiic_nau7802
import sys
import qwiic_i2c


print("\nQwiic NAU7802 Example 4 - Low Power\n")

# Create instance of device
my_scale = qwiic_nau7802.QwiicNAU7802()

# Check if it's connected
if my_scale.is_connected() == False:
	print("The device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

# Initialize the device
my_scale.begin()

# Loop forever
while True:
	# Tell NAU7802 to power down, current consumption is ~200nA
	my_scale.power_down()

	# Wait a little bit while in low power mode
	qwiic_i2c.delay_ms(1000)

	# Power up again
	my_scale.power_up()

	# Wait for new reading to become available, and time how long it takes
	start_time = qwiic_i2c.ticks_ms()
	while my_scale.available() == False:
		qwiic_i2c.delay_ms(1)

	# Measurement finished, stop the timer!
	finish_time = qwiic_i2c.ticks_ms()

	# Print data
	print("Start up time (ms):", qwiic_i2c.ticks_diff(finish_time, start_time))
	print("Reading:", my_scale.get_reading())

	# Give some space between prints
	print()
