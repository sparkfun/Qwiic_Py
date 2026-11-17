#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_scd4x_ex7_test_and_reset.py
#
# This example shows how to perform a self test and factory reset on the SCD4x sensor.
# 
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

import qwiic_scd4x
import sys
import time

def runExample():
	print("\nQwiic SCD4x Example 7 - Self Test and Factory Reset\n")

	# Create instance of device
	mySCD4x = qwiic_scd4x.QwiicSCD4x() 

	# Check if it's connected
	if mySCD4x.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	# Initialize the device
	if mySCD4x.begin() == False:
		print("Error while initializing device", file=sys.stderr)
		return
	
	# We need to stop periodic measurements before we can change the sensor signal compensation settings
	mySCD4x.stop_periodic_measurement()
	print("Periodic measurements stopped")

	# Now we can run the self test:
	print("Starting the self-test. This will take 10 seconds to complete...")
	if mySCD4x.perform_self_test() == True:
		print("Self-test passed!")
	else:
		print("Self-test failed!", file=sys.stderr)
		return
	
	# We can do a factory reset if we want to completely reset the sensor
	if mySCD4x.perform_factory_reset() == True:
		print("Factory reset completed!")
	else:
		print("Factory reset failed!", file=sys.stderr)
		return

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)