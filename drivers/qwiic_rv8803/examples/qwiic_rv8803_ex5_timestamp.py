#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_rv8803_ex5_timestamp.py
#
# This example shows how to get the timestamp of an event generated on the EVI pin, by a button press on the RTC.
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

import qwiic_rv8803
import sys
import time

def runExample():
	print("\nQwiic RV8803 Example 5 - Timestamp\n")

	# Create instance of device
	myRTC = qwiic_rv8803.QwiicRV8803()

	# Check if it's connected
	if myRTC.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myRTC.begin()

	# Configure EVI event capture with button debounce so we can catch button presses on the RTC
	myRTC.set_evi_event_capture(True)
	myRTC.set_evi_debounce_time(myRTC.kEviDebounce256Hz)

	while True:
		if myRTC.get_interrupt_flag(myRTC.kFlagEvi):
			myRTC.update_time()
			myRTC.clear_interrupt_flag(myRTC.kFlagEvi)
			print ("Current Time: ", end="")
			print (myRTC.string_date_usa(), end="")
			# get timestamp
			print (" ", myRTC.string_timestamp())

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)