#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_tmp117_ex6_set_conv_cycle.py
#
# This script can set and get the Conversion Times in Continuous Conversion mode
# for the Sensor. A chart for the averaging modes and the conversion times can
# be found in the table below or in the Datasheet on page 27 table 7.
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

def conv_avg_mode_to_string(conv_avg_mode):
	if conv_avg_mode == qwiic_tmp117.QwiicTMP117.kConvAvgNone:
		return "No Averaging"
	elif conv_avg_mode == qwiic_tmp117.QwiicTMP117.kConvAvg8:
		return "8 Averaged Conversions"
	elif conv_avg_mode == qwiic_tmp117.QwiicTMP117.kConvAvg32:
		return "32 Averaged Conversions"
	elif conv_avg_mode == qwiic_tmp117.QwiicTMP117.kConvAvg64:
		return "64 Averaged Conversions"

def runExample():
	print("\nQwiic TMP117 Example 6 - Set Conversion Cycle Time\n")

	# Create instance of device
	myTMP117 = qwiic_tmp117.QwiicTMP117()

	# Check if it's connected
	if myTMP117.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myTMP117.begin()

	print("           Conversion Cycle Times in CC Mode      ")
	print("               AVG       0       1       2       3")
	print("       CONV  averaging  (0)     (8)     (32)   (64)")
	print("         0             15.5ms  125ms   500ms    1s")
	print("         1             125ms   125ms   500ms    1s")
	print("         2             250ms   250ms   500ms    1s")
	print("         3             500ms   500ms   500ms    1s")
	print("         4             1s      1s      1s       1s")
	print("         5             4s      4s      4s       4s")
	print("         6             8s      8s      8s       8s")
	print("         7             16s     16s     16s      16s")
	print("AVG = Conversion Average Mode")
	print("CONV = Conversion Cycle Bit\n")
	
	cm = myTMP117.get_conversion_average_mode()
	print("Current Conversion Average Mode:", cm, "(" + conv_avg_mode_to_string(cm) + ")")
	print("Current Conversion Cylcle Bit Value: ", myTMP117.get_conversion_cycle_bit())
	
	while True:
		print("\n\nSelect One of the following Options: ")
		print("1: Set Conversion Average Mode")
		print("2: Set Conversion Cycle Bit")
		print("Enter a number for one of the options above (1-2): ")
		option = int(input())
		
		if option == 1:
			print("Current Conversion Average Mode:", conv_avg_mode_to_string(myTMP117.get_conversion_average_mode()))
			print ("\nSelect One of the Following Averaging Modes:")
			print("0: No Averaging")
			print("1: 8 Averaged Conversions")
			print("2: 32 Averaged Conversions")
			print("3: 64 Averaged Conversions")
			print("Enter a number for one of the options above (0-3): ")
			avgMode = int(input())
			if avgMode not in [0, 1, 2, 3]:
				print("Invalid option. Please enter a number between 0 and 3.")
				continue
			myTMP117.set_conversion_average_mode(avgMode)
			print("New Conversion Average Mode:", conv_avg_mode_to_string(myTMP117.get_conversion_average_mode()))

		if option == 2:
			print("Current Conversion Cycle Bit Value:", myTMP117.get_conversion_cycle_bit())
			print("Enter a number 0-7 for the Conversion Cycle Bit Value: ")
			convCycleBit = int(input())
			if convCycleBit < 0 or convCycleBit > 7:
				print("Invalid option. Please enter a number between 0 and 7.")
				continue
			myTMP117.set_conversion_cycle_bit(convCycleBit)
			print("New Conversion Cycle Bit Value:", myTMP117.get_conversion_cycle_bit())

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)