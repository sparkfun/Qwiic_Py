#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_rv8803_ex6_fine_tuning.py
#
# This example shows how to calibrate the RTC's oscillator to have it keep even more accurate time
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
	print("\nQwiic RV8803 Example 6 - Fine Tuning\n")

	# Create instance of device
	myRTC = qwiic_rv8803.QwiicRV8803()

	# Check if it's connected
	if myRTC.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myRTC.begin()

	# We now must measure the frequency on the Clock Out carefully to calibrate our crystal. To start generating a signal on Clock Out, tie CLKOE High.
 	# Change measuredFrequency accordingly, note that you can only correct +/-7.6288 ppm
	myRTC.set_calibration_offset(0) # zero out any previous calibration
	myRTC.set_clock_out_timer_frequency(myRTC.kClockOutFrequency1Hz) # set the clock out to 1Hz square wave
	measuredFrequency = 1.0000012 # measured frequency in HZ (CHANGE THIS TO YOUR MEASURED VALUE)
	newPPM = (measuredFrequency - 1) * 1000000 # Calculate PPM difference between measuredFrequency and our desired 1 Hz wave
	# myRTC.set_calibration_offset(newPPM) # Uncomment this line after you have changed the value of measuredFrequency to load the new calibration into the RTC
	print("Tie CLKOE high to measure the frequency on the Clock Out pin.")
	print("Measure the frequency and input it into measuredFrequency in this calibration script.")
	print("Then uncomment the line to set the calibration offset to the new value.")
	
	# Wait forever (until user interrupts the program) so we can manually measure the square wave
	while True:
		pass

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)