#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex6_qwiic_adxl313_interrupt.py
#
# Simple Example for the Qwiic ADXL313 DeviceSet that shows how to setup a interrupt on the ADXL313.
# Note, for this example we will setup the interrupt and poll the interrupt register
# via software.
# We will utilize the autosleep feature of the sensor.
# When it senses inactivity, it will go to sleep.
# When it senses new activity, it will wake up and trigger the INT1 pin.
# We will monitor the status of the interrupt by continuing to read the 
# interrupt register on the device.

# ///// Autosleep setup //////
# First, setup THRESH_INACT, TIME_INACT, and participating axis.
# These settings will determine when the unit will go into autosleep mode and save power!
# We are only going to use the x-axis (and are disabling y-axis and z-axis).
# This is so you can place the board "flat" inside your project,
# and we can ignore gravity on z-axis.

# ///// Interrupt setup //////
# Enable activity interrupt.
# Map activity interrupt to "int pin 1".
# This harware interrupt pin setup could be monitored by a GPIO on the raspi,
# or external system, however, for this example, we will simply
# poll the interrupt register via software to monitor its status.
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, October 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
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
#==================================================================================
# Example 6
#

from __future__ import print_function
import qwiic_adxl313
import time
import sys

def runExample():

	print("\nSparkFun Adxl313  Example 6 - Setup Autosleep and interrupts, then only print values when it's awake.\n")
	myAdxl = qwiic_adxl313.QwiicAdxl313()

	if myAdxl.connected == False:
		print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Device connected successfully.")        
  
	myAdxl.standby()	# Must be in standby before changing settings.
						# This is here just in case we already had sensor powered and/or
						# configured from a previous setup.

	myAdxl.setRange(myAdxl.ADXL313_RANGE_4_G)

	# setup activity sensing options
	myAdxl.setActivityX(True)		# enable x-axis participation in detecting activity
	myAdxl.setActivityY(False)		# disable y-axis participation in detecting activity
	myAdxl.setActivityZ(False)		# disable z-axis participation in detecting activity
	myAdxl.setActivityThreshold(10)	# 0-255 (62.5mg/LSB)

	# setup inactivity sensing options
	myAdxl.setInactivityX(True)			# enable x-axis participation in detecting inactivity
	myAdxl.setInactivityY(False)		# disable y-axis participation in detecting inactivity
	myAdxl.setInactivityZ(False)		# disable z-axis participation in detecting inactivity
	myAdxl.setInactivityThreshold(10)	# 0-255 (62.5mg/LSB)
	myAdxl.setTimeInactivity(5)			# 0-255 (1sec/LSB)

	# Interrupt Mapping
	# when activity of inactivity is detected, it will effect the int1 pin on the sensor
	myAdxl.setInterruptMapping(myAdxl.ADXL313_INT_ACTIVITY_BIT, myAdxl.ADXL313_INT1_PIN)
	myAdxl.setInterruptMapping(myAdxl.ADXL313_INT_INACTIVITY_BIT, myAdxl.ADXL313_INT1_PIN)

	myAdxl.ActivityINT(1)
	myAdxl.InactivityINT(1)
	myAdxl.DataReadyINT(0)

	myAdxl.autosleepOn()
	
	myAdxl.measureModeOn()

	# print int enable statuses, to verify we're setup correctly
	print("activity int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_ACTIVITY_BIT))
	print("inactivity int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_INACTIVITY_BIT))
	print("dataReady int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_DATA_READY_BIT))
	time.sleep(5)

	while True:
		myAdxl.updateIntSourceStatuses() # this will update all INTSOURCE statuses.
		
		if myAdxl.ADXL313_INTSOURCE_INACTIVITY:
			print("Inactivity detected.")
			time.sleep(1)
		if myAdxl.ADXL313_INTSOURCE_DATAREADY:
			myAdxl.readAccel() # read all axis from sensor, note this also updates all instance variables
			print(\
			 '{: 06d}'.format(myAdxl.x)\
			, '\t', '{: 06d}'.format(myAdxl.y)\
			, '\t', '{: 06d}'.format(myAdxl.z)\
			)
		else:
			print("Device is asleep (dataReady is reading false)")
		time.sleep(0.05)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


