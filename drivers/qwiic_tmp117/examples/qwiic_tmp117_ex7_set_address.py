#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_tmp117_ex7_set_address.py
#
# This script allows the user to change the address of the device and to
# change the Wire port for I2C Communications. The address can be physically
# changed with an external jumper on the back of the sensor. 
# 
# See the "Address Select" section in the hookup guide for more information:
# https://learn.sparkfun.com/tutorials/qwiic-tmp117-high-precision-digital-temperature-sensor-hookup-guide
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

import qwiic_tmp117
import sys
import time

def runExample():
	print("\nQwiic TMP117 Example 7 - Set Address\n")

	# The default address of the device is 0x48, but it can be changed to any of the following:
	# 0x48, 0x49, 0x4A, or 0x4B
	# The address can be changed by cutting the default address trace and 
	# applying a solder jumper to the back of the device
	# See the hookup guide for more information on applying a solder jumper for address selection

	# Once your address has been physically changed, you must pass this address to instantiations of 
	# the QwiicTMP117 class as seen below:

	# Put your desired address (0x48-0x4B) here:
	newAddress = 0x48

	# Create instance of device
	myTMP117 = qwiic_tmp117.QwiicTMP117(address=newAddress)

	# Check if it's connected
	if myTMP117.is_connected() == False:
		print("The device isn't connected to the system, or your supplied address does not align with the current jumper configuration.", \
			file=sys.stderr)
		print("Please check your connection and the address jumper on the back of the device.", \
			file=sys.stderr)
		return
	
	# Initialize the device
	myTMP117.begin()

	print("New Device Address:", hex(myTMP117.get_address()))
	return

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)