#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_vl53l5cx_ex6_settings.py
#
# This example shows how to read all 64 distance readings at once.
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
	print("\nQwiic VL53LCX Example 6 - Advanced Settings\n")

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

	myVL53L5CX.set_resolution(8*8) # enable all 64 pads
	image_resolution = myVL53L5CX.get_resolution()  # Query sensor for current resolution - either 4x4 or 8x8
	image_width = int(sqrt(image_resolution)) # Calculate printing width
	
	# Set the ranging mode
	if myVL53L5CX.set_ranging_mode(myVL53L5CX.kRangingModeAutonomous) != myVL53L5CX.kStatusOK:
		print("Failed to set ranging mode")
		sys.exit(1)

	# Check that the sensor has been set to the expected mode
	if myVL53L5CX.get_ranging_mode() != myVL53L5CX.kRangingModeAutonomous:
		print("Failed to read correct ranging mode")
		sys.exit(1)

	# Set device to sleep mode
	if myVL53L5CX.set_power_mode(myVL53L5CX.kPowerModeSleep) != myVL53L5CX.kStatusOK:
		print("Failed to set power mode to sleep")
		sys.exit(1)
	
	# Check that the sensor has been set to the expected mode
	if myVL53L5CX.get_power_mode() != myVL53L5CX.kPowerModeSleep:
		print("Failed to read correct power mode")
		sys.exit(1)
	else:
		print("Shhhh... device is sleeping!")
	
	print("Waking up device in 5...")
	time.sleep(1)
	print("4...")
	time.sleep(1)
	print("3...")
	time.sleep(1)
	print("2...")
	time.sleep(1)
	print("1...")
	time.sleep(1)

	if myVL53L5CX.set_power_mode(myVL53L5CX.kPowerModeWakeup) != myVL53L5CX.kStatusOK:
		print("Failed to set power mode to wake")
		sys.exit(1)
	
	# Check that the sensor has been set to the expected mode
	if myVL53L5CX.get_power_mode() != myVL53L5CX.kPowerModeWakeup:
		print("Failed to read correct power mode")
		sys.exit(1)
	else:
		print("Device is awake!")


	print("Current Integration Time:", myVL53L5CX.get_integration_time_ms(), "ms")

	if myVL53L5CX.set_integration_time_ms(8) != myVL53L5CX.kStatusOK:
		print("Failed to set integration time")
		sys.exit(1)
	
	# Check that the integration time has been set to the expected value
	print("New Integration Time:", myVL53L5CX.get_integration_time_ms(), "ms")

	# Set the sharpener value
	print("Current Sharpener Value:", str(myVL53L5CX.get_sharpener_percent()) + "%")

	if myVL53L5CX.set_sharpener_percent(19) != myVL53L5CX.kStatusOK:
		print("Failed to set sharpener value")
		sys.exit(1)
	
	# Check that the sharpener value has been set to the expected value
	print("New Sharpener Value:", str(myVL53L5CX.get_sharpener_percent()) + "%")
	
	# Set the Target Order
	order = myVL53L5CX.get_target_order()
	print("Current Target Order:", order)
	
	if order == myVL53L5CX.kTargetOrderStrongest:
		print("Target Order is Strongest")
	elif order == myVL53L5CX.kTargetOrderClosest:
		print("Target Order is Closest")
	
	if myVL53L5CX.set_target_order(myVL53L5CX.kTargetOrderClosest) != myVL53L5CX.kStatusOK:
		print("Failed to set target order")
		sys.exit(1)
	
	# Check that the target order has been set to the expected value
	order = myVL53L5CX.get_target_order()
	if order == myVL53L5CX.kTargetOrderStrongest:
		print("New Target Order is Strongest")
	elif order == myVL53L5CX.kTargetOrderClosest:
		print("New Target Order is Closest")
	
	if myVL53L5CX.start_ranging() != myVL53L5CX.kStatusOK:
		print("Failed to start ranging")
		sys.exit(1)

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