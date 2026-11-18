#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_adxl313_ex6_interrupt.py
#
# Simple Example for the Qwiic ADXL313 DeviceSet that shows how to setup a interrupt on the ADXL313.
# Note, for this example we will setup the interrupt and poll the interrupt register
# via software.
# We will utilize the autosleep feature of the sensor.
# When it senses inactivity, it will go to sleep.
# When it senses new activity, it will wake up and trigger the INT1 pin.
# We will monitor the status of the interrupt by continuing to read the 
# interrupt register on the device.

# ///// Autosleep setup //////
# First, setup THRESH_INACT, TIME_INACT, and participating axis.
# These settings will determine when the unit will go into autosleep mode and save power!
# We are only going to use the x-axis (and are disabling y-axis and z-axis).
# This is so you can place the board "flat" inside your project,
# and we can ignore gravity on z-axis.

# ///// Interrupt setup //////
# Enable activity interrupt.
# Map activity interrupt to "int pin 1".
# This harware interrupt pin setup could be monitored by a GPIO on the raspi,
# or external system, however, for this example, we will simply
# poll the interrupt register via software to monitor its status.
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
# Example 6
#

import qwiic_adxl313
import qwiic_i2c
import sys


print("\nSparkFun ADXL313 Example 6 - Setup Autosleep and interrupts, then only print values when it's awake.\n")
my_adxl = qwiic_adxl313.QwiicADXL313()

if my_adxl.is_connected() == False:
	print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)
else:
	print("Device connected successfully.")        

my_adxl.standby()	# Must be in standby before changing settings.
					# This is here just in case we already had sensor powered and/or
					# configured from a previous setup.

my_adxl.set_range(my_adxl.ADXL313_RANGE_4_G)

# setup activity sensing options
my_adxl.set_activity_x(True)		# enable x-axis participation in detecting activity
my_adxl.set_activity_y(False)		# disable y-axis participation in detecting activity
my_adxl.set_activity_z(False)		# disable z-axis participation in detecting activity
my_adxl.set_activity_threshold(10)	# 0-255 (62.5mg/LSB)

# setup inactivity sensing options
my_adxl.set_inactivity_x(True)			# enable x-axis participation in detecting inactivity
my_adxl.set_inactivity_y(False)		# disable y-axis participation in detecting inactivity
my_adxl.set_inactivity_z(False)		# disable z-axis participation in detecting inactivity
my_adxl.set_inactivity_threshold(10)	# 0-255 (62.5mg/LSB)
my_adxl.set_time_inactivity(5)			# 0-255 (1sec/LSB)

# Interrupt Mapping
# when activity of inactivity is detected, it will effect the int1 pin on the sensor
my_adxl.set_interrupt_mapping(my_adxl.ADXL313_INT_ACTIVITY_BIT, my_adxl.ADXL313_INT1_PIN)
my_adxl.set_interrupt_mapping(my_adxl.ADXL313_INT_INACTIVITY_BIT, my_adxl.ADXL313_INT1_PIN)

my_adxl.activity_int(1)
my_adxl.inactivity_int(1)
my_adxl.data_ready_int(0)

my_adxl.autosleep_on()

my_adxl.measure_mode_on()

# print int enable statuses, to verify we're setup correctly
print("activity int enable: ", my_adxl.is_interrupt_enabled(my_adxl.ADXL313_INT_ACTIVITY_BIT))
print("inactivity int enable: ", my_adxl.is_interrupt_enabled(my_adxl.ADXL313_INT_INACTIVITY_BIT))
print("data_ready int enable: ", my_adxl.is_interrupt_enabled(my_adxl.ADXL313_INT_DATA_READY_BIT))
qwiic_i2c.delay_ms(5000)

while True:
	my_adxl.update_int_source_statuses() # this will update all INTSOURCE statuses.

	if my_adxl.ADXL313_INTSOURCE_INACTIVITY:
		print("Inactivity detected.")
		qwiic_i2c.delay_ms(1000)
	if my_adxl.ADXL313_INTSOURCE_DATAREADY:
		my_adxl.read_accel() # read all axis from sensor, note this also updates all instance variables
		print(\
		 '{: 06d}'.format(my_adxl.x)\
		, '\t', '{: 06d}'.format(my_adxl.y)\
		, '\t', '{: 06d}'.format(my_adxl.z)\
		)
	else:
		print("Device is asleep (data_ready is reading false)")
	qwiic_i2c.delay_ms(50)
