#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex2_Presence_Sensing.py
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

	print("\nSparkFun MAX3010x Photodetector - Example 1\n")
	sensor = qwiic_max3010x.QwiicMax3010x()

	if sensor.begin() == False:
		print("The Qwiic MAX3010x device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("The Qwiic MAX3010x is connected.")

  	# Setup to sense up to 18 inches, max LED brightness
	ledBrightness = 0xFF # Options: 0=Off to 255=50mA
	sampleAverage = 4 # Options: 1, 2, 4, 8, 16, 32
	ledMode = 2 # Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
	sampleRate = 400 # Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
	pulseWidth = 411 # Options: 69, 118, 215, 411
	adcRange = 2048 # Options: 2048, 4096, 8192, 16384

	if sensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange) == False:
		print("Device setup failure. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Setup complete.")        

	sensor.setPulseAmplitudeRed(0) # Turn off Red LED
	sensor.setPulseAmplitudeGreen(0) # Turn off Green LED

	samplesTaken = 0       # Counter for calculating the Hz or read rate
	unblockedValue = 0     # Average IR at power up
	startTime = 0          # Used to calculate measurement rate

	# Take an average of IR readings at power up
	unblockedValue = 0
	for i in range(0,32):
		unblockedValue += sensor.getIR() # Read the IR value
	unblockedValue /= 32

	startTime = millis()


	while True:
			samplesTaken += 1

			IRSample = sensor.getIR()
			hertz = samplesTaken / ((millis() - startTime) / 1000)
			currentDelta = (IRSample - unblockedValue)

			hertz = round(hertz, 2)
			currentDelta = round(currentDelta, 2)

			message = ' ' # blank message
			if currentDelta > 100:
				message = 'Something is there!'

			print(\
			 'IR[', IRSample , '] \t',\
             'Hz[', hertz , '] \t',\
			 'delta[', currentDelta, ']',\
			 message
			)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 2")
		sys.exit(0)


