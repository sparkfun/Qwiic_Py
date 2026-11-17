#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_pir_ex2.py
#
# Simple Example for the Qwiic PIR Device
#------------------------------------------------------------------------
#
# Written by Andy England @ SparkFun Electronics, January 2021
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
# Copyright (c) 2021 SparkFun Electronics
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
# Example 2
#

from __future__ import print_function
import qwiic_pir
import time
import sys

def run_example():

	print("\nSparkFun Qwiic PIR  Example 2\n")
	my_PIR = qwiic_pir.QwiicPIR()

	if my_PIR.begin() == False:
		print("The Qwiic PIR isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	print ("Waiting 30 seconds for PIR to stabilize")
	for i in range(0, 30):
		print(i)
		time.sleep(1)

	print("Device Stable")

	while True:
		if my_PIR.available() is True:
			if my_PIR.object_detected():
				print("Object Detected")
			if my_PIR.object_removed():
				print("Object Removed")
			my_PIR.clear_event_bits()
		time.sleep(0.2)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 2")
		sys.exit(0)
