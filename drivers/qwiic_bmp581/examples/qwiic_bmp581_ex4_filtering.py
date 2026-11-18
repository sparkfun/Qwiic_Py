#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_bmp581_ex4_filtering.py
#
# This example demonstrates how to use filtering to smooth temperature and pressure measurements.
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

import qwiic_bmp581
import sys
import qwiic_i2c


print("\nQwiic BMP581 Example 4 - Filtering\n")

# Create instance of device
myBMP581 = qwiic_bmp581.QwiicBMP581()

# Check if it's connected
if not myBMP581.is_connected():
	print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
	sys.exit(1)

# Initialize the device
if not myBMP581.begin():
	print("Unable to Initialize device! Please check your connection and try again.", file=sys.stderr)
	sys.exit(1)

print("BMP581 connected!")

# The BMP581 can filter both the temperature and pressure measurements individually.
# By default, both filter coefficients are set to 0 (no filtering). We can smooth
# out the measurements by increasing the coefficients with this function
config = qwiic_bmp581.IirConfig()
config.setIirT = config.IIR_FILTER_COEFF_127 # Set filter coefficient for temperature
config.setIirP = config.IIR_FILTER_COEFF_127 # Set filter coefficient for pressure
config.shdwSetIirT = myBMP581.ENABLE # Store filtered data in data registers
config.shdwSetIirP = myBMP581.ENABLE # Store filtered data in data registers
config.iirFlushForcedEn = myBMP581.DISABLE # Disable filter in forced mode

myBMP581.set_iir_config(config)

while True:
	data = myBMP581.get_sensor_data()
	print("Temperature (C): ", data.temperature, end='\t\t')
	print("Pressure (Pa): ", data.pressure)

	# Print every 100ms to see the filtering in action
	qwiic_i2c.delay_ms(100)
