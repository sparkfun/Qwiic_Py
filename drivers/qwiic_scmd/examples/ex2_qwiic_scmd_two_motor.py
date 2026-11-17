#!/usr/bin/env python
#-----------------------------------------------------------------------------
# A simple test to speed up and slow down both motors in opposite directions.
#------------------------------------------------------------------------
#
# Written by Mark Lindemer
# SparkFun Electronics, April 2020
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

import time
import sys
import math
import qwiic_scmd

myMotor = qwiic_scmd.QwiicScmd()

def runExample():
	print("Motor Test.")
	R_MTR = 0
	L_MTR = 1
	FWD = 0
	BWD = 1

	if myMotor.connected == False:
		print("Motor Driver not connected. Check connections.", \
			file=sys.stderr)
		return
	myMotor.begin()
	print("Motor initialized.")
	time.sleep(.250)
	
	# Zero Motor Speeds
	myMotor.set_drive(0,0,0)
	myMotor.set_drive(1,0,0)
	
	myMotor.enable()
	print("Motor enabled")
	time.sleep(.250)


	while True:
		speed = 20
		for speed in range(20,255):
			print(speed)
			myMotor.set_drive(R_MTR,FWD,speed)
			myMotor.set_drive(L_MTR,BWD,speed)
			time.sleep(.05)
		for speed in range(254,20, -1):
			print(speed)
			myMotor.set_drive(R_MTR,FWD,speed)
			myMotor.set_drive(L_MTR,BWD,speed)
			time.sleep(.05)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("Ending example.")
		myMotor.disable()
		sys.exit(0)
