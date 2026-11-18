#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_as726x_ex2_settings.py
#
# This example shows how to set custom Gain and Measurement Mode settings with begin()
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
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

import qwiic_as726x
import sys


print("\nQwiic AS726x Example 2 - Settings\n")

# Create instance of device
myAS726x = qwiic_as726x.QwiicAS726x()

# Check if it's connected
if myAS726x.is_connected() == False:
	print("The device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

# Set a desired custom Gain or Measurement Mode here, to be passed to the begin() function
gain = myAS726x.GAIN_1X
# Other possible gain settings:
# GAIN_1X = 0b00 #1x
# GAIN_37X = 0b01 #3.7x 
# GAIN_16X = 0b10 #16x
# GAIN_64X = 0b11 #64x (default)

measurement_mode = myAS726x.MEASUREMENT_MODE_4CHAN
# Other possible measurement modes:
# MEASUREMENT_MODE_4CHAN 	# 4-channel reading 
							# on the as7262: V, B, G, Y (O and R will be 0)
# 							# on the as7263: S, T, U, V (R and W will be 0)
# MEASUREMENT_MODE_4CHAN2	# 4-channel reading, of 2nd set of channels
							# on the as7262: G, Y, O, R (V and B will be 0)
							# on the as7263: R, T, U, W (S and V will be 0)
# MEASUREMENT_MODE_6CHAN_CONTINUOUS # 6-channel continuous reading
# MEASUREMENT_MODE_6CHAN_ONE_SHOT (default) # 6-channel one-shot reading

# Initialize the device with non-default settings
myAS726x.begin(gain, measurement_mode)

while True:
	myAS726x.take_measurements()
	# Check which device is connected
	if myAS726x.get_version() == myAS726x.SENSOR_TYPE_AS7262:
		# Visible readings
		print(" Reading: V[{}] B[{}] G[{}] Y[{}] O[{}] R[{}]".format(
			myAS726x.get_calibrated_violet(),
			myAS726x.get_calibrated_blue(),
			myAS726x.get_calibrated_green(),
			myAS726x.get_calibrated_yellow(),
			myAS726x.get_calibrated_orange(),
			myAS726x.get_calibrated_red()
		), end="")

	elif myAS726x.get_version() == myAS726x.SENSOR_TYPE_AS7263:
		# Near IR readings
		print(" Reading: R[{}] S[{}] T[{}] U[{}] V[{}] W[{}]".format(
			myAS726x.get_calibrated_r(),
			myAS726x.get_calibrated_s(),
			myAS726x.get_calibrated_t(),
			myAS726x.get_calibrated_u(),
			myAS726x.get_calibrated_v(),
			myAS726x.get_calibrated_w()
		), end="")

	print(" tempF[{}]".format(myAS726x.get_temperature_f()))
