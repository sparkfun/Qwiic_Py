#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_proximity_ex5_advanced_settings.py
#
# Simple Example for the Qwiic Proximity Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
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
# Example 5 - Advanced Settings
#

import qwiic_proximity
import qwiic_i2c
import sys


print("\nSparkFun Proximity Sensor VCN4040 Example 5\n")
oProx = qwiic_proximity.QwiicProximity()

if not oProx.is_connected():
	print("The Qwiic Proximity device isn't connected to the system. Please check your connection", \
		file=sys.stderr)
	sys.exit(1)

# begin Setup
oProx.begin()

oProx.power_on_ambient()  	# Power Up the ambient sensor

# Set the integration time for the proximity sensor
# 1 to 8 is valid
oProx.set_prox_integration_time(8)

# Set the integration time for the ambient light sensor in milliseconds
# 80 to 640ms is valid
oProx.set_ambient_integration_time(80)

# If sensor sees more than this, interrupt pin will go low
oProx.set_prox_high_threshold(2000)

# The int pin will stay low until the value goes below the low threshold value
oProx.set_prox_low_threshold(150)

# Enable both 'away' and 'close' interrupts
oProx.set_prox_interrupt_type(oProx.VCNL4040_PS_INT_BOTH)

# This causes the int pin to go low every time a reading is outside the thresholds
# Get a multimeter and probe the INT pin to see this feature in action
oProx.enable_prox_logic_mode()

while True:

	proxValue = oProx.get_proximity()
	print("Proximity Value: \t[%5d]" % proxValue)

	ambientValue = oProx.get_ambient()
	print("Ambient Value: \t\t[%5d]\n" % ambientValue)


	qwiic_i2c.delay_ms(1000)
