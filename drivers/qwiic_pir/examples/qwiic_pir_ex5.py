#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_pir_ex5.py
#
# Simple Example to change the I2C address of the Qwiic PIR Device
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, March 2021
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
# Example 5
#

from __future__ import print_function
import qwiic_pir
import time
import sys

def run_example():

	print("\nSparkFun Qwiic PIR  Example 5\n")
	my_PIR = qwiic_pir.QwiicPIR()

	if my_PIR.begin() == False:
		print("The Qwiic PIR isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	print("\nEnter a new I2C address for the Qwiic PIR to use.")
	print("\nDon't use the 0x prefix. For instance, if you wanted to")
	print("\nchange the address to 0x5B, you would type 5B and hit enter.")
	
	new_address = input("\nNew address: ")
	# Change to hex
	new_address = int(new_address, 16)
	
	# Check if the user entered a valid address
	if new_address > 0x08 and new_address < 0x77:
		print("\nCharacters received and new address valid!")
		print("\nAttempting to set Qwiic PIR to new address...")
		
		my_PIR.set_I2C_address(new_address)
		print("\nAddress successfully changed!")
		
		# Check that the Qwiic PIR acknowledges on the new address
		time.sleep(0.02)
		if my_PIR.begin() == False:
			print("\nThe Qwiic PIR is not connected to the system. Please check you're connection", \
				file=sys.stderr)
				
		else:
			print("\nPIR acknowledged on new address!")
	
	else:
		print("\nAddress entered not valid I2C address.")

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 5")
		sys.exit(0)
