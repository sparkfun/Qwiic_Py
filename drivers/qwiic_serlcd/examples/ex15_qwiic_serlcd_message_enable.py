#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex15_qwiic_serlcd_message_enable.py
#
# This example demonstrates how to turn off the system messages displayed when
# the user changes a setting. For instance 'Contrast: 5' or 'Backlight: 100%' is
# no longer displayed.
#
# Note - This example and the disableSystemMessages() and enableSystemMessages() 
# commands are only supported on SerLCD v1.2 and above.
#
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, August 2020
#
# Ported from Arduino Library code with many contributions from
# Gaston Williams - August 29, 2018
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
# Example 15
#

import qwiic_serlcd
import time
import sys

def runExample():

	print("\nSparkFun Qwiic SerLCD   Example 15\n")
	print("\nType CTRL+C to end.\n")
	myLCD = qwiic_serlcd.QwiicSerlcd()

	if myLCD.connected == False:
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLCD.setBacklight(255, 255, 255) # bright white
	myLCD.setContrast(5) # set contrast. Lower to 0 for higher contrast.
	myLCD.begin() # call this for default settings (no
	myLCD.leftToRight()
	myLCD.noCursor()
	time.sleep(1) # give a sec for system messages to complete

	myLCD.disableSystemMessages() # Now whenever you change a system setting like Contrast,
	# SerLCD will not display the setting. This makes changing the setting faster, and also
	# invisible to the user.

	#myLCD.enableSystemMessages() # This will re-enable the printing of system messages

	myLCD.clearScreen()
	myLCD.print("Hello World!")

	counter = 0

	while True:		
		# do something that would normally cause a system message
		# let's change color of backlight values every other count value
		if (counter % 2) == 0:
			myLCD.setBacklight(255, 0, 0)
		else:
			myLCD.setBacklight(0, 255, 0)

		time.sleep(0.1) # give it a sec to change backlight
		
		print("counter: %d" % counter)
		myLCD.setCursor(0,1)
		myLCD.print(str(counter))
		counter = counter + 1
		time.sleep(1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 15")
		sys.exit(0)


