#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ads1015_ex7_multi_channel.py
#
#   This example shows how to output ADC values on multiple channels.
  
#   It is based on the example provided by @StefanThoresson in Issue #6:
#   https://github.com/sparkfun/SparkFun_ADS1015_Arduino_Library/issues/6
#   Thank you Stefan.
  
#   We used this example to determine the delay values for conversionDelay.
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

def run_example():
	print("\nQwiic ADS1015 Example 7 - MultiChannel\n")

	myAds = qwiic_ads1015.QwiicADS1015()

	# Check if it's connected
	if myAds.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myAds.begin()

	# Set the gain
	# Possible Values are: 
		# CONFIG_PGA_TWO_THIRDS,
		# CONFIG_PGA_1,
		# CONFIG_PGA_2,
		# CONFIG_PGA_4,
		# CONFIG_PGA_8,
		# CONFIG_PGA_16

	myAds.set_gain(myAds.CONFIG_PGA_2)

	# Set the Sample Rate
	# Possible Values are:
		# CONFIG_RATE_128HZ
		# CONFIG_RATE_250HZ
		# CONFIG_RATE_490HZ
		# CONFIG_RATE_920HZ
		# CONFIG_RATE_1600HZ
		# CONFIG_RATE_2400HZ
		# CONFIG_RATE_3300HZ
	myAds.set_sample_rate(myAds.CONFIG_RATE_1600HZ)

	# 	For the fastest conversion timing, we need to check the Config Register Operational Status bit
	#   to see when the conversion is complete - instead of using a fixed delay.
	#   However, we can only do this if we use single-shot mode.
	#   Because this breaks backward-compatibility, _useConversionReady is disabled by default.
	#   To enable it, call:
	myAds.use_conversion_ready(True)

	while True:
		channel_A0 = myAds.get_single_ended(0)
		channel_A1 = myAds.get_single_ended(1)
		
		channel_A0_mV = myAds.get_single_ended_millivolts(0)
		channel_A1_mV = myAds.get_single_ended_millivolts(1)
		
		# get_differential options are:
			# CONFIG_MUX_DIFF_P0N1 # A0-A1 (default)
			# CONFIG_MUX_DIFF_P0N3 # A0-A3
			# CONFIG_MUX_DIFF_P1N3 # A1-A3
			# CONFIG_MUX_DIFF_P2N3 # A2-A3
		channel_A0_A1 = myAds.get_differential(myAds.CONFIG_MUX_DIFF_P0N1)
		channel_A0_A1_mV = myAds.get_differential_millivolts(myAds.CONFIG_MUX_DIFF_P0N1)


		print("A0: ", channel_A0, "(", channel_A0_mV, "mv)", end = '\t')
		print("A1: ", channel_A1, "(", channel_A1_mV, "mv)", end = '\t')
		print("A0-A1: ", channel_A0_A1, "(", channel_A0_A1_mV, "mv)")
		# No delay, go as fast as possible, only slowed by the time it takes to print()

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 7")
		sys.exit(0)