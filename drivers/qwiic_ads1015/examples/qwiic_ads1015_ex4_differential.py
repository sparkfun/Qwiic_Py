#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ads1015_ex4_differential.py
#
#   This example shows how to output ADC values on one differential input between A0 and A1.
#   *at default gain setting of 1 (and 3.3V VCC), 0-2V will read 0-2047.
#   *anything greater than 2V will read 2047.
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
	print("\nQwiic ADS1015 Example 4 - Differential\n")

	myAds = qwiic_ads1015.QwiicADS1015()

	# Check if it's connected
	if myAds.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myAds.begin()

	while True:
		input = myAds.get_differential() # default (i.e. no arguments)
  		
		# Optional "commented out" examples below show how to read differential readings between other pins
		# input = myAds.get_differential(myAds.kConfigMuxDiffP0N3)
		# input = myAds.get_differential(myAds.kConfigMuxDiffP1N3)
		# input = myAds.get_differential(myAds.kConfigMuxDiffP2N3)

		print("Differential: ", input)
		time.sleep(0.30)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 4")
		sys.exit(0)