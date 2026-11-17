#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Example2_One-Shot_Temperature_Reading.py
# Example for the TMP102 I2C Temperature Sensor
# Alex Wende @ SparkFun Electronics
# April 29th 2016
#
# This sketch connects to the TMP102 temperature sensor and enables the
# one-shot temperature measurement mode using the one_shot() function.
# The function returns 0 until the temperature measurement is ready to
# read (takes around 25ms). After the measurment is read, the TMP102 is
# placed back into sleep mode before the loop is repeated. This can be 
# useful to save power or increase the continuous conversion rate from
# 8Hz up to a maximum of 40Hz.

# This code is beerware; if you see me (or any other SparkFun employee) at
# the local, and you've found our code helpful, please buy us a round!

# Distributed as-is; no warranty is given.   
#-----------------------------------------------------------------------------

import qwiic_tmp102
import time
import sys

# Connections
# VCC = 3.3V
# GND = GND
# SDA = A4
# SCL = A5

# Sensor address can be changed with an external jumper to:
# ADD0 - Address
# VCC - 0x49
# SDA - 0x4A
# SCL - 0x4B


def runExample():

	print("\nSparkFun Qwiic TMP102 Sensor Example 2\n")
	myTmpSensor = qwiic_tmp102.QwiicTmp102Sensor()

	if myTmpSensor.is_connected == False:
		print("The Qwiic TMP102 Sensor device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myTmpSensor.begin()

	print("Initialized.")

	while True:
		myTmpSensor.one_shot(1)
		while(myTmpSensor.one_shot() == 0):
			time.sleep(1)
		print ("TempC = ", myTmpSensor.read_temp_c())
		myTmpSensor.sleep()
		time.sleep(1)


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)




