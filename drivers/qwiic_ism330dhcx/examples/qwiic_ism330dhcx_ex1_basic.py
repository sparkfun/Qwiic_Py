#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ism330dhcx_ex1_basic.py
#
# This example shows the basic settings and functions for retrieving accelerometer and gyroscopic data
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, January 2025
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

import qwiic_ism330dhcx
import sys
import time

def runExample():
	print("\nQwiic ISM330DHCX Example 1 - Basic Readings\n")

	# Create instance of device
	myIsm = qwiic_ism330dhcx.QwiicISM330DHCX()

	# Check if it's connected
	if myIsm.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myIsm.begin()
	# Reset the device to default settings. This if helpful is you're doing multiple
	# uploads testing different settings. 
	myIsm.device_reset()

	# Wait for it to finish resetting
	while myIsm.get_device_reset() == False:
		time.sleep(1)

	print("Reset.")
	print("Applying settings.")
	time.sleep(0.100)

	myIsm.set_device_config()
	myIsm.set_block_data_update()

	# Set the output data rate and precision of the accelerometer
	myIsm.set_accel_data_rate(myIsm.kXlOdr104Hz)
	myIsm.set_accel_full_scale(myIsm.kXlFs4g)

	# Set the output data rate and precision of the gyroscope
	myIsm.set_gyro_data_rate(myIsm.kGyroOdr104Hz)
	myIsm.set_gyro_full_scale(myIsm.kGyroFs500dps)

	# Turn on the accelerometer's filter and apply settings
	myIsm.set_accel_filter_lp2()
	myIsm.set_accel_slope_filter(myIsm.kLpOdrDiv100)

	# Turn on the gyroscope's filter and apply settings
	myIsm.set_gyro_filter_lp1()
	myIsm.set_gyro_lp1_bandwidth(myIsm.kBwMedium)

	while True:
		if myIsm.check_status():
			# Get the accelerometer data
			accelData = myIsm.get_accel()
			print("Accel X: %f, Y: %f, Z: %f " % (accelData.xData, accelData.yData, accelData.zData), end='')
			gyroData = myIsm.get_gyro()
			print("Gyro X: %f, Y: %f, Z: %f" % (gyroData.xData, gyroData.yData, gyroData.zData))
		
		time.sleep(0.100) # Delay so that we don't spam user console or I2C bus

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)