#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp4725_ex5_power_down.py
#
# This example demonstrates how to enter and leave power down mode on the MCP4725 DAC.
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
	print("\nQwiic Template Example 5 - Power Down\n")

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
		# We'll start by writing 3.3V to the DAC in normal mode
		print("Writing 3.3V to DAC")
		# By default, the write_dac() function will write to the DAC in normal mode if no mode is specified.
		myDac.write_dac(4095)  # ~3.3 V if VDD = 3.3V.
		
		time.sleep(2)

		# Now, we will put the dac in power down mode.
		# This will reduce the current consumption of the DAC to ~60nA (typical).
		# The DAC will not output any voltage in power down mode, but it can still receive I2C commands.
		# The output stage will switch from an amplifier output to a known resistive load (1k, 100k, or 500k).
		# To wake the DAC from power down mode, write a value to the DAC, with normal mode enabled.
		# See datasheet pg. 20
		print("Entering Power Down Mode...")
		myDac.write_dac(2048, myDac.kPowerDownMode100K)  # Note, it doesn't matter what value we write here, the DAC will stop performing conversions
		time.sleep(2)

		print("Writing to the DAC in Power Down Mode (will not output conversion)...")
		myDac.write_dac(4095, myDac.kPowerDownMode100K)  # We won't see the voltage we expect, as the DAC is still in power down mode

		time.sleep(2)

		# Now by issuing a write_dac command with normal mode enabled, we will wake the DAC from power down mode and again will see the value expected
		print("Writing 0.825V to DAC")
		myDac.write_dac(1024, myDac.kPowerDownModeNormal)  # ~0.825V if VDD = 3.3V
		
		time.sleep(2)
			

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)