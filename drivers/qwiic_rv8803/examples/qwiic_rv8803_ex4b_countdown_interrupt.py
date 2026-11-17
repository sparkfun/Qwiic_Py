#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_rv8803_ex4b_countdown_interrupt.py
#
# This example shows how to generate a periodic interrupt signal, 
# as well as show you how to calculate the proper set up values for your necessary time.
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

# These helper functions are just to provide us with a platform-independent way to get the current time in microseconds (from our microcontroller, not the RTC)
# The CircuitPython time module has time.monotonic_ns()
# The MicroPython time module has time.time_ns()
# RasPi time module has both

def check_has_monotonic_ns():
	try:
		time.monotonic_ns()
		return True 
	except AttributeError:
		return False
	
def get_microseconds(use_monotonic_ns):
	if use_monotonic_ns:
		return time.monotonic_ns() // 1000 # works in CircuitPython and RasPi
	else:
		return time.time_ns() // 1000 # only works in MicroPython

def runExample():
	print("\nQwiic RV8803 Example 4b - Countdown Interrupt\n")

	# First we'll check if the time module for current platform has the monotonic_ns() function
	useMono = check_has_monotonic_ns()

	# Create instance of device
	myRTC = qwiic_rv8803.QwiicRV8803()

	# Check if it's connected
	if myRTC.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myRTC.begin()

	# To configure a periodic interrupt, we'll need to do some math to figure out how to set our registers. 
	# We are able to change how many clock ticks we want to count (0-4095), and also the length of each clock tick. 
	# (4 options: 4096 Hz, 64 Hz, 1 Hz, 1/60 Hz)

	#   The time ranges covered by each freqeuncy setting are as follows
	#   4096 Hz: 244.14 uS - .9998 Second;                            244.14 uS per LSB             COUNTDOWN_TIMER_FREQUENCY_4096_HZ
	#   64 Hz: 15.625 mS - 63.984 Seconds;                            15.625 mS per LSB             COUNTDOWN_TIMER_FREQUENCY_64_HZ
	#   1 Hz: 1 Second - 4095 Seconds (68 minutes 16 seconds);        1 Second per LSB              COUNTDOWN_TIMER_FREQUENCY_1_HZ
	#   1/60 Hz: 1 Minute = 4095 Minutes (68 hours 16 minutes)        1 Minute per LSB              COUNTDOWN_TIMER_FREQUENCY_1_60TH_HZ

	# As an example, we'll configure a ~3.5 second interrupt. 
	# We'll choose 60 Hz as our frequency as we want something > 1 second, 
	# but still want enough granularity to fire an interrupt at 3.5 seconds, not 3 or 4.
	# Since the resolution for this setting is 15.625 mS per LSB, we'll convert 3.5 seconds to 3500 ms. 
	# We'll then simply divide the time we want by the resolution to get the number of clock ticks we need to wait to fire the interrupt
	# 3500 / 15.625 = 224 Clock ticks

	myRTC.disable_all_interrupts()
	myRTC.clear_all_interrupt_flags() # Clear all flags in case any interrupts have occurred.
	myRTC.set_countdown_timer_frequency(myRTC.kCountdownTimerFrequency64Hz)
	myRTC.set_countdown_timer_clock_ticks(224)
	myRTC.enable_hardware_interrupt(myRTC.kTimerInterrupt)
	myRTC.set_countdown_timer_enable(True) # This will start the timer on hte last clock tick of the I2C transaction
	lastInterruptTime = get_microseconds(useMono)

	while True:
		if myRTC.get_interrupt_flag(myRTC.kFlagTimer):
			timeSinceLastInterrupt = get_microseconds(useMono) - lastInterruptTime
			lastInterruptTime = get_microseconds(useMono)
			myRTC.clear_interrupt_flag(myRTC.kFlagTimer)
			print("Timer Interrupt Triggered! Time since last interrupt: ", timeSinceLastInterrupt, " uS")

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)
