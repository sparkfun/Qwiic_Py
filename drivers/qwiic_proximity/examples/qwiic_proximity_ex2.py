#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_proximity_ex2.py
#
# Simple Example for the Qwiic Proximity Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
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
# Example 2 - Is something there
#

from __future__ import print_function
import qwiic_proximity
import time
import sys

def runExample():

	print("\nSparkFun Proximity Sensor VCN4040 Example 2\n")
	oProx = qwiic_proximity.QwiicProximity()

	if oProx.connected == False:
		print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# begin Setup
	oProx.begin()

	oProx.set_led_current(200)
	oProx.set_prox_integration_time(8) # 1 to 8 is valid

  	# Take 8 readings and average them
	startingProxValue=0
	for x in range(8):
		startingProxValue += oProx.get_proximity()

	startingProxValue /= 8

	deltaNeeded = startingProxValue * 0.05 # Look for %5 change
	if deltaNeeded < 5:
		deltaNeeded = 5   # set a min value

	# Begin operation loop
	nothingThere = True

	while True:
		proxValue = oProx.get_proximity()
		print("Proximity Value: %d" % proxValue)

		if proxValue > startingProxValue + deltaNeeded:
			nothingThere = False
			print("\tSomething is there!")

		elif not nothingThere:
			print("\tI don't see anything")

			nothingThere=True

		time.sleep(.4)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 2")
		sys.exit(0)


