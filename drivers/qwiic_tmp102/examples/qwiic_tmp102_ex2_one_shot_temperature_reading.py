#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_tmp102_ex2_one_shot_temperature_reading.py
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
import qwiic_i2c
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


print("\nSparkFun Qwiic TMP102 Sensor Example 2\n")
myTmpSensor = qwiic_tmp102.QwiicTMP102()

if not myTmpSensor.is_connected():
	print("The Qwiic TMP102 Sensor device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

myTmpSensor.begin()

print("Initialized.")

while True:
	myTmpSensor.one_shot(1)
	while(myTmpSensor.one_shot() == 0):
		qwiic_i2c.delay_ms(1000)
	print ("TempC = ", myTmpSensor.read_temp_c())
	myTmpSensor.sleep()
	qwiic_i2c.delay_ms(1000)
