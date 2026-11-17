#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_bmp581_ex7_nvm.py
#
# This example demonstrates how to read basic temperature and pressure values from the Qwiic BMP581
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

import qwiic_bmp581
import sys
import time


# Data to write into the NVM. In this case we're going to store some
# characters, but any 6 bytes of data can be stored
dataToWrite = "Hello!"

def runExample():
	print("\nQwiic Template Example 7 - NVM\n")

	# Create instance of device
	myBMP581 = qwiic_bmp581.QwiicBMP581()

	# Check if it's connected
	if myBMP581.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	# Initialize the device
	if myBMP581.begin() == False:
		print("Unable to Initialize device! Please check your connection and try again.", file=sys.stderr)
		return
	
	print("BMP581 connected!")

	print ("Writing data to NVM:", dataToWrite)
	# The BMP581 contains non-volatile memory (NVM) that is primarily used for
    # calibration data internally by the sensor. However 6 bytes are user programmable,
    # stored in 3 2-byte locations (0x20 - 0x22).
	dataIndex = 0
	for addr in range(myBMP581.kNvmStartAddr, myBMP581.kNvmEndAddr + 1):
		data = ord(dataToWrite[dataIndex]) | (ord(dataToWrite[dataIndex + 1]) << 8)
		myBMP581.nvm_write(addr, data) 
		dataIndex += 2

	print("Data read back from NVM:")

	# Now we can read back the data and display it
	for addr in range(myBMP581.kNvmStartAddr, myBMP581.kNvmEndAddr + 1):
		data = myBMP581.nvm_read(addr)
		print(chr(data & 0xFF), end='')
		print(chr((data >> 8) & 0xFF), end='')

	return

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)