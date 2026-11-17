#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Example_01_BasicReadings.py
#
# Simple Example for the Qwiic AS6212 Device
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
# Example 1
#

from __future__ import print_function
import qwiic_as6212
import time
import sys

def runExample():

	print("\nSparkFun Qwiic AS6212 Sensor Example 1\n")
	myTempSensor = qwiic_as6212.QwiicAs6212Sensor()

	if myTempSensor.is_connected == False:
		print("The Qwiic AS6212 Sensor device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myTempSensor.begin()
	time.sleep(1)

	print("Initialized.")

	# Initialize configuration settings
	# These settings are saved in the sensor, even if it loses power
  
	# set the number of consecutive faults before triggering alarm.
	# valid options: 1,2,3 or 4
	myTempSensor.set_consecutive_faults(1)
  
	# set the polarity of the Alert. (0:Active LOW, 1:Active HIGH).
	myTempSensor.set_alert_polarity(myTempSensor.AS6212_ALERT_ACTIVE_LOW)
  
	# set the sensor in Comparator Mode (0) or Interrupt Mode (1).
	myTempSensor.set_interrupt_mode(myTempSensor.AS6212_MODE_COMPARATOR)
  
	# set the Conversion Cycle Time (how quickly the sensor gets a new reading)
	myTempSensor.set_conversion_cycletime(myTempSensor.AS6212_CONVERSION_CYCLE_TIME_250MS)

	# set T_HIGH, the upper limit to trigger the alert on
	myTempSensor.set_high_temp_f(78.0)  # set T_HIGH in F
	# myTempSensor.set_high_temp_c(25.56) # set T_HIGH in C
  
	# set T_LOW, the lower limit to shut turn off the alert
	myTempSensor.set_low_temp_f(75.0)	# set T_LOW in F
	# myTempSensor.set_low_temp_c(23.89)	# set T_LOW in C

	print("TLOW F: ", myTempSensor.read_low_temp_f())
	print("THIGH F: ", myTempSensor.read_high_temp_f())
		
	while True:
		myTempSensor.set_sleep_mode(0) # turn sleep  mode off (0)
		time.sleep(0.250) # allow time to wake up and complete first conversion
		
		temperature = myTempSensor.read_temp_f()
		
		# Check for alert
		alertRegisterState = myTempSensor.get_alert_status()		# read the Alert from register
		
		# Place sensor in sleep mode to save power.
		# Current consumption typically ~0.1uA.
		myTempSensor.set_sleep_mode(1) # turn sleep  mode on (1)
		
		print("Temperature: ", temperature, "\tAlert Register: ", alertRegisterState)
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)