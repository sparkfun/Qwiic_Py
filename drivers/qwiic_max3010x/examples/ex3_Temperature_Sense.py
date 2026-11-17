#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex3_Temperature_Sesnse.py
#
# Simple example for the qwiic MAX3010x device
# This demo outputs the onboard temperature sensor. 
# The temp sensor is accurate to +/-1 C but
# has an astonishing precision of 0.0625 C.
#
#------------------------------------------------------------------------
#
# Written by Pete Lewis
# SparkFun Electronics, May 2020
#
# Based on code from the SparkFun MAX3010x Sensor Arduino Library
# https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library
# By: Nathan Seidle @ SparkFun Electronics, October 2016
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
# Example 3
#

import qwiic_max3010x
import time
import sys

def runExample():

	print("\nSparkFun MAX3010x Photodetector - Example 3\n")
	sensor = qwiic_max3010x.QwiicMax3010x()

	if sensor.begin() == False:
		print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("The Qwiic MAX3010x is connected.")

  	# Setup Sensor
    # The LEDs are very low power and won't affect the temp reading much but
    # we will call setup() with LEDs off, to avoid any local heating (ledMode = 0)

	if sensor.setup(ledMode = 0) == False:
		print("Device setup failure. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Setup complete.")        

	sensor.enableDIETEMPRDY() # Enable the temp ready interrupt. This is required.

	while True:
			temperature = sensor.readTemperature()
			temperatureF = sensor.readTemperatureF()

			temperature = round(temperature, 2)
			temperatureF = round(temperatureF, 2)

			print(\
			 'temperatureC[', temperature , '] \t',\
             'temperatureF[', temperatureF , ']',\
			)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


