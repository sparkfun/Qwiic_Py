#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_max3010x_ex2_presence_sensing.py
#
# Simple example for the qwiic MAX3010x device
# This takes an average reading at power up and if the reading changes more than 100,
# then print 'Something is there!'.
#
#------------------------------------------------------------------------
#
# Written by Pete Lewis
# SparkFun Electronics, May 2020
#
# Based on code from the SparkFun MAX3010x Sensor Arduino Library
# https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library
# By: Nathan Seidle @ SparkFun Electronics, October 2nd, 2016
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

import qwiic_max3010x
import qwiic_i2c
import sys


print("\nSparkFun MAX3010x Photodetector - Example 2\n")
sensor = qwiic_max3010x.QwiicMAX3010x()

if not sensor.begin():
	print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)
else:
	print("The Qwiic MAX3010x is connected.")

# Setup to sense up to 18 inches, max LED brightness
led_brightness = 0xFF # Options: 0=Off to 255=50mA
sample_average = 4 # Options: 1, 2, 4, 8, 16, 32
led_mode = 2 # Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
sample_rate = 400 # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
pulse_width = 411 # Options: 69, 118, 215, 411
adc_range = 2048 # Options: 2048, 4096, 8192, 16384

sensor.setup(led_brightness, sample_average, led_mode, sample_rate, pulse_width, adc_range)
print("Setup complete.")        

sensor.set_pulse_amplitude_red(0) # Turn off Red LED
sensor.set_pulse_amplitude_green(0) # Turn off Green LED

samples_taken = 0       # Counter for calculating the hz or read rate
unblocked_value = 0     # Average IR at power up
start_time = 0          # Used to calculate measurement rate

# Take an average of IR readings at power up
unblocked_value = 0
for i in range(0,32):
	unblocked_value += sensor.get_ir() # Read the IR value
unblocked_value /= 32

start_time = qwiic_i2c.ticks_ms()


while True:
		samples_taken += 1

		ir_sample = sensor.get_ir()
		hertz = samples_taken / (qwiic_i2c.ticks_diff(qwiic_i2c.ticks_ms(), start_time) / 1000)
		current_delta = (ir_sample - unblocked_value)

		hertz = round(hertz, 2)
		current_delta = round(current_delta, 2)

		message = ' ' # blank message
		if current_delta > 100:
			message = 'Something is there!'

		print(\
		 'IR[', ir_sample , '] \t',\
             'hz[', hertz , '] \t',\
		 'delta[', current_delta, ']',\
		 message
		)
