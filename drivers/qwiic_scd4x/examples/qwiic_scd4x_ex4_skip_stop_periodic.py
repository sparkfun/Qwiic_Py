#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_scd4x_ex4_skip_stop_periodic.py
#
# This example skips the stop_periodic_measurement() call in begin() and 
# prints the current CO2 level, relative humidity, and temperature in C.
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


print("\nQwiic SCD4x Example 4 - Skip Stop Periodic Measurement\n")

# Create instance of device
mySCD4x = qwiic_scd4x.QwiicSCD4x() 

# Check if it's connected
if not mySCD4x.is_connected():
	print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
	sys.exit(1)

# Initialize the device

# begin() has three boolean parameters:
# meas_begin: set to true to begin periodic measurements automatically;
#            set to false to leave periodic measurements disabled.
#            Default is true.
# auto_calibrate: set to true to leave automatic calibration enabled;
#                set to false to disable automatic calibration.
#                Default is true.
# skip_stop_periodic_measurement: set to true to make begin() skip the initial call of stop_periodic_measurement;
#                               set to false to make begin() stop periodic measurements before doing anything else.
#                               Default is false.

# When periodic measurements are enabled, the SCD4x will only repond to:
# read_measurement; stop_periodic_measurement; set_ambient_pressure; and get_data_ready_status. All other commands are ignored.

# Because begin() uses get_serial_number to check if the SCD4x is connected, begin() would fail if a previous example had
# left periodic measurements enabled. So, by default, begin() will call stop_periodic_measurement before calling
# get_serial_number. The down side to this is that stop_periodic_measurement takes 500ms to complete, incorporating a
# blocking call of delay(500). If the user is confident that periodic measurements are already disabled,
# skip_stop_periodic_measurement can be set to true to skip the initial call of stop_periodic_measurement.
# In this example, we will tell begin() to: enable periodic measurements; enable auto calibration;
# and skip the initial stop_periodic_measurement to save that 500ms delay.
# Instead we can manually call stop_periodic_measurement first:

#It is OK to call stop_periodic_measurement before begin()
mySCD4x.stop_periodic_measurement()

# Now we call begin() and set skip_stop_periodic_measurement to true
if not mySCD4x.begin(skip_stop_periodic_measurement=True):
	print("Error while initializing device", file=sys.stderr)
	sys.exit(1)

while True:
	if mySCD4x.read_measurement(): # This must be called to get new data. It will return false until new data is available 
		print("\nCO2(ppm):", mySCD4x.get_co2())
		print("Temperature(C):", mySCD4x.get_temperature())
		print("Humidity(%RH):", mySCD4x.get_humidity())
	else:
		print(".", end="")

	qwiic_i2c.delay_ms(500) # Only check for new data every 0.5 second
