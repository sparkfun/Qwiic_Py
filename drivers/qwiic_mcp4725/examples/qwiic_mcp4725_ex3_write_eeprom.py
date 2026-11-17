#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp4725_ex3_write_eeprom.py
#
# This example writes the DAC and EEPROM With a single command.
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
	print("\nQwiic Template Example 3 - Write EEPROM\n")

	# Create instance of device
	myDac = qwiic_mcp4725.QwiicMCP4725()

	# Check if it's connected
	if myDac.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myDac.begin()
	
	# The MCP4725 has an EEROM that can store a single 12-bit DAC value as well 
	# as two configuration bits for the power down mode. The DAC will output this 
	# value on reset or power-cycle. 
	print("Writing 2048 to DAC EEPROM")
	myDac.write_dac_eeprom(2048); # ~1.65 V if VDD = 3.3V

	# Now, you can unplug the DAC from your controller and plug it back in, 
	# and you will see that the value we wrote persists even after a power-cycle.
	print("Value written to EEPROM, value should persist after power-cycle")

	return
	
if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)