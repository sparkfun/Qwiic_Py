#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_scd4x_ex8_scd41_single_shot.py
#
# This example shows how to perform single-shot data acquisition on the SCD41 sensor.
# 
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
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

import qwiic_scd4x
import sys
import qwiic_i2c


print("\nQwiic SCD4x Example 8 - SCD41 Single-Shot\n")

# Create instance of device
mySCD4x = qwiic_scd4x.QwiicSCD4x() 

# Check if it's connected
if not mySCD4x.is_connected():
	print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
	sys.exit(1)

# Initialize the device (NOTE: we do not start periodic measurements)
if not mySCD4x.begin(meas_begin=False):
	print("Error while initializing device", file=sys.stderr)
	sys.exit(1)

# Lets call measure_single_shot to start the first conversion
if not mySCD4x.measure_single_shot():
	print("Error while starting single-shot measurement. Are you sure your device is a SCD41 and is connected?", file=sys.stderr)
	sys.exit(1)

while True:
	# Wait for the measurement to be ready
	while not mySCD4x.read_measurement():
		print(".", end="")
		qwiic_i2c.delay_ms(500)

	# Print the single-shot data
	print("\nCO2(ppm):", mySCD4x.get_co2())
	print("Temperature(C):", mySCD4x.get_temperature())
	print("Humidity(%RH):", mySCD4x.get_humidity())

	# Request just the RH and the Temperature (should take ~50ms)
	if not mySCD4x.measure_single_shot_rht_only():
		print("Failed to start single-shot RHT measurement", file=sys.stderr)
		sys.exit(1)

	# Wait for the measurement to be ready
	while not mySCD4x.read_measurement():
		print(".", end="")
		qwiic_i2c.delay_ms(5)

	# Print the single-shot data
	print("\nTemperature(C):", mySCD4x.get_temperature())
	print("Humidity(%RH):", mySCD4x.get_humidity())

	# Do a single shot request for all the data (should take ~5seconds)
	if not mySCD4x.measure_single_shot():
		print("Failed to start single-shot measurement", file=sys.stderr)
		sys.exit(1)
