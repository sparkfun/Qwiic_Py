#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_ccs811_ex7.py
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
# Example 3
#

from __future__ import print_function
import qwiic_ccs811
import time
import sys
import random

# Define some error messages
_deviceErrors = { \
	1 << 5 : "HeaterSupply",  \
    1 << 4 : "HeaterFault", \
    1 << 3 : "MaxResistance", \
    1 << 2 : "MeasModeInvalid",  \
    1 << 1 : "ReadRegInvalid", \
    1 << 0 : "MsgInvalid" \
}

def runExample():

	print("\nSparkFun CCS811 Sensor Example 3 - NTC data to CCS811 for compensation. \n")
	mySensor = qwiic_ccs811.QwiicCcs811()

	if mySensor.connected == False:
		print("The Qwiic CCS811 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	mySensor.begin()


	while True:

		humidityVariable = random.randrange(0, 10000)/100   # 0 to 100%
		temperatureVariable = random.randrange(500, 7000) / 100 #5C to 70C

		print("New humidity and temperature:")
		print("  Humidity:    %.2f percent relative" % humidityVariable)
		print("  Temperature: %.2f degrees C" % temperatureVariable)

		mySensor.set_environmental_data(humidityVariable, temperatureVariable)
		if mySensor.data_available():

			mySensor.read_algorithm_results()

			print("  CO2:\t%.3f ppm" % mySensor.CO2)
			print("  tVOC:\t%.3f ppb\n" % mySensor.TVOC)	

		elif mySensor.check_status_error():

			error = mySensor.get_error_register();
			if error == 0xFF:   
				# communication error
				print("Failed to get Error ID register from sensor")
			else:
				strErr = "Unknown Error"
				for code in _deviceErrors.keys():
					if error & code:
						strErr = _deviceErrors[code]
						break
				print("Device Error: %s" % strErr)

		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)


