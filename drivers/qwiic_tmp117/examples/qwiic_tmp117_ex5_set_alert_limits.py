#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_tmp117_ex5_set_alert_limits.py
#
# This script can set and get the Alert Function Mode, Low Temperature 
# Limit, and High Temperature Limit for the sensor. These limits can
# be set within +/- 256°C. When the temperature goes above/below the 
# specified temperature limits, it will cause the alert pins to go
# high. To access these registers, please reference Example 2: Alert Statuses.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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
#===============================================================================

import qwiic_tmp117
import sys
import time

def alert_mode_to_string(alert_mode):
	if alert_mode == qwiic_tmp117.QwiicTMP117.kAlertMode:
		return "Alert Mode"
	elif alert_mode == qwiic_tmp117.QwiicTMP117.kThermMode:
		return "Therm Mode"

def runExample():
	print("\nQwiic TMP117 Example 5 - Set Alert Mode Temperature Limits\n")

	# Create instance of device
	myTMP117 = qwiic_tmp117.QwiicTMP117()

	# Check if it's connected
	if myTMP117.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myTMP117.begin()

	print("Current Alert Function Mode:", alert_mode_to_string(myTMP117.get_alert_function_mode()))
	print("Current Low Temperature Limit:", myTMP117.get_low_limit())
	print("Current High Temperature Limit:", myTMP117.get_high_limit())

	while True:
		print("\n\nEnter a number for one of the options below: ")
		print("0: Set Alert Function Mode")
		print("1: Set Low Limit")
		print("2: Set High Limit")
		print("Enter a number for one of the options above (0-2): ")
		option = int(input())
		
		if option == 0:
			print("Enter 0 for Alert Mode or 1 for Therm Mode: ")
			alertMode = int(input())
			
			if alertMode not in [0, 1]:
				print("Invalid option. Please enter 0 or 1.")
				continue

			myTMP117.set_alert_function_mode(alertMode)
			print("Alert Function Mode set to:", alert_mode_to_string(myTMP117.get_alert_function_mode()))
		
		if option == 1:
			print("Enter the low temperature limit in Celsius (between -256 and +255.98): ")
			lowLimit = float(input())
			if lowLimit < -256 or lowLimit > 255.98:
				print("Invalid temperature. Please enter a temperature between -256 and +255.98.")
				continue
			myTMP117.set_low_limit(lowLimit)
			print("Low Temperature Limit set to:", myTMP117.get_low_limit())

		if option == 2:
			print("Enter the high temperature limit in Celsius (between -256 and +255.98): ")
			highLimit = float(input())
			if highLimit < -256 or highLimit > 255.98:
				print("Invalid temperature. Please enter a temperature between -256 and +255.98.")
				continue
			myTMP117.set_high_limit(highLimit)
			print("High Temperature Limit set to:", myTMP117.get_high_limit())

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)