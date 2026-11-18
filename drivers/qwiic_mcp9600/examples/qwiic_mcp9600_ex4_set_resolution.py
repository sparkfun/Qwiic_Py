#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp9600_ex4_set_resolution.py
#
#   This example allows you to change the ADC resolution on the thermocouple (hot) and ambient (cold) junctions. Why
#   do this, you ask? Well, setting the resolution lower decreases the sampling time, meaning that you can measure
#   high-speed thermal transients! (at the expense of lower resolution, of course).

#   Before we start adjusting ADC resolution, a quick word on how this all works. All thermocouple systems have a hot
#   and cold junction, and the MCP9600 is no different. Thanks to physics, thermocouples only measure the difference
#   in hot and cold junction temperatures, meaning that in order to know the temperature of the hot junction, the
#   amplifier needs to know the temperature of cold junction. From there, it will add the cold junction temperature
#   to the temperature difference measured by the thermocouple, giving the absolute temperature rather than just the
#   relative one.

#   This means that the MCP9600 has to take two temperature measurements! Thankfully, the MCP9600 will let us set the 
#   resolution on each one independently. SetAmbientResolution and SetThermocoupleResolution configure these measurements
#   with a desired resolution for the cold and hot junctions respectively. 

#   Cold Junction Possible Resolutions:
#   AMBIENT_RESOLUTION_ZERO_POINT_0625   -> Configures the ambient (cold) junction to measure in increments of 0.0625ºC
#   AMBIENT_RESOLUTION_ZERO_POINT_25     -> Configures the ambient (cold) junction to measure in increments of 0.25ºC

#   Hot Junction Possible Resolutions: 
#   THERMOCOUPLE_RESOLUTION_18_BIT  -> Reads the hot junction ADC to 18 bits, or 2µV
#   THERMOCOUPLE_RESOLUTION_16_BIT  -> Reads the hot junction ADC to 16 bits, or 8µV
#   THERMOCOUPLE_RESOLUTION_14_BIT  -> Reads the hot junction ADC to 14 bits, or 32µV
#   THERMOCOUPLE_RESOLUTION_12_BIT  -> Reads the hot junction ADC to 12 bits, or 128µV

#   It's worth noting that since the thermocouple that serves as the hot junction is arbitrary, we can't provide a 
#   specification on how many degrees Celcius precision you will get for a given ADC resolution. 

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

import qwiic_mcp9600
import sys
import qwiic_i2c

# Change the Resolutions here!
ambient_resolution = qwiic_mcp9600.QwiicMCP9600.AMBIENT_RESOLUTION_ZERO_POINT_0625
thermocouple_resolution = qwiic_mcp9600.QwiicMCP9600.THERMOCOUPLE_RESOLUTION_14_BIT

def run_example():

	print("\nQwiic MCP9600 Example 4 - Set Resolution\n")

	# Create instance of device
	my_thermo = qwiic_mcp9600.QwiicMCP9600()

	# Check if it's connected
	if not my_thermo.is_connected():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_thermo.begin()
	
	# Set the resolution on the ambient (cold) junction
	my_thermo.set_ambient_resolution(ambient_resolution)
	my_thermo.set_thermocouple_resolution(thermocouple_resolution)
	
	while True:
		if my_thermo.available():
			# Read temperatures
			thermocouple_temp = my_thermo.get_thermocouple_temp()
			ambient_temp = my_thermo.get_ambient_temp()
			temp_delta = my_thermo.get_temp_delta()

			# Print temperatures
			print(f"Thermocouple: {thermocouple_temp}C   Ambient: {ambient_temp}C   Temperature Delta: {temp_delta}C")
			
		# Delay to avoid hammering the I2C bus
		qwiic_i2c.delay_ms(20)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)