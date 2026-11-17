#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Example1-GetTemperature.py
#
# Simple Example for the Qwiic TMP102 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
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

import qwiic_tmp102
import time
import sys

def runExample():

	print("\nSparkFun Qwiic TMP102 Sensor Example 1\n")
	myTmpSensor = qwiic_tmp102.QwiicTmp102Sensor()

	if myTmpSensor.is_connected == False:
		print("The Qwiic TMP102 Sensor device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myTmpSensor.begin()

	print("Initialized.")

	# Initialize sensor0 settings
	# These settings are saved in the sensor, even if it loses power
  
	# set the number of consecutive faults before triggering alarm.
	# 0-3: 0:1 fault, 1:2 faults, 2:4 faults, 3:6 faults.
	myTmpSensor.set_fault(0)
  
	# set the polarity of the Alarm. (0:Active LOW, 1:Active HIGH).
	myTmpSensor.set_alert_polarity(1)	# Active HIGH
  
	# set the sensor in Comparator Mode (0) or Interrupt Mode (1).
	myTmpSensor.set_alert_mode(0)	# Comparator Mode.
  
	# set the Conversion Rate (how quickly the sensor gets a new reading)
	#0-3: 0:0.25Hz, 1:1Hz, 2:4Hz, 3:8Hz
	myTmpSensor.set_conversion_rate(2)
  
	#set Extended Mode.
	#0:12-bit Temperature(-55C to +128C) 1:13-bit Temperature(-55C to +150C)
	myTmpSensor.set_extended_mode(0)

	#set T_HIGH, the upper limit to trigger the alert on
	myTmpSensor.set_high_temp_f(85.0)  # set T_HIGH in F
	#myTmpSensor.set_high_temp_c(29.4) # set T_HIGH in C
  
	#set T_LOW, the lower limit to shut turn off the alert
	myTmpSensor.set_low_temp_f(84.0)	# set T_LOW in F
	#myTmpSensor.set_low_temp_c(26.67)	# set T_LOW in C
		
	while True:
		myTmpSensor.wakeup()
		
		temperature = myTmpSensor.read_temp_f()
		
		# Check for alert
		alertRegisterState = myTmpSensor.alert()		# read the Alert from register
		
		# Place sensor in sleep mode to save power.
		# Current consumption typically <0.5uA.
		myTmpSensor.sleep()
		
		print("Temperature: ", temperature)
		print("Alert Register: ", alertRegisterState)
		time.sleep(2)
	

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


