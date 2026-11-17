#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_cy8cmbr3_ex2_advanced.py
#
# Shows how to set up and use the Qwiic CY8CMBR3 Capacitive Soil Moisture Sensor
# for advanced soil moisture readings including settings.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, January 2026
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2026 SparkFun Electronics
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

import qwiic_cy8cmbr3
import sys
import time

def runExample():
	print("\nQwiic Template Example 2 - Advanced\n")

	# Create instance of device
	mySoilSensor = qwiic_cy8cmbr3.QwiicCY8CMBR3()

	# Check if it's connected
	if mySoilSensor.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	# Initialize the device
	mySoilSensor.begin()

	# Sensitivity values (counts per pF)
    # kCsSensitivity500CountsPerPf = 0  # 50 counts/0.1pF
    # kCsSensitivity250CountsPerPf = 1  # 50 counts/0.2pF
    # kCsSensitivity167CountsPerPf = 2  # 50 counts/0.3pF
    # kCsSensitivity125CountsPerPf = 3  # 50 counts/0.4pF
	mySoilSensor.set_sensitivity_cs0(mySoilSensor.kCsSensitivity500CountsPerPf)

	# Refresh Intervals
	# See qwiic_cy8cmbr3.py for all options
	mySoilSensor.set_refresh_interval(mySoilSensor.kRefreshInterval100ms)

	mySoilSensor.save_config()

	mySoilSensor.reset()

	# Infinite loop reading data
	while True:
		# Depending on your application, you may want to tune sensitity and refresh interval
		# and you may find any of the following different ways of reading the capacitance counts
		# most useful (balancing accuracy, range, and resolution).

		# Read and print the soil capacitance
		capacitance = mySoilSensor.get_capacitance_pf()
		print("Soil Capacitance: " + str(capacitance) + " pF")
		# Sleep for a second to avoid spamming the output
		
		# Raw count data
		raw_counts = mySoilSensor.get_raw_count()
		print("Soil Raw Count: " + str(raw_counts) + " counts")

		# Baseline counts
		base_counts = mySoilSensor.get_baseline_count()
		print("Soil Baseline Count: " + str(base_counts) + " counts")

		# Delta counts
		delta_counts = mySoilSensor.get_diff_count()
		print("Soil Delta Count: " + str(delta_counts) + " counts")
		
		print("\n--------------------------------\n")

		time.sleep(1)



if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)