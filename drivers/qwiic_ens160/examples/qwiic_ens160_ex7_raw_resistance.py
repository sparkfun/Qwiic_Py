#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_template_ex7_raw_resistance.py
#
#  This example retreieves the raw resistance of the plates. This would be used
#  in the case that you want to process these values yourself.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, October 2024
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

import qwiic_ens160
import sys
from time import sleep

def runExample():
	# TODO Replace template and title
	print("\nQwiic ENS160 Example 7 - Raw Resistance\n")

	# Create instance of device
	myEns = qwiic_ens160.QwiicENS160()

	# Check if it's connected
	if myEns.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myEns.begin()

	myEns.set_operating_mode(myEns.kOpModeReset)

	sleep(0.1)

	# Set to standard operation
	# Others include kOpModeDeepSleep and kOpModeIdle
	myEns.set_operating_mode(myEns.kOpModeStandard)
	
	# There are four values here: 
	# 0 - Operating ok: Standard Operation
	# 1 - Warm-up: occurs for 3 minutes after power-on.
	# 2 - Initial Start-up: Occurs for the first hour of operation.
	# 	  and only once in sensor's lifetime.
	# 3 - No Valid Output

	ensStatus = myEns.get_flags()
	print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): ", ensStatus)
	
	while True:
		if myEns.check_data_status():
			res_value = myEns.get_raw_resistance()
			print("Resistance Value: ", res_value)
		
		sleep(0.2)
	
if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)