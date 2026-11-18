#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_mcp4725_ex4_read.py
#
# This example writes the DAC and then reads the DAC value back from the device.
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

import qwiic_mcp4725
import sys
import qwiic_i2c
def run_example():
	print("\nQwiic Template Example 4 - Read\n")

	# Create instance of device
	my_dac = qwiic_mcp4725.QwiicMCP4725()

	# Check if it's connected
	if not my_dac.is_connected():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	my_dac.begin()
	
	# Write both the DAC and EEPROM
	my_dac.write_dac_eeprom(1024)  # ~0.825V if VDD = 3.3V
	
	qwiic_i2c.delay_ms(250)  # Delay to allow the EEPROM write to complete

	# Now write just the DAC with a different value
	my_dac.write_dac(2048)  # ~1.65V if VDD = 3.3V

	while True:
		# Read the DAC value
		# The returned object is a dictionary with the following keys:
			# - `rdy_flag`: Ready flag
            # - `por_flag`: Power-on reset flag
            # - `dac_power_down_mode`: DAC power down mode
            # - `dac_value`: DAC register value
            # - `eeprom_power_down_mode`: EEPROM power down mode
            # - `eeprom_value`: EEPROM register value

		read_data = my_dac.read_dac_eeprom()
		print("EEPROM Value:", read_data['eeprom_value'])
		print("DAC Value:", read_data['dac_value'])

		qwiic_i2c.delay_ms(1000)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example")
		sys.exit(0)