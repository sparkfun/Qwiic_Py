#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_env_bme280_ex4.py
#
# Simple Example for the Qwiic BME280 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
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
# Example 4 - port of the Arduino example 4
#

import qwiic_bme280
import time
import sys

def runExample():

	print("\nSparkFun BME280 Sensor  Example 4\n")
	mySensor = qwiic_bme280.QwiicBme280()

	if mySensor.connected == False:
		print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	mySensor.begin()

	# setup the sensor
	mySensor.filter = 1  		# 0 to 4 is valid. Filter coefficient. See 3.4.4
	mySensor.standby_time = 0 	# 0 to 7 valid. Time between readings. See table 27.
	
	mySensor.tempature_oversample = 1			# 0 to 16 are valid. 0 disables temp sensing. See table 24.
	mySensor.pressure_oversample = 1	# 0 to 16 are valid. 0 disables pressure sensing. See table 23.
	mySensor.humidity_oversample = 1	# 0 to 16 are valid. 0 disables humidity sensing. See table 19.
	mySensor.mode = mySensor.MODE_NORMAL # MODE_SLEEP, MODE_FORCED, MODE_NORMAL is valid. See 3.3

	while True:
		print("Humidity:\t%.3f" % mySensor.humidity)

		print("Pressure:\t%.3f" % mySensor.pressure)	

		print("Altitude:\t%.3f" % mySensor.altitude_feet)

		print("Temperature:\t%.2f\n" % mySensor.temperature_fahrenheit)

		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 4")
		sys.exit(0)


