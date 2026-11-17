#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_rv8803_ex4a_alarm_interrupt.py
#
# This example shows how to set an alarm and make the RTC generate an interrupt when the clock time matches the alarm time.
# The INT pin will be high (~3.3V) until real time matches alarm time when it will go low (~0V).
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

# Make sure to change these values to the decimal values that you want to match
minuteAlarmValue = 55  # 0-60, change this to a minute or two from now to see the alarm get generated
hourAlarmValue = 0  # 0-24
weekdayAlarmValue = qwiic_rv8803.QwiicRV8803.kSunday | qwiic_rv8803.QwiicRV8803.kSaturday  # Or together days of the week to enable the alarm on those days.
dateAlarmValue = 0  # 1-31

# Define which alarm registers we want to match, make sure you only enable weekday or date alarm, enabling both will default to a date alarm
# In its current state, an alarm will be generated once an hour, when the MINUTES registers on the time and alarm match. Setting minuteAlarmEnable to false would trigger an alarm every minute
minuteAlarmEnable = True
hourAlarmEnable = False
weekdayAlarmEnable = False
dateAlarmEnable = False

def runExample():
	print("\nQwiic RV8803 Example 4a - Alarm Interrupt\n")

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
	myRTC.clear_all_interrupt_flags()
	#The alarm interrupt compares the alarm interrupt registers with the current time registers. We must choose which registers we want to compare by setting bits to true or false
	myRTC.set_items_to_match_for_alarm(minuteAlarmEnable, hourAlarmEnable, weekdayAlarmEnable, dateAlarmEnable)
	myRTC.set_alarm_minutes(minuteAlarmValue)
	myRTC.set_alarm_hours(hourAlarmValue)
	myRTC.set_alarm_weekday(weekdayAlarmValue)
	# myRTC.set_alarm_date(dateAlarmValue) # uncomment this line if you want to set a date alarm instead of weekday
	myRTC.enable_hardware_interrupt(myRTC.kAlarmInterrupt)

	while True:
		if myRTC.get_interrupt_flag(myRTC.kFlagAlarm):
			print("Alarm Triggered! Clearing flag...")
			myRTC.clear_interrupt_flag(myRTC.kFlagAlarm)
		else:
			myRTC.update_time()
			print("Waiting for alarm to trigger. Current Time: ", end="")
			print (myRTC.string_date_usa(), end="")
			print (" ", myRTC.string_time())

		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)