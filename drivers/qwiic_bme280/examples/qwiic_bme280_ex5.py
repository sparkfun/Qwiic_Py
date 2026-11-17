#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_env_bme280_ex5.py
#
# Simple Example for the Qwiic BME280 Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
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
# Example 5 - port of the Arduino example 5
#

import qwiic_bme280
import time
import sys

def runExample():

	print("\nSparkFun BME280 Sensor  Example 5\n")
	mySensor = qwiic_bme280.QwiicBme280()

	if mySensor.connected == False:
		print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	mySensor.begin()

	print("ID(0xD0): 0x%.2x" % mySensor._i2c.readByte(mySensor.address, mySensor.BME280_CHIP_ID_REG))
	print("Reset register(0xE0): 0x%.2x" % mySensor._i2c.readByte(mySensor.address, mySensor.BME280_RST_REG))
	print("ctrl_meas(0xF4): 0x%.2x" % mySensor._i2c.readByte(mySensor.address, mySensor.BME280_CTRL_MEAS_REG))
	print("ctrl_hum(0xF2): 0x%.2x\n" % mySensor._i2c.readByte(mySensor.address, mySensor.BME280_CTRL_HUMIDITY_REG))

	print("Displaying all regs:")
	memCounter = 0x80
	for row in range(8,16):
		print("0x%.2x 0:" % row, end='')
		for column in range(0,16):
			tempReadData = mySensor._i2c.readByte(mySensor.address, memCounter)
			print("0x%.2x " % tempReadData, end='')

			memCounter += 1
		print("")


	print("Displaying concatenated calibration words:")
	print("dig_T1, uint16: %d" % mySensor.calibration["dig_T1"])
	print("dig_T2, int16: %d" % mySensor.calibration["dig_T2"])
	print("dig_T3, int16: %d" % mySensor.calibration["dig_T3"])
	print("dig_P1, uint16: %d" % mySensor.calibration["dig_P1"])
	print("dig_P2, int16: %d" % mySensor.calibration["dig_P2"])
	print("dig_P3, int16: %d" % mySensor.calibration["dig_P3"])
	print("dig_P4, int16: %d" % mySensor.calibration["dig_P4"])
	print("dig_P5, int16: %d" % mySensor.calibration["dig_P5"])
	print("dig_P6, int16: %d" % mySensor.calibration["dig_P6"])
	print("dig_P7, int16: %d" % mySensor.calibration["dig_P7"])
	print("dig_P8, int16: %d" % mySensor.calibration["dig_P8"])
	print("dig_P9, int16: %d" % mySensor.calibration["dig_P9"])
	print("dig_H1, uint8: %d" % mySensor.calibration["dig_H1"])
	print("dig_H2, int16: %d" % mySensor.calibration["dig_H2"])
	print("dig_H3, uint8: %d" % mySensor.calibration["dig_H3"])
	print("dig_H4, int16: %d" % mySensor.calibration["dig_H5"])
	print("dig_H6, int8: %d" % mySensor.calibration["dig_H6"])
	while True:

		print("Humidity:\t%.3f" % mySensor.humidity)

		print("Pressure:\t%.3f" % mySensor.pressure)	

		print("Altitude:\t%.3f" % mySensor.altitude_feet)

		print("Temperature:\t%.2f\n" % mySensor.temperature_fahrenheit)

		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 5")
		sys.exit(0)


