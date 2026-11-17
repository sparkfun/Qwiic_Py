#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp4725_ex1_basic.py
#
# This example writes the DAC with three example voltages: 0V, 1.65V, and 3.3V
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
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

import qwiic_mcp4725
import sys
import time

def runExample():
	print("\nQwiic Template Example 1 - Basic\n")

	# Create instance of device
	myDac = qwiic_mcp4725.QwiicMCP4725()

	# Check if it's connected
	if myDac.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myDac.begin()
	
	while True:
		# This loop will write three different voltages to the DAC with 
		# 2 second delays in between each write, so you can see the voltage
		# change on the output with a multimeter or oscilloscope.
		
		# The full range of the 12-bit DAC is 0-4095, which corresponds to VSS (Ground) to VDD (3.3V). 
		# The equation for output voltage is (see datasheet pg. 19): VDD * (DAC Value / 4096)

		print("Writing 0V to DAC")
		myDac.write_dac(0)  # ~0V if VDD = 3.3V
		
		time.sleep(2)

		print("Writing 1.65V to DAC")
		myDac.write_dac(2048)  # ~1.65 V if VDD = 3.3V

		time.sleep(2)

		print("Writing 3.3V to DAC")
		myDac.write_dac(4095)  # ~3.3 V if VDD = 3.3V
		
		time.sleep(2)
	

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)