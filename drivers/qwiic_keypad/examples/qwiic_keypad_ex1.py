#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_env_keypad_ex1.py
#
# Simple Example for the Qwiic Keypad Device
# This example prints which button was pressed. Press * for space and # for new line.
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
# Example 1
#

import qwiic_keypad
import time
import sys

def runExample():

	print("\nSparkFun qwiic Keypad   Example 1\n")
	myKeypad = qwiic_keypad.QwiicKeypad()

	if myKeypad.connected == False:
		print("The Qwiic Keypad device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myKeypad.begin()

	print("Initialized. Firmware Version: %s" % myKeypad.version)
	print("Press a button: * to do a space. # to go to next line.")

	button = 0
	while True:

		# necessary for keypad to pull button from stack to readable register
		myKeypad.update_fifo()  
		button = myKeypad.get_button()

		if button == -1:
			print("No keypad detected")
			time.sleep(1)

		elif button != 0:

			# Get the character version of this char
			charButton = chr(button)
			if charButton == '#':
				print()
			elif charButton == '*':
				print(" ", end="")
			else: 
				print(charButton, end="")

			# Some platforms won't print until newline character, so a flush is
			# needed to update. However some platforms (eg. MicroPython) don't
			# include sys.stdout.flush(), so wrap in a try block
			try:
				sys.stdout.flush()
			except:
				pass

		time.sleep(.25)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)


