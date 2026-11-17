#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_tmp117_ex2_alert_statuses.py
#
# This script sets the TMP117 temperature sensor's high limit,
# low limit, and alert function mode. Once set, we read the 
# temperature in C and checks alert status. If we are outside
# of the boundary, we will output a message indicating
# that we are beyond the limit. 
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

def runExample():
	print("\nQwiic TMP117 Example 2 - Alert Statuses\n")

	# Create instance of device
	myTMP117 = qwiic_tmp117.QwiicTMP117()

	# Check if it's connected
	if myTMP117.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myTMP117.begin()

	print("\nNote: Make sure to configure your High and")
	print("Low Temperature Limits. These values will")
	print("be cleared on power cycle since it is only")
	print("saved in the volatile registers. This code")
	print("sets it manually. You can look at Example 5")
	print("in the library for more ideas!")

	# Note: Set the high and low limits. Make sure to set limits
    # between -256°C and 255.99°C. For quick testing at room
    # temperature that is about 20°C-25°C, we can use the heat
    # from our hand or lightly breathing on the sensor. Adjust
    # as necessary.
	myTMP117.set_high_limit(25.50)
	myTMP117.set_low_limit(25)

	# Verify that the limits are set
	print("\nHigh Limit:", myTMP117.get_high_limit(),"C")
	print("Low Limit:", myTMP117.get_low_limit(),"C")

	# Set to kAlertMode or kThermMode
	myTMP117.set_alert_function_mode(myTMP117.kAlertMode)

	# Get "Alert Function Mode" Bit from configuration register
    # Note: Depending on the mode, this affects the way HIGH and
    # LOW Alert Fields behave in the Configuration Register. For more
    # information, check out the following sections of the datasheet:
    #   7.4.4.1 Alert Mode (pg 14)
    #   7.4.4.2 Therm Mode (pg 16)
    #   7.6.1.2 Configuration Register (pg 26)

	# Wait and then verify that the alert function mode is set
	time.sleep(0.5)
	print("\nAlert Function Mode:", myTMP117.get_alert_function_mode())
	print("----------------------------------------")

	while True:
		if myTMP117.data_ready():
			# Note: If you are in Alert Mode (T/nA = kAlertMode = 0), the high and low alert
			# flags will clear whenever you read the configuration register. You
			# can add a delay to perform another temperature conversion to trigger the
			# flags again. The delay depends on the conversion cycle time so make
			# sure to adjust as necessary to check the if the flags are triggered.

			tempC = myTMP117.read_temp_c()
			print("\nTemperature in Celsius:", tempC)

			# Note: Add short delay before reading the configuration register  again.
			# Adjust this value as necessary based on your conversion cycle time.
			# Default conversion time for AVG = 1 and CONV = 4 about 1 second. Therefore,
			# a value of between 1-3 seconds should be sufficient.
			time.sleep(1.5)

			alertFlags = myTMP117.get_high_low_alert() # Returned value is a list containing the two flags
			lowAlertFlag = alertFlags[myTMP117.kLowAlertIdx]
			highAlertFlag = alertFlags[myTMP117.kHighAlertIdx]

			print ("Low Alert Flag:", lowAlertFlag)
			print ("High Alert Flag:", highAlertFlag)

			if highAlertFlag:
				print("High Alert")
			elif lowAlertFlag:
				# Alert when the temperature is over the LOW limit:
				# - In Alert Mode (T/nA = kAlertMode = 0) this flag will clear
				# when the configuration register is read.
				# - In Therm mode (T/nA =  kThermMode = 1), this flag is always 0
				print("Low Alert")
			else:
				print("No Alert")

		time.sleep(0.5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)