#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_max3010x_ex1_basic_readings.py
#
# Simple example for the qwiic MAX3010x device
# Outputs all Red/IR/Green values.
#
#------------------------------------------------------------------------
#
# Written by Pete Lewis
# SparkFun Electronics, May 2020
#
# Based on code from the SparkFun MAX3010x Sensor Arduino Library
# https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library
# By: Nathan Seidle @ SparkFun Electronics, October 2nd, 2016
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

import qwiic_max3010x
import qwiic_i2c
import sys


print("\nSparkFun MAX3010x Photodetector - Example 1\n")
sensor = qwiic_max3010x.QwiicMAX3010x()

if not sensor.begin():
	print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)
else:
	print("The Qwiic MAX3010x is connected.")

sensor.setup()
print("Setup complete.")        

while True:
		print(\
		 'R[', sensor.get_red() , '] \t'\
                                                             'IR[', sensor.get_ir() , '] \t'\
                                                             'G[', sensor.get_green() , ']'\
		)
		qwiic_i2c.delay_ms(100)
