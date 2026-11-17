#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_scd4x_ex9_sensor_type.py
#
# This example determines and prints the device type then exits
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
import time

def runExample():
	print("\nQwiic SCD4x Example 9 - Sensor Type\n")

	# Create instance of device
	mySCD4x = qwiic_scd4x.QwiicSCD4x() 

	# Check if it's connected
	if mySCD4x.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	# Initialize the device (NOTE: we do not start periodic measurements and we poll and set device type)
	if mySCD4x.begin(measBegin=False, pollAndSetDeviceType=True) == False:
		print("Error while initializing device", file=sys.stderr)
		return
	
	# Get the type of our sensor (NOTE: this is actually already done in the begin() function above since we set pollAndSetDeviceType=True)
	# But it is useful to see how to call the below functions explicitly if you want to check sensor type after begin()
	
	mySCD4x.get_feature_set_version() # issues command to get feature set and stores the sensor type
	sensor_type = mySCD4x.get_sensor_type() # returns the sensor type

	if sensor_type == mySCD4x.kTypeSCD40:
		print("Sensor type is SCD40")
	elif sensor_type == mySCD4x.kTypeSCD41:
		print("Sensor type is SCD41")
	else:
		print("Unknown sensor type")

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)