#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ads1015_ex6_display_millivolts.py
#
#   This example shows how to output ADC values on one single-ended channel (A3).
#   It will also print out the voltage of the reading in mV.
#   Note, the conversion multiplier needs to be corrected for gain settings,
#   And this is done automatically in the library, using .getMultiplier(),
#   as shown below.
  
#   *at gain setting of 1, like in this example (and 3.3V VCC), 0-3.3V will read 0-1652.
# 
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
	print("\nQwiic ADS1015 Example 6 - Display Millivolts\n")

	myAds = qwiic_ads1015.QwiicADS1015()

	# Check if it's connected
	if myAds.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myAds.begin()

	myAds.set_gain(myAds.kConfigPga1)

	while True:
		channel_A3 = myAds.get_single_ended(3)
		print("A3: ", channel_A3, end = '\t')
		
		# Get the multiplier for the gain setting
		multiplier = myAds.get_multiplier()
		# The private variable _multiplierToVolts is auto-updated each time setGain is called
		print(channel_A3 * multiplier, "mV")

		time.sleep(0.050)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 6")
		sys.exit(0)