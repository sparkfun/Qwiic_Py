#!/usr/bin/env python
#-------------------------------------------------------------------------------
# SparkFun_Qwiic_6DoF_LSM6DSO_Arduino_Library.py
#
# Demonstrates how to get basic measurements from the LSM6DSO 6DoF IMU
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

import qwiic_lsm6dso
import sys
import time

def runExample():
	print("\nQwiic LSM6DSO Example 1 - Basic Readings\n")

	# Create instance of device
	my_imu = qwiic_lsm6dso.QwiicLSM6DSO()

	# Check if it's connected
	if my_imu.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_imu.begin()

	# The accelerometer range can be 2g, 4g, 8g, or 16g
	# A higher range means less chance of clipping, but less resolution
	my_imu.set_accel_range(my_imu.FS_XL_16g)
	
	# The gyroscope range can be 125dps, 250dps, 500dps, 1000dps, or 2000dps
	# A higher range means less chance of clipping, but less resolution
	my_imu.set_gyro_range(my_imu.FS_G_2000dps)
	
	# Both the accelerometer and gyroscope can have independent data rates, but
	# it's recommended to use the same rate for both. Valid choices are:
	# 12.5Hz, 26Hz, 52Hz, 104Hz, 208Hz, 416Hz, 833Hz, 1660Hz, 3330Hz, and 6660Hz
	# Higher data rates are more accurate, but use more power
	my_imu.set_accel_data_rate(my_imu.ODR_6660Hz)
	my_imu.set_gyro_data_rate(my_imu.ODR_6660Hz)

	# Note - if you want to minimize power consumption, the accelerometer and
	# gyroscope can be disabled by setting the rate to zero (called DISABLE).
	# Additionally, the accelerometer can be set to an even lower rate of 1.6Hz
	# my_imu.set_accel_data_rate(my_imu.ODR_1_6Hz)
	# my_imu.set_gyro_data_rate(my_imu.ODR_DISABLE)

	# Loop forever while printing data
	while True:
		# Read all the accelerometer and gyro data
		accX, accY, accZ, gyrX, gyrY, gyrZ = my_imu.read_float_accel_gyro_all()
		
		# Now print the results!
		print("Accelerometer: X:%.2f, Y:%.2f, Z:%.2f g" % (accX, accY, accZ))
		print("Gyroscope:     X:%.2f, Y:%.2f, Z:%.2f dps" % (gyrX, gyrY, gyrZ))

		# Add some space between readings
		print()

		# We'll do a very brief delay in order to log more data. This can help
		# make it easier to see the difference between settings
		time.sleep(0.01)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)