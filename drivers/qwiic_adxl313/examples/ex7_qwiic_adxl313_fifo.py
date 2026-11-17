#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex7_qwiic_adxl313_fifo.py
#
# Simple Example for the Qwiic ADXL313 DeviceSet that shows how to setup the FIFO on the ADXL313.
# One key advantage of using the FIFO is that it allows us to
# let the ADXL313 store up to 32 samples in it's FIFO "buffer".
# While it is doing this, we can use our microcontroller to do other things,
# Then, when the FIFO is full (or close to), we can quickly read in the 32 samples.

# In order to use the FIFO in this way, we need to set it up to fire an interrupt
# when it gets "almost full". This threshold of samples is called the "watermark".
# When the watermark level is reached, it will fire the interrupt INT1.
# Our raspi will be monitoring the watermark int source bit, and then quickly
# read whatevers in the FIFO and save it to a log file.
# Note, we can't print the data in real time to the terminal
# because python terminal is too slow.

# Some timestamps of each stage of this cycle will also be printed.
# This will allow us to fine tune bandwidth and watermark settings.
# The "Entries" of the FIFO_STATUS register will also be printed before each read.
# This will tell us how many samples are currently held in the FIFO.
# This will allow us to read the entire contents and keep an eye on how full it is
# getting before each read. This will help us fine tune how much time we have
# between each read to do other things. (in this example, we are simplly going to do
# a delay and print dots, but you could choose to do more useful things).

# **SPI app note***
# Note, this example uses I2C to communicate the the sensor.
# If you are going to use SPI, then you will need to add in a sufficient
# delay in between reads (at least 5uSec), to allow the FIFO to "pop" the next
# reading in the data registers. See datasheet page 16 for more info.

# ///// FIFO setup //////
# Stream mode
# Trigger INT1, Note, this example does not utilize monitoring this hardware interrupt.
# We will be monitoring via software by reading the int source and watching the 
# watermark bit.
# Watermark Threshold (aka (samples in FIFO_CTL register)): 30

# ///// Interrupt setup //////
# Enable watermark interrupt.
# Map watermark interrupt to "int pin 1".
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
# Example 7
#

from __future__ import print_function
import qwiic_adxl313
import time
import sys

lastWatermarkTime = 0 # used for printing timestamps in debug
fifoEntriesAmount = 0 # used to know how much is currently in the fifo and make sure to read it all out.

def micros():
	return round(time.time_ns()/1000)

# Open a log file in "append mode", We must log data here because printing to terminal is too slow
logfile = open("log.txt","a")

def runExample():

	print("\nSparkFun Adxl313  Example 7 - FIFO reading with debug info about timing.\n")
	myAdxl = qwiic_adxl313.QwiicAdxl313()

	if myAdxl.connected == False:
		print("The Qwiic ADXL313 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Device connected successfully.")        
  
	myAdxl.standby()	# Must be in standby before changing settings.
						# This is here just in case we already had sensor powered and/or
						# configured from a previous setup.

	myAdxl.setRange(myAdxl.ADXL313_RANGE_4_G)

	# set bandwidth
	# note, 12.5Hz was chosen for this example to highlight the FIFO wait/read cycle
	# you can tweak BW and the fifo sample threshhold to suit your application.
	myAdxl.setBandwidth(myAdxl.ADXL313_BW_12_5)
	# also try:
	# myAdxl.bandwidth = myAdxl.ADXL313_BW_12_5

	# setup activity sensing options
	myAdxl.setActivityX(False)		# disable x-axis participation in detecting activity
	myAdxl.setActivityY(False)		# disable y-axis participation in detecting activity
	myAdxl.setActivityZ(False)		# disable z-axis participation in detecting activity

	# setup inactivity sensing options
	myAdxl.setInactivityX(False)		# disable x-axis participation in detecting inactivity
	myAdxl.setInactivityY(False)		# disable y-axis participation in detecting inactivity
	myAdxl.setInactivityZ(False)		# disable z-axis participation in detecting inactivity

	# FIFO SETUP
	myAdxl.setFifoMode(myAdxl.ADXL313_FIFO_MODE_STREAM)
	myAdxl.setFifoSamplesThreshhold(30) # can be 1-32

	# Interrupt Mapping
	# when fifo fills up to watermark level, it will effect the int1 pin on the sensor
	myAdxl.setInterruptMapping(myAdxl.ADXL313_INT_WATERMARK_BIT, myAdxl.ADXL313_INT1_PIN)

	# enable/disable interrupts
	# note, we set them all here, just in case there were previous settings,
	# that need to be changed for this example to work properly.
	myAdxl.ActivityINT(0)		# disable activity
	myAdxl.InactivityINT(0)		# disable inactivity
	myAdxl.DataReadyINT(0)		# disable dataready
	myAdxl.WatermarkINT(1)		# enable watermark

	myAdxl.autosleepOff()		# just in case it was set from a previous setup
	
	myAdxl.measureModeOn()		# wakes up sensor from stanby and puts into measurement mode

	# print int enable statuses, to verify we're setup correctly
	print("activity int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_ACTIVITY_BIT))
	print("inactivity int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_INACTIVITY_BIT))
	print("dataReady int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_DATA_READY_BIT))
	print("FIFO watermark int enable: ", myAdxl.isInterruptEnabled(myAdxl.ADXL313_INT_WATERMARK_BIT))
	print("FIFO watermark Samples Threshhold: ", myAdxl.getFifoSamplesThreshhold())
	print("FIFO mode: ", myAdxl.getFifoMode())
	
	lastWatermarkTime = micros()

	myAdxl.clearFifo() # clear FIFO for a fresh start on this example.
	# The FIFO may have been full from previous use
	# and then would fail to cause an interrupt when starting this example.

	uSecTimer = 0 # used to print some "dots" during down time in cycle
	while True:
		myAdxl.updateIntSourceStatuses() # this will update all INTSOURCE statuses.
		if myAdxl.ADXL313_INTSOURCE_WATERMARK:
			entries = myAdxl.getFifoEntriesAmount()
			timegap_us = (micros() - lastWatermarkTime)
			timegap_ms = round(timegap_us / 1000)
			
			print("\nWatermark Interrupt! Time since last read: ", timegap_us, "us ", timegap_ms, "ms Entries:", entries)
			lastWatermarkTime = micros()
			while entries > 0:
				myAdxl.updateIntSourceStatuses() # this will update all INTSOURCE statuses.
				if myAdxl.ADXL313_INTSOURCE_DATAREADY:
					myAdxl.readAccel() # read all axis from sensor, note this also updates all instance variables

					# Gotta log data to a text file, because printing to terminal is too slow
					logfile.write(str(myAdxl.x))
					logfile.write("\t")
					logfile.write(str(myAdxl.y))
					logfile.write("\t")
					logfile.write(str(myAdxl.z))
					logfile.write("\n")
					entries -= 1 # we've read one more entry, so let's keep track and keep going until we're done
				else:
					print("Waiting for Data.")
		
		time.sleep(0.000001) # sleep 1 microsecond
		uSecTimer += 1
		if uSecTimer > 100:
			print(".", end = '')
			uSecTimer = 0


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		logfile.close() 
		sys.exit(0)


