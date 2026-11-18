#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_rv8803_ex4c_periodic_interrupt.py
#
# This example shows how to generate a periodic 1s interrupt pulse
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
import qwiic_i2c

def run_example():
	print("\nQwiic RV8803 Example 4c - Periodic Interrupt\n")

	# Create instance of device
	myRTC = qwiic_rv8803.QwiicRV8803()

	# Check if it's connected
	if myRTC.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myRTC.begin()

	myRTC.disable_all_interrupts()
	myRTC.clear_all_interrupt_flags() # Clear all flags in case any interrupts have occurred.
	myRTC.set_periodic_time_update_frequency(myRTC.TIME_UPDATE_1_SECOND) # Another option is TIME_UPDATE_1_MINUTE
	myRTC.enable_hardware_interrupt(myRTC.UPDATE_INTERRUPT)
	lastInterruptTime = qwiic_i2c.ticks_ms() # Time from our microcontroller, not the RTC

	while True:
		if myRTC.get_interrupt_flag(myRTC.FLAG_UPDATE):
			now = qwiic_i2c.ticks_ms()
			timeSinceLastInterrupt = qwiic_i2c.ticks_diff(now, lastInterruptTime)
			lastInterruptTime = now
			myRTC.clear_interrupt_flag(myRTC.FLAG_UPDATE)
			print("Periodic 1s interrupt triggered. Time since last interrupt: ", timeSinceLastInterrupt, " ms")

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)
