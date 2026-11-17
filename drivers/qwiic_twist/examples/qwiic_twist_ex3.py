#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_twist_ex3.py
#
# Simple Example for the Qwiic Twist Device
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
# Example 1
#

import qwiic_twist
import time
import sys

def runExample():

	print("\nSparkFun qwiic Twist   Example 3\n")
	myTwist = qwiic_twist.QwiicTwist()

	if myTwist.connected == False:
		print("The Qwiic twist device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myTwist.begin()

	myTwist.set_color(255/2, 0, 255/2) #Set Red and Blue LED brightnesses to half of max.

	myTwist.connect_red = -10  # Red LED will go down 10 in brightness with each encoder tick
	myTwist.connect_blue = 10 #Blue LED will go up 10 in brightness with each encoder tick

	while True:

		print("Count: %d, Pressed: %s" % (myTwist.count, \
			"YES" if myTwist.pressed else "NO", \
			))

		time.sleep(.3)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


