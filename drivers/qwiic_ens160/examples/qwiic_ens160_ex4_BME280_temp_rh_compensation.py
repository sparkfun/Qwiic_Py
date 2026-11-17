#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ens160_ex4_BME280_temp_rh_compensation.py
#
#  This example shows how to give the ENS160 Temperature and Relative Humidity
#  Data for compensation with the BME280. Note that the values that are given for compensation are not
#  populated in their registers until the Air Quality Sensor is set to "Standard" operation
#  and when data is ready (i.e. the data ready bit is set). Also note that there will be some 
#  rounding of the temperature and relative humidity values when they're given to the sensor
#  and again when they're read back.
# 
# SparkFun Environmental Combo Breakout: https://www.sparkfun.com/products/22858
# SparkFun Atmospheric Sensor Breakout: https://www.sparkfun.com/products/15440
# 
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
import qwiic_bme280 # https://github.com/sparkfun/Qwiic_BME280_Py/
import sys
from time import sleep

def runExample():
	print("\nQwiic ENS160 Example 4 - Humidity and Temperature Sensor Compensation - BME280\n")

	# Create instance of Air Quality Sensor
	myEns = qwiic_ens160.QwiicENS160()

	# Check if it's connected
	if myEns.is_connected() == False:
		print("The ENS device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myEns.begin()

	# Create instance of Humidity and Temperature Sensor
	myBme = qwiic_bme280.QwiicBme280()

	# Check if it's connected
	if myBme.is_connected() == False:
		print("The BME device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myBme.begin()

	# Fetch Humidity and temperature for compensation
	rh = myBme.humidity
	tempC = myBme.temperature_celsius
	print("Relative Humidity: {}".format(rh))
	print("Temperature (Celcius): {}".format(tempC))
	
	# ENS setup and compensation:
	myEns.set_operating_mode(myEns.kOpModeReset)

	sleep(0.1)

	myEns.set_temp_compensation_celsius(tempC)
	myEns.set_rh_compensation(rh)

	sleep(0.5)

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
	print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): {}".format(ensStatus))

	# Wait for the RH and Temp compensation to be set and ready to read
	while not myEns.check_data_status():
		pass
	
	# Read out the RH and Temp compensation actually used by the device
	print("---------------------------")
	print("Compensation Relative Humidity (%): ", myEns.get_rh())
	print("---------------------------")
	print("Compensation Temperature (Celsius): ", myEns.get_temp_celsius())
	print("---------------------------")

	# Print the compensated values from the ENS160
	while True:
		if myEns.check_data_status():		
			print("Air Quality Index (1-5) : ", myEns.get_aqi())
			print("Total Volatile Organic Compounds (ppb): ", myEns.get_tvoc())
			print("CO2 concentration (ppm): ", myEns.get_eco2())
			
		sleep(0.2)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)