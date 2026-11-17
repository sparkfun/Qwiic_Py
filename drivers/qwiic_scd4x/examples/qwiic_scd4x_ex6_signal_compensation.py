#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_scd4x_ex6_signal_compensation.py
#
# This example shows how to set the three signal compensation settings: 
# temperature offset, sensor altitude, and ambient pressure.
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
	print("\nQwiic SCD4x Example 6 - Signal Compensation\n")

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

	# Now we can change the sensor settings.
	# There are three signal compensation commands we can use: set_temperature_offset; set_sensor_altitude; and set_ambient_pressure
	print("Temperature offset is currently: ", mySCD4x.get_temperature_offset())
	mySCD4x.set_temperature_offset(5) # Set the temperature offset to 5C
	print("Temperature offset is now: ", mySCD4x.get_temperature_offset())
	
	print("Sensor altitude is currently: ", mySCD4x.get_sensor_altitude())
	mySCD4x.set_sensor_altitude(1000) # Set the sensor altitude to 1000 meters
	print("Sensor altitude is now: ", mySCD4x.get_sensor_altitude())

	# There is no get_ambient_pressure command
	if mySCD4x.set_ambient_pressure(98700):
		print("Ambient pressure set")

	# The signal compensation settings are stored in RAM by default and will reset if reInit is called
  	# or if the power is cycled. To store the settings in EEPROM we can call:
	# mySCD4x.persist_settings() # Uncomment this line to store the sensor settings in EEPROM

	# Just for giggles, while the periodic measurements are stopped, let's read the sensor serial number
	serialNumber = mySCD4x.get_serial_number()
	if serialNumber is None:
		print("Error while reading serial number", file=sys.stderr)
		return
	
	print("The sensor's serial number is:", "0x" + serialNumber)

	# Finally, we need to restart periodic measurements
	mySCD4x.start_periodic_measurement()
	print("Periodic measurements restarted")

	while True:
		if mySCD4x.read_measurement(): # This must be called to get new data. It will return false until new data is available 
			print("\nCO2(ppm):", mySCD4x.get_co2())
			print("Temperature(C):", mySCD4x.get_temperature())
			print("Humidity(%RH):", mySCD4x.get_humidity())
		else:
			print(".", end="")
		
		time.sleep(0.5) # Only check for new data every 0.5 second

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)