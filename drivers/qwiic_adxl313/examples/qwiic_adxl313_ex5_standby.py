#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_adxl313_ex5_standby.py
#
# Simple Example for the Qwiic ADXL313 DeviceSet that Shows how to switch the sensor 
# between stanby mode and measure mode.
# This example will put the device in measure mode and print 100 readings to terminal,
# Then enter standby mode for 5 seconds.
# Then loop.
# Note, the typical current required in each mode is as follows:
# Standby: 0.1uA
# Measure: 55-170uA
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, October 2020
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
# Example 5
#

import qwiic_adxl313
import qwiic_i2c
import sys

def run_example():

	print("\nSparkFun ADXL313 Example 5 - Standby mode and measure mode.\n")
	my_adxl = qwiic_adxl313.QwiicADXL313()

	if my_adxl.is_connected() == False:
		print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Device connected successfully.")        

	while True:
		# enter measure mode
		print("Entering measure mode.")
		my_adxl.measure_mode_on()
		for i in range(100):
			
			my_adxl.update_int_source_statuses(); # this will update all INTSOURCE statuses.
		
			if my_adxl.ADXL313_INTSOURCE_DATAREADY:
				my_adxl.read_accel() # read all axis from sensor, note this also updates all instance variables
				print(\
				'{: 06d}'.format(my_adxl.x)\
				, '\t', '{: 06d}'.format(my_adxl.y)\
				, '\t', '{: 06d}'.format(my_adxl.z)\
				)
			else:
				print("Waiting for data.")
			qwiic_i2c.delay_ms(50)
		print("Endering Standby Mode")
		my_adxl.standby()
		qwiic_i2c.delay_ms(5000) # 5 seconds of standby... really saving power during this time (0.1uA)
        

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit):
		print("\nEnding Example 5")
		sys.exit(0)


