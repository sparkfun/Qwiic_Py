#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_ccs811_ex1_basic_readings.py
#
# Simple Example for the Qwiic CCS811 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
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

import qwiic_ccs811
import qwiic_i2c
import sys


print("\nSparkFun CCS811 Sensor Basic Example \n")
mySensor = qwiic_ccs811.QwiicCCS811()

if not mySensor.is_connected():
	print("The Qwiic CCS811 device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

# On a Raspberry Pi the CCS811 needs a slower I2C clock (see the README)
if not mySensor.is_rpi_i2c_baudrate_ok():
	print("NOTE: For the CCS811 to work on a Raspberry Pi, add the line\n"
			"  dtparam=i2c_arm_baudrate=10000\n"
			"to /boot/firmware/config.txt (/boot/config.txt on older systems) and reboot.\n", file=sys.stderr)

if not mySensor.begin():
	print("Unable to initialize the CCS811. Please check your connection", file=sys.stderr)
	sys.exit(1)

while True:

	mySensor.read_algorithm_results()

	print("CO2:\t%.3f" % mySensor.get_co2())

	print("tVOC:\t%.3f\n" % mySensor.get_tvoc())	


	qwiic_i2c.delay_ms(1000)
