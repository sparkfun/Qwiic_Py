#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Example_02_SingleShot.py
#
# Simple Example for the Qwiic AS6212 Device
#
# This example uses the Single Shot Feature of the device.
# It puts the sensor into sleep mode, and then in order to take
# each reading, it calls the trigger_single_shot_conversion() function.
# This allows us to take single readings on demand and really
# keep power use to a minimum.
#
# Note, in the basic readings example, we are "waking up" the sensor
# (by turning sleep mode off), and then it enters continuous reading mode,
# and so the sensor will continue to make conversions at the set conversion cycle time (4Hz).
# This uses more power, but can be useful if you want to setup an alert, and can
# be even finer tuned by setting up the amount of desired consecutive faults.
#
# Note, using single shot readings like in this example, can also
# allow you to poll the SS bit (and know when the conversion is complete)
# SS bit = 0 = No conversion ongoing / conversion finished
# SS bit = 1 = Start single shot conversion / conversion ongoing
# This can allow you to immediate start another conversion, and increase
# the amount of conversions you demand.
#
# As the device exhibits a very short conversion time (~36ms-51ms), the effective conversion
# rate can be increased by setting the single shot bit repetitively after a conversion has finished.
# However, it has to be ensured that the additional power is limited, otherwise self-heating
# effects have to be considered.
# 
#------------------------------------------------------------------------
#
# Written by Pete Lewis, SparkFun Electronics, Aug 2021
# 
# Thanks to Alex Wende and Lori Croster @ SparkFun Electronics
# for code examples from TMP102 Python Package, May 2021
# (https://github.com/sparkfun/Qwiic_TMP102_Py)
#
# Thanks to Brandon Williams. This library was based off his 
# original library created 07/15/2020 and can be found here:
# https://github.com/will2055/AS6212-Arduino-Library/
#
# Thanks to Madison Chodikov @ SparkFun Electronics
# for code examples from TMP117 Arduino Library
# (https://github.com/sparkfun/SparkFun_TMP117_Arduino_Library)
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
# Copyright (c) 2021 SparkFun Electronics
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
# Example 2
#

from __future__ import print_function
import qwiic_as6212
import time
import sys

def runExample():

	print("\nSparkFun Qwiic AS6212 Sensor Example 2 - Single Shot Readings\n")
	myTempSensor = qwiic_as6212.QwiicAs6212Sensor()

	if myTempSensor.is_connected == False:
		print("The Qwiic AS6212 Sensor device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myTempSensor.begin()
	time.sleep(1)

	print("Initialized.")

	myTempSensor.set_sleep_mode(1) # turn sleep  mode on (1)
	print("Sleep mode ON")
	time.sleep(1)

	while True:
		myTempSensor.trigger_single_shot_conversion() # trigger SS

		#wait for conversion to complete (~51ms)
		conversionTime = 0
		while myTempSensor.get_single_shot_status() == 1:
			conversionTime += 1
			time.sleep(0.001) # 1ms
			
		tempF = myTempSensor.read_temp_f()
		
		print("Temperature: %.2fF \t Conversion time: %ims" % (tempF, conversionTime))
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)