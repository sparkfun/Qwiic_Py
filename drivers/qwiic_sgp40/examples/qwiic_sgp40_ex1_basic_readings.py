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
import qwiic_i2c
import sys


print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Example 1\n")
my_sgp40 = qwiic_sgp40.QwiicSGP40()

print("\nWaiting 10 seconds for the SGP40 to warm-up.")
if not my_sgp40.begin():
	print("\nThe Qwiic SGP40 isn't connected to the system or failed its self test. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

print("\nSGP40 ready!")

while True:

	print("\nVOC Index is: " + str(my_sgp40.get_voc_index()))

	qwiic_i2c.delay_ms(1000)
