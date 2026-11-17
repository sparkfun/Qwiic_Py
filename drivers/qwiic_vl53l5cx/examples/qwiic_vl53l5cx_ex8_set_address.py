#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_vl53l5cx_ex8_set_address.py
#
# This example shows how to set a custom address for the VL53L5CX.
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

import qwiic_vl53l5cx 
import sys
from math import sqrt
import time

def runExample():
	print("\nQwiic VL53LCX Example 8 - Set Address\n")

	# Create instance of device
	myVL53L5CX = qwiic_vl53l5cx.QwiicVL53L5CX() 

	# Check if it's connected
	if myVL53L5CX.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	# Initialize the device
	print ("Initializing sensor board. This can take up to 10s. Please wait.")
	if myVL53L5CX.begin() == False:
		print("Sensor initialization unsuccessful. Exiting...", file=sys.stderr)
		sys.exit(1)

	# Set the address of the sensor
	newAddress = 0x44 # You can change this to any value in the range 0x08 <= newAddress <= 0x77
	print("Press any key, followed by enter to set the address of the sensor to:", hex(newAddress))
	input()
	if myVL53L5CX.set_i2c_address(newAddress) == False:
		print("Failed to set address. Exiting...", file=sys.stderr)
		sys.exit(1)
	
	print("Sensor address is now:", hex(myVL53L5CX.get_i2c_address()))
	
	myVL53L5CX.set_resolution(8*8) # enable all 64 pads
	image_resolution = myVL53L5CX.get_resolution()  # Query sensor for current resolution - either 4x4 or 8x8

	image_width = int(sqrt(image_resolution)) # Calculate printing width
	myVL53L5CX.start_ranging()

	while True:
		if myVL53L5CX.check_data_ready():
			measurement_data = myVL53L5CX.get_ranging_data()
			for y in range (0, (image_width * (image_width - 1) )+ 1, image_width):
				for x in range (image_width - 1, -1, -1):
					print("\t", end="")
					print(measurement_data.distance_mm[x + y], end = "")
				print("\n")
			print("\n")
		
		time.sleep(0.005)
	
if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)