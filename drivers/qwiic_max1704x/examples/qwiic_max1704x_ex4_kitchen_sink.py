#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_max1704x_ex4_kitchen_sink.py 
#
# This file demonstrates the simple API of the SparkFun MAX17043 Arduino library.

# This example is an "everything-but-the-kitchen-sink" test of the MAX17048.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
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
#===============================================================================

import qwiic_max1704x
import sys
import time

def runExample():
	print("\nQwiic MAX1704X Example 4 - MAX17048 Kitchen Sink\n")

	# Create instance of device
	myLipo = qwiic_max1704x.QwiicMAX1704X(qwiic_max1704x.QwiicMAX1704X.kDeviceTypeMAX17048)

	# Check if it's connected
	if myLipo.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	myLipo.begin()

	# Just because we can, let's reset the MAX17048
	print("Resetting the MAX17048...")
	myLipo.reset()
	time.sleep(1) # Give it time to get its act back together

	# Read and print the reset indicator
	ri = myLipo.is_reset(True)
	print("Reset indicator: ", ri) # Read the RI flag and clear it automatically if it is set
	# If RI was set before, it will be cleared now
	if ri:
		print("Reset Indicator is now: ", myLipo.is_reset(False))

	# To quick-start or not to quick-start? That is the question!
	# Read the following and then decide if you do want to quick-start the fuel gauge.
	# "Most systems should not use quick-start because the ICs handle most startup problems transparently,
	# such as intermittent battery-terminal connection during insertion. If battery voltage stabilizes
	# faster than 17ms then do not use quick-start. The quick-start command restarts fuel-gauge calculations
	# in the same manner as initial power-up of the IC. If the system power-up sequence is so noisy that the
	# initial estimate of SOC has unacceptable error, the system microcontroller might be able to reduce the
	# error by using quick-start."
	# If you still want to try a quick-start then uncomment the next line:
	# myLipo.quick_start()

	# Read and print the device ID
	print("Device ID: 0x{:02X}".format(myLipo.get_id()))

	# Read and print the device version
	print("Device version: 0x{:02X}".format(myLipo.get_version()))

	# Read and print the battery threshold
	print("Battery empty threshold is currently: {}%".format(myLipo.get_threshold()))

	# Set an interrupt to alert when the battery SoC gets too low.
	# We can alert at anywhere between 1% and 32%:
	myLipo.set_threshold(20) # Set alert threshold to 20%.

	# Read and print the battery empty threshold
	print("Battery empty threshold is now: {}%".format(myLipo.get_threshold()))

	# Read and print the high voltage threshold
	high_voltage = myLipo.get_valrt_max() * 0.02 # 1 LSb is 20mV. Convert to Volts.
	print("High voltage threshold is currently: {:.2f}V".format(high_voltage))

	# Set the high voltage threshold
	myLipo.set_valrt_max_volts(4.1) # Set high voltage threshold (Volts)

	# Read and print the high voltage threshold
	high_voltage = myLipo.get_valrt_max() * 0.02 # 1 LSb is 20mV. Convert to Volts.
	print("High voltage threshold is now: {:.2f}V".format(high_voltage))

	# Read and print the low voltage threshold
	low_voltage = myLipo.get_valrt_min() * 0.02 # 1 LSb is 20mV. Convert to Volts.
	print("Low voltage threshold is currently: {:.2f}V".format(low_voltage))

	# Set the low voltage threshold
	myLipo.set_valrt_min_volts(3.9) # Set low voltage threshold (Volts)

	# Read and print the low voltage threshold
	low_voltage = myLipo.get_valrt_min() * 0.02 # 1 LSb is 20mV. Convert to Volts.
	print("Low voltage threshold is now: {:.2f}V".format(low_voltage))

	# Enable the State Of Change alert
	print("Enabling the 1% State Of Change alert: ", end="")
	if myLipo.enable_soc_alert():
		print("success.")
	else:
		print("FAILED!")

	# Read and print the HIBRT Active Threshold
	print("Hibernate active threshold is: ", end="")
	act_thr = myLipo.get_hibrt_act_thr() * 0.00125 # 1 LSb is 1.25mV. Convert to Volts.
	print("{:.5f}V".format(act_thr))

	# Read and print the HIBRT Hibernate Threshold
	print("Hibernate hibernate threshold is: ", end="")
	hib_thr = myLipo.get_hibrt_hib_thr() * 0.208 # 1 LSb is 0.208%/hr. Convert to %/hr.
	print("{:.3f}%/h".format(hib_thr))

	while True:
		# Print the variables:
		print("Voltage: {:.2f}V".format(myLipo.get_voltage()))  # Print the battery voltage

		print("Percentage: {:.2f}%".format(myLipo.get_soc()))  # Print the battery state of charge with 2 decimal places

		print("Change Rate: {:.2f}%/hr".format(myLipo.get_change_rate()))  # Print the battery change rate with 2 decimal places

		print("Alert: {}".format(myLipo.get_alert()))  # Print the generic alert flag

		print("Voltage High Alert: {}".format(myLipo.is_voltage_high(True)))  # Print the alert flag. Passing "True" also clears the flag

		print("Voltage Low Alert: {}".format(myLipo.is_voltage_low(True)))  # Print the alert flag. Passing "True" also clears the flag

		print("Empty Alert: {}".format(myLipo.is_low()))  # Print the alert flag

		print("SOC 1% Change Alert: {}".format(myLipo.is_change()))  # Print the alert flag
		
		print("Hibernating: {}".format(myLipo.is_hibernating()))  # Print the alert flag
		
		time.sleep(0.5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)