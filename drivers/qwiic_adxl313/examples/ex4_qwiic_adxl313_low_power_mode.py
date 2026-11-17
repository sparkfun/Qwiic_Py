#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex4_qwiic_adxl313_low_power_mode.py
#
#   Shows how to use Low Power feature. 
#   In addition to turning on low power mode, you will also want to consider
#   bandwidth rate. This will affect your results in low power land.
#   In this example, we will turn on low power mode and set BW to 12.5Hz.
#   Then we will only take samples at or above 12.5Hz (so we don't miss samples)
#
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
# Example 4
#

from __future__ import print_function
import qwiic_adxl313
import time
import sys

def runExample():

	print("\nSparkFun Adxl313  Example 4 - Low power mode ON with 12.5Hz bandwidth.\n")
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

	myAdxl.lowPowerOn()
	#also try:
	#myAdxl.lowPower = True

	myAdxl.setBandwidth(myAdxl.ADXL313_BW_12_5)
	#also try:
	#myAdxl.bandwidth = myAdxl.ADXL313_BW_12_5
	
	#12.5Hz is the best power savings.
	#Other options possible are the following.
	#Note, bandwidths not listed below do not cause power savings.
	#ADXL313_BW_200		    (115uA in low power)
	#ADXL313_BW_100		    (82uA in low power)
	#ADXL313_BW_50		    (64uA in low power)
	#ADXL313_BW_25		    (57uA in low power)
	#ADXL313_BW_12_5	    (50uA in low power)
	#ADXL313_BW_6_25		  (43uA in low power)

	myAdxl.measureModeOn()

	while True:
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
		time.sleep(0.08)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 4")
		sys.exit(0)
