#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ads1015_ex2_change_gain.py
#
#   This example shows how to output ADC values on one single-ended channel (A3) with a PGA GAIN of 1. 
#   At this gain setting (and 3.3V VCC), 0-3.3V will read 0-1652.

#   Other possible gain settings are as follows. 
#   Note, changing the gain effects the range of the sensor (aka the max and min voltages it can read).
#   Also note, to avoid damaging your ADC, never exceed VDD (3.3V for a qwiic system).

#   ADS1015_CONFIG_PGA_TWOTHIRDS  +/- 6.144v
#   ADS1015_CONFIG_PGA_1          +/- 4.096v (used in this example)
#   ADS1015_CONFIG_PGA_2          +/- 2.048v
#   ADS1015_CONFIG_PGA_4          +/- 1.024v
#   ADS1015_CONFIG_PGA_8          +/- 0.512v
#   ADS1015_CONFIG_PGA_16         +/- 0.256v
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
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

import qwiic_ads1015
import sys
import time

def runExample():
	print("\nQwiic ADS1015 Example 2 - Change Gain\n")

	# Create instance of device
	myAds = qwiic_ads1015.QwiicADS1015()

	# Check if it's connected
	if myAds.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myAds.begin()

	myAds.set_gain(myAds.kConfigPga1)

	while True:
		channel_A3 = myAds.get_single_ended(3)
		print("A3: ", channel_A3)
		time.sleep(0.050)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 2")
		sys.exit(0)