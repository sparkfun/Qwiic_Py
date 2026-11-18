#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_icm20948_ex1_basic_readings.py
#
# Simple Example for the Qwiic ICM20948 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, March 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
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
#==================================================================================
# Example 1
#

import qwiic_icm20948
import qwiic_i2c
import sys

def run_example():

	print("\nSparkFun 9DoF ICM-20948 Sensor  Example 1\n")
	imu = qwiic_icm20948.QwiicICM20948()

	if not imu.is_connected():
		print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	imu.begin()

	while True:
		if imu.data_ready():
			imu.get_agmt() # read all axis and temp from sensor, note this also updates all instance variables
			print(\
			 'ax: {: 06d}'.format(imu.ax_raw)\
			, '\t', 'ay: {: 06d}'.format(imu.ay_raw)\
			, '\t', 'az: {: 06d}'.format(imu.az_raw)\
			, '\t', 'gx: {: 06d}'.format(imu.gx_raw)\
			, '\t', 'gy: {: 06d}'.format(imu.gy_raw)\
			, '\t', 'gz: {: 06d}'.format(imu.gz_raw)\
			, '\t', 'mx: {: 06d}'.format(imu.mx_raw)\
			, '\t', 'my: {: 06d}'.format(imu.my_raw)\
			, '\t', 'mz: {: 06d}'.format(imu.mz_raw)\
			)
			qwiic_i2c.delay_ms(30)
		else:
			print("Waiting for data")
			qwiic_i2c.delay_ms(500)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example 1")
		sys.exit(0)


