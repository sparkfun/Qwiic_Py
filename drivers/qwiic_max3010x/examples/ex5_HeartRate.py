#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex5_HeartRate.py
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
import time
import sys

# Provide platform-dependent way to get current time in milliseconds
if hasattr(time, "monotonic_ns"):
	def millis():
		return time.monotonic_ns() // 1000000 # works in CircuitPython and Linux/Raspberry Pi
else:
	def millis():
		return time.time_ns() // 1000000 #only works in MicroPython

def runExample():

	print("\nSparkFun MAX3010x Photodetector - Example 5\n")
	sensor = qwiic_max3010x.QwiicMax3010x()

	if sensor.begin() == False:
		print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("The Qwiic MAX3010x is connected.")

	print("Place your index finger on the sensor with steady pressure.")

	if sensor.setup() == False:
		print("Device setup failure. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Setup complete.")

	sensor.setPulseAmplitudeRed(0x0A) # Turn Red LED to low to indicate sensor is running
	sensor.setPulseAmplitudeGreen(0) # Turn off Green LED

	RATE_SIZE = 4 # Increase this for more averaging. 4 is good.
	rates = list(range(RATE_SIZE)) # list of heart rates
	rateSpot = 0
	lastBeat = 0 # Time at which the last beat occurred
	beatsPerMinute = 0.00
	beatAvg = 0
	samplesTaken = 0 # Counter for calculating the Hz or read rate
	startTime = millis() # Used to calculate measurement rate
	
	while True:
                
		irValue = sensor.getIR()
		samplesTaken += 1
		if sensor.checkForBeat(irValue) == True:
			# We sensed a beat!
			print('BEAT')
			delta = ( millis() - lastBeat )
			lastBeat = millis()	
	
			beatsPerMinute = 60 / (delta / 1000.0)
			beatsPerMinute = round(beatsPerMinute,1)
	
			if beatsPerMinute < 255 and beatsPerMinute > 20:
				rateSpot += 1
				rateSpot %= RATE_SIZE # Wrap variable
				rates[rateSpot] = beatsPerMinute # Store this reading in the array

				# Take average of readings
				beatAvg = 0
				for x in range(0, RATE_SIZE):
					beatAvg += rates[x]
				beatAvg /= RATE_SIZE
				beatAvg = round(beatAvg)
        
		Hz = round(float(samplesTaken) / ( ( millis() - startTime ) / 1000.0 ) , 2)
		if (samplesTaken % 200 ) == 0:
                        
			print(\
				'IR=', irValue , ' \t',\
            				'BPM=', beatsPerMinute , '\t',\
                                                                                #'DCE', getDCE() , '\t',\
            				'Avg=', beatAvg , '\t',\
				'Hz=', Hz, \
				)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 5")
		sys.exit(0)


