#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_serlcd_ex17_change_i2c_address.py
#
# This example demonstrates how to change the i2c address on your LCD.
# Note, once you change the address, then you will need to intatiate your class
# using your new address.
#
# Once you have changed the address, you can try using the optional instantiation
# line of code that is currently commented out.
#
# There is a set range of available addresses from 0x07 to 0x78, so make sure your 
# chosen address falls within this range. 
# 
# The next thing to note is that when you change the address you'll
# need to call an instance of the QwiicSerLCD class that includes your new
# address, like so: "myLCD = qwiic_serlcd.QwiicSerLCD(address=YOUR_NEW_ADDRESS_HERE)"
# so that the new address is fed to all the available functions. 
# 
# Finally if for some reason you've forgotten your new address. No big deal, run a 
# hardware reset on your screen to get it back to the default address (0x72).
# To cause a hardware reset, simply tie the RX pin LOW, and they cycle power 
# (while continuing to hold RX low). Then release RX, and cycle power again.
#
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, August 2020
#
# Ported from Arduino Library code with many contributions from
# Gaston Williams - August 29, 2018
#
# Some code/comments/ideas ported from the Qwiic Quad Relay Arduino Library
# Written by Elias Santistevan, July 2019
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
# Copyright (c) 2020 SparkFun Electronics
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
# Example 17
#

import qwiic_serlcd
import qwiic_i2c
import sys

old_address = 0x72 # default
new_address = 0x71 # must be within 0x07 to 0x78, DEFAULT: 0x72

def run_example():

	print("\nSparkFun Qwiic SerLCD   Example 17\n")
	print("\nType CTRL+C to end.\n")
	myLCD = qwiic_serlcd.QwiicSerLCD(address=old_address)

	print("Attemping to connect to %s..." % hex(myLCD.address))

	if not myLCD.is_connected():
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	else:
		print("Connected!")
		myLCD.set_backlight(255, 255, 255) # bright white
		myLCD.set_contrast(5) # set contrast. Lower to 0 for higher contrast.
		myLCD.begin() # call this for default settings (no
		myLCD.left_to_right()
		myLCD.no_cursor()
		qwiic_i2c.delay_ms(1000) # give a sec for system messages to complete

		myLCD.clear_screen()

		myLCD.set_address(new_address) # note this updates class member myLCD.address to the new_address
		
		if myLCD.is_connected():
			print("Address changed to %s successfully!" % hex(myLCD.address))
			myLCD.clear_screen()
			myLCD.print("My new add: %s" % hex(myLCD.address))
		else:
			print("Address change failed :(")
	while True:
		qwiic_i2c.delay_ms(1000) # do nothing

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 17")
		sys.exit(0)


