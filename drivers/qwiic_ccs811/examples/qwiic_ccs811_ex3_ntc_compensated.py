#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_ccs811_ex3_ntc_compensated.py
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

import qwiic_ccs811
import qwiic_i2c
import sys

# Define some error messages
_device_errors = { \
	1 << 5 : "HeaterSupply",  \
    1 << 4 : "HeaterFault", \
    1 << 3 : "MaxResistance", \
    1 << 2 : "MeasModeInvalid",  \
    1 << 1 : "ReadRegInvalid", \
    1 << 0 : "MsgInvalid" \
}


print("\nSparkFun CCS811 Sensor Example 3 - NTC data to CCS811 for compensation. \n")
mySensor = qwiic_ccs811.QwiicCCS811()

if not mySensor.is_connected():
	print("The Qwiic CCS811 device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

mySensor.begin()

mySensor.set_reference_resistance(9950)

while True:

	if mySensor.data_available():

		mySensor.read_algorithm_results()

		print("CO2:\t%.3f ppm" % mySensor.get_co2())

		print("tVOC:\t%.3f ppb" % mySensor.get_tvoc())

		mySensor.read_ntc()
		print("Measured Resistance: %.3f ohms" % mySensor.get_resistance())

		read_temperature = mySensor.get_temperature()
		print("Converted Temperature: %.2f deg C" % read_temperature)

		mySensor.set_environmental_data( 50, read_temperature)

	elif mySensor.check_status_error():

		error = mySensor.get_error_register()
		if error == 0xFF:   
			# communication error
			print("Failed to get Error ID register from sensor")
		else:
			str_err = "Unknown Error"
			for code in _device_errors.keys():
				if error & code:
					str_err = _device_errors[code]
					break
			print("Device Error: %s" % str_err)

	qwiic_i2c.delay_ms(1000)
