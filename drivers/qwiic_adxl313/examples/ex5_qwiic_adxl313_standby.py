#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex5_qwiic_adxl313_standby.py
#
# Simple Example for the Qwiic ADXL313 DeviceSet that Shows how to switch the sensor 
# between stanby mode and measure mode.
# This example will put the device in measure mode and print 100 readings to terminal,
# Then enter standby mode for 5 seconds.
# Then loop.
# Note, the typical current required in each mode is as follows:
# Standby: 0.1uA
# Measure: 55-170uA
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
# Example 5
#

from __future__ import print_function
import qwiic_adxl313
import time
import sys

def runExample():

	print("\nSparkFun Adxl313  Example 5 - Standby mode and measure mode.\n")
	myAdxl = qwiic_adxl313.QwiicAdxl313()

	if myAdxl.connected == False:
		print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Device connected successfully.")        

	while True:
		# enter measure mode
		print("Entering measure mode.")
		myAdxl.measureModeOn()
		for i in range(100):
			
			myAdxl.updateIntSourceStatuses(); # this will update all INTSOURCE statuses.
		
			if myAdxl.ADXL313_INTSOURCE_DATAREADY:
				myAdxl.readAccel() # read all axis from sensor, note this also updates all instance variables
				print(\
				'{: 06d}'.format(myAdxl.x)\
				, '\t', '{: 06d}'.format(myAdxl.y)\
				, '\t', '{: 06d}'.format(myAdxl.z)\
				)
			else:
				print("Waiting for data.")
			time.sleep(0.05)
		print("Endering Standby Mode")
		myAdxl.standby()
		time.sleep(5) # 5 seconds of standby... really saving power during this time (0.1uA)
        

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


