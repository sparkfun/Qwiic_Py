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

	# Loop forever while printing data
	while True:
		# There are a few ways to read sensor data, some are faster than others.
		# Uncomment the section you want to use below.

		# You can read each axis individually
		# accX = my_imu.read_float_accel_x()
		# accY = my_imu.read_float_accel_y()
		# accZ = my_imu.read_float_accel_z()
		# gyrX = my_imu.read_float_gyro_x()
		# gyrY = my_imu.read_float_gyro_y()
		# gyrZ = my_imu.read_float_gyro_z()

		# Or you can read all 3 axes of each sensor in one call for faster reads
		# accX, accY, accZ = my_imu.read_float_accel_all()
		# gyrX, gyrY, gyrZ = my_imu.read_float_gyro_all()

		# Or you can read all 6 axes in a single call for the fastest read speed
		accX, accY, accZ, gyrX, gyrY, gyrZ = my_imu.read_float_accel_gyro_all()
		
		# Now print the results!
		print("Accelerometer: X:%.2f, Y:%.2f, Z:%.2f g" % (accX, accY, accZ))
		print("Gyroscope:     X:%.2f, Y:%.2f, Z:%.2f dps" % (gyrX, gyrY, gyrZ))

		# You can also read the temperature of the IMU
		temperature = my_imu.read_temp_c()
		print("Temperature:   %.2f C" % temperature)

		# Add some space between readings
		print()

		# Wait a second and repeat
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)