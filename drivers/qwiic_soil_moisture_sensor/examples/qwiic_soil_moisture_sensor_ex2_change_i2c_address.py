#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_soil_moisture_sensor_ex2_change_i2c_address.py
#
# Simple Example for the Qwiic Soil Moisture Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
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
# Copyright (c) 2019 SparkFun Electronics
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
# Example 2
#

import qwiic_soil_moisture_sensor
import qwiic_i2c
import sys

# If you've already changed the I2C address, change this to the current address!
current_address = qwiic_soil_moisture_sensor.SOIL_MOISTURE_SENSOR_DEFAULT_ADDRESS


print("\nSparkFun Qwiic Soil Moisture Sensor Example 2 - Change I2C Address\n")
mySoilSensor = qwiic_soil_moisture_sensor.QwiicSoilMoistureSensor(current_address)

if not mySoilSensor.is_connected():
	print("The Qwiic Soil Moisture Sensor device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

mySoilSensor.begin()

print("Ready!")
print("Enter a new I2C address for the Qwiic Soil Moisture Sensor to use.")
print("Any address from 0x08 to 0x3F works.")
print("Don't use the 0x prefix. For instance if you wanted to")
print("change the address to 0x3B, you would type 3B and hit enter.")

new_address = input("\nNew Address: ")
new_address = int(new_address, 16)

# Check if the user entered a valid address
if new_address >= 0x08 and new_address <= 0x3F:
	print("\nCharacters received and new address valid!")
	print("\nAttempting to set Soil Moisture Sensor address...")

	mySoilSensor.change_address(new_address)
	print("\nAddress successfully changed!")

	# Check that the Soil Moisture Sensor acknowledges on new addres
	qwiic_i2c.delay_ms(20)
	if not mySoilSensor.begin():
		print("\nThe Qwiic Soil Moisture Sensor isn't connected to the system. Please check your connection", file=sys.stderr)
	else:
		print("\nSoil Moisture Sensor acknowledged on new address!")

else:
	print("\nAddress entered not a valid I2C address")
