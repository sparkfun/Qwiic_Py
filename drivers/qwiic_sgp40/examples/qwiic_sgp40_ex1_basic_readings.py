# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_sgp40_ex1.py
#
# Simple example to get VOC index
# ----------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
#
# This python library supports the SparkFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatable) single board 
# computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
# ======================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================
# Example 1

import qwiic_sgp40
import time
import sys

def run_example():

	print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Example 1\n")
	my_sgp40 = qwiic_sgp40.QwiicSGP40()
	
	if my_sgp40.begin() != 0:
		print("\nThe Qwiic SGP40 isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	
	print("\nSGP40 ready!")
	
	while True:
		
		print("\nVOC Index is: " + str(my_sgp40.get_VOC_index()))
		
		time.sleep(1)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
