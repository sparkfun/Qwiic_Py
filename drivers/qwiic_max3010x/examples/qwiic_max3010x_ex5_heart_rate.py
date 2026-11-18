#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_max3010x_ex5_heart_rate.py
#
# Simple example for the qwiic MAX3010x device
# This is a demo to show the reading of heart rate or beats per minute (BPM) using
# a Penpheral Beat Amplitude (PBA) algorithm.
#
# It is best to attach the sensor to your finger using a rubber band or other tightening
# device. Humans are generally bad at applying constant pressure to a thing. When you
# press your finger against the sensor it varies enough to cause the blood in your
# finger to flow differently which causes the sensor readings to go wonky.
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
# Example 5
#

import qwiic_max3010x
import qwiic_i2c
import sys


def run_example():

	print("\nSparkFun MAX3010x Photodetector - Example 5\n")
	sensor = qwiic_max3010x.QwiicMAX3010x()

	if not sensor.begin():
		print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("The Qwiic MAX3010x is connected.")

	print("Place your index finger on the sensor with steady pressure.")

	sensor.setup()
	print("Setup complete.")

	sensor.set_pulse_amplitude_red(0x0A) # Turn Red LED to low to indicate sensor is running
	sensor.set_pulse_amplitude_green(0) # Turn off Green LED

	RATE_SIZE = 4 # Increase this for more averaging. 4 is good.
	rates = list(range(RATE_SIZE)) # list of heart rates
	rate_spot = 0
	last_beat = 0 # Time at which the last beat occurred
	beats_per_minute = 0.00
	beat_avg = 0
	samples_taken = 0 # Counter for calculating the hz or read rate
	start_time = qwiic_i2c.ticks_ms() # Used to calculate measurement rate
	
	while True:
                
		ir_value = sensor.get_ir()
		samples_taken += 1
		if sensor.check_for_beat(ir_value):
			# We sensed a beat!
			print('BEAT')
			delta = qwiic_i2c.ticks_diff(qwiic_i2c.ticks_ms(), last_beat)
			last_beat = qwiic_i2c.ticks_ms()	
	
			beats_per_minute = 60 / (delta / 1000.0)
			beats_per_minute = round(beats_per_minute,1)
	
			if beats_per_minute < 255 and beats_per_minute > 20:
				rate_spot += 1
				rate_spot %= RATE_SIZE # Wrap variable
				rates[rate_spot] = beats_per_minute # Store this reading in the array

				# Take average of readings
				beat_avg = 0
				for x in range(0, RATE_SIZE):
					beat_avg += rates[x]
				beat_avg /= RATE_SIZE
				beat_avg = round(beat_avg)
        
		hz = round(float(samples_taken) / ( qwiic_i2c.ticks_diff(qwiic_i2c.ticks_ms(), start_time) / 1000.0 ) , 2)
		if (samples_taken % 200 ) == 0:
                        
			print(\
				'IR=', ir_value , ' \t',\
            				'BPM=', beats_per_minute , '\t',\
                                                                                #'DCE', get_dce() , '\t',\
            				'Avg=', beat_avg , '\t',\
				'hz=', hz, \
				)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 5")
		sys.exit(0)
