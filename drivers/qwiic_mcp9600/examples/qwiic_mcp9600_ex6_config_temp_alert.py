#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp9600_ex6_config_temp_alert.py
#
#   This example outputs the ambient and thermocouple temperatures from the MCP9600 sensor, but allows for a non
#   K-type thermocouple to be used.
#   The Qwiic MCP9600 supports K/J/T/N/S/E/B/R type thermocouples, and the type can be configured below!
# 
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
import time

# Change the alert configuration here!
rising_alert = 1  # What alert to use for detecting cold -> hot transitions.
falling_alert = 3  # What alert to use for detecting hot -> cold transitions.
				   # These numbers are arbitrary and can be anything from 1 to 4, but just can't be equal!

alert_temp = 29.5  # What temperature to trigger the alert at (before hysteresis).
				   # This is about the surface temperature of my finger, but please change this if
				   # you have colder/warmer hands or if the ambient temperature is different.
hysteresis = 2  # How much hysteresis to have, in degrees Celsius. Feel free to adjust this, but 2°C seems to be about right.

def runExample():

	print("\nQwiic MCP9600 Example 6 - Config Temp Alert\n")

	# Create instance of device
	myThermo = qwiic_mcp9600.QwiicMCP9600()

	# Check if it's connected
	if myThermo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myThermo.begin()
	
	myThermo.config_alert_hysteresis(rising_alert, hysteresis)
	myThermo.config_alert_temp(rising_alert, alert_temp)
	myThermo.config_alert_junction(rising_alert, 0)
	myThermo.config_alert_edge(rising_alert, True)
	myThermo.config_alert_logic_level(rising_alert, True)
	myThermo.config_alert_mode(rising_alert, 1)
	myThermo.config_alert_enable(rising_alert, True)

	myThermo.config_alert_hysteresis(falling_alert, hysteresis)
	myThermo.config_alert_temp(falling_alert, alert_temp)
	myThermo.config_alert_junction(falling_alert, 0)
	myThermo.config_alert_edge(falling_alert, False)
	myThermo.config_alert_logic_level(falling_alert, True)
	myThermo.config_alert_mode(falling_alert, 1)
	myThermo.config_alert_enable(falling_alert, True)

	# TODO: This is maybe a bit too messy/verbose for users to have to look at. But the arduino lib had it...
	print("alert 1 hysteresis: ", bin(myThermo.read_block_retry(myThermo.kRegisterAlert1Hysteresis, 1)[0]))
	a1_limit_bytes = myThermo.read_block_retry(myThermo.kRegisterAlert1Limit, 2)
	print("alert 1 limit: ", bin(a1_limit_bytes[0] << 8 | a1_limit_bytes[1]))
	print("alert 1 config: ", bin(myThermo.read_block_retry(myThermo.kRegisterAlert1Config, 1)[0]))

	print("alert 3 hysteresis: ", bin(myThermo.read_block_retry(myThermo.kRegisterAlert3Hysteresis, 1)[0]))
	a3_limit_bytes = myThermo.read_block_retry(myThermo.kRegisterAlert3Limit, 2)
	print("alert 3 limit: ", bin(a3_limit_bytes[0] << 8 | a3_limit_bytes[1]))
	print("alert 3 config: ", bin(myThermo.read_block_retry(myThermo.kRegisterAlert3Config, 1)[0]))

	start_time = time.time()
	update_time = 1

	while True:
		if (time.time() - start_time >= update_time): # Update every second w/o blocking
			print(f"Thermocouple: {myThermo.get_thermocouple_temp()}C   Ambient: {myThermo.get_ambient_temp()}C   Temperature Delta: {myThermo.get_temp_delta()}C")

			if myThermo.is_temp_greater_than_limit(rising_alert):
				print("Temperature exceeds limit 1!")
				print("Clearing alert 1...")
				myThermo.clear_alert_pin(rising_alert)


			if myThermo.is_temp_greater_than_limit(falling_alert):
				print("Temperature exceeds limit 3!")
				print("Clearing alert 3...")
				myThermo.clear_alert_pin(falling_alert)

			start_time = time.time()
		
		# TODO: Arduino example cleared alerts based on non-blocking user input on the command line. 
		# 		For Python, that is platform specific so we might want to address if that's necessary or what a good alternative is...

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)