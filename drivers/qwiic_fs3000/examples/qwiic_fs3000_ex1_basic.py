#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_fs3000_ex1_basic.py
#
#   Read values of air velocity from the FS3000 sensor, print them to terminal.
#   Prints raw data, m/s and mph.
#   Note, the response time on the sensor is 125ms.
#
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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
#===============================================================================

import qwiic_fs3000
import sys
import time

def runExample():
	print("\nQwiic Template Example 1 - Basic\n")

	# Create instance of device
	myFS3000 = qwiic_fs3000.QwiicFS3000() 

	# Check if it's connected
	if myFS3000.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myFS3000.begin()

	# Set the range to match which version of the sensor you are using.
	# FS3000-1005 (0-7.23 m/sec) --->>>  kAirflowRange7Mps
	# FS3000-1015 (0-15 m/sec)   --->>>  kAirflowRange15Mps
	myFS3000.set_range(myFS3000.kAirflowRange7Mps)
		
	while True:
		# Read the sensor
		raw = myFS3000.read_raw()
		m_s = myFS3000.read_meters_per_second()
		mph = myFS3000.read_miles_per_hour()
		
		if raw == -1 or m_s == -1 or mph == -1:
			continue # -1 indicates an error
		
		print("FS3000 Readings \tRaw: ", raw, end="")
		print("\tm/s: ", m_s, end="")
		print("\tmph:", mph)

		time.sleep(1)  # note, response time on the sensor is 125ms

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)