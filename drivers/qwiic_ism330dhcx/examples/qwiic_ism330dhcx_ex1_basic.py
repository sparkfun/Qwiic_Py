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
import qwiic_i2c

def run_example():
	print("\nQwiic ISM330DHCX Example 1 - Basic Readings\n")

	# Create instance of device
	my_ism = qwiic_ism330dhcx.QwiicISM330DHCX()

	# Check if it's connected
	if my_ism.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	my_ism.begin()
	# Reset the device to default settings. This if helpful is you're doing multiple
	# uploads testing different settings. 
	my_ism.device_reset()

	# Wait for it to finish resetting
	while not my_ism.get_device_reset():
		qwiic_i2c.delay_ms(1000)

	print("Reset.")
	print("Applying settings.")
	qwiic_i2c.delay_ms(100)

	my_ism.set_device_config()
	my_ism.set_block_data_update()

	# Set the output data rate and precision of the accelerometer
	my_ism.set_accel_data_rate(my_ism.XL_ODR_104HZ)
	my_ism.set_accel_full_scale(my_ism.XL_FS_4G)

	# Set the output data rate and precision of the gyroscope
	my_ism.set_gyro_data_rate(my_ism.GYRO_ODR_104HZ)
	my_ism.set_gyro_full_scale(my_ism.GYRO_FS_500DPS)

	# Turn on the accelerometer's filter and apply settings
	my_ism.set_accel_filter_lp2()
	my_ism.set_accel_slope_filter(my_ism.LP_ODR_DIV100)

	# Turn on the gyroscope's filter and apply settings
	my_ism.set_gyro_filter_lp1()
	my_ism.set_gyro_lp1_bandwidth(my_ism.BW_MEDIUM)

	while True:
		if my_ism.check_status():
			# Get the accelerometer data
			accel_data = my_ism.get_accel()
			print("Accel X: %f, Y: %f, Z: %f " % (accel_data.x_data, accel_data.y_data, accel_data.z_data), end='')
			gyro_data = my_ism.get_gyro()
			print("Gyro X: %f, Y: %f, Z: %f" % (gyro_data.x_data, gyro_data.y_data, gyro_data.z_data))
		
		qwiic_i2c.delay_ms(100) # Delay so that we don't spam user console or I2C bus

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example")
		sys.exit(0)