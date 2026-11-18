#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_dual_encoder_reader_ex1_read_counts.py
#
# Simple Example demonstrating how to read encoder counts for the Qwiic Dual Encoder Reader (as part of the SparkFun Auto pHAT)
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

import qwiic_dual_encoder_reader
import qwiic_i2c
import sys

def run_example():

	print("\nSparkFun Qwiic Dual Encoder Reader Example 1\n")
	my_encoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

	if my_encoders.is_connected() == False:
		print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	my_encoders.begin()

	while True:

		print("Count1: %d, Count2: %s" % (my_encoders.get_count1(), \
			my_encoders.get_count2(), \
			))

		qwiic_i2c.delay_ms(300)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example 1")
		sys.exit(0)


