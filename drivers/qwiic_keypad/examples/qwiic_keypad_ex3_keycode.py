#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_keypad_ex3_keycode.py
#
# Simple Example for the Qwiic Keypad Device
#  This example waits for the user to input the correct 4 digit keycode,
#  and then responds with a nice message on serial if they get it right.
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
# Example 3
#

import qwiic_keypad
import qwiic_i2c
import sys


# the correct keyCode - change to your own unique set of keys if you like.
keyCode = ['1', '2', '3', '4'] 

def run_example():
	# used to store the presses coming in from user. init with blanks
	user_entry = [' ']*len(keyCode)
	# used to know when a user is active and therefore we want to engage timeout stuff
	userIsActive = False

	TIMEOUT=30  # in 100s of millisecs

	timeOutCounter = 0  # variable this is incremented to keep track of timeouts.
	userEntryIndex = 0 # used to keep track of where we are in the userEnt

	print("\nSparkFun qwiic Keypad   Example 3\n")
	myKeypad = qwiic_keypad.QwiicKeypad()

	if not myKeypad.is_connected():
		print("The Qwiic Keypad device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myKeypad.begin()

	print("Initialized. Firmware Version: %s" % myKeypad.get_version())
	print("Please type in the correct 4 digit KeyCode:")


	button = 0
	while True:

		# necessary for keypad to pull button from stack to readable register
		myKeypad.update_fifo()  
		button = myKeypad.get_button()

		if button == -1:
			print("No keypad detected")
			qwiic_i2c.delay_ms(1000)

		elif button > 100:
			# At startup a series 127's come accoss -- way out of range
			# just noise
			# Skip
			pass
		elif button != 0:
			# store button into next spot in array, note, index is incremented later
			user_entry[userEntryIndex] = chr(button)

			print_entry(user_entry)
			userIsActive = True  # used to only timeout when user is active

			if check_entry(user_entry):
				print("\n\nKeycode correct. Wahooooooooooo!")
				userIsActive = False # don't display timeout stuff.
				qwiic_i2c.delay_ms(1000)
		
			userEntryIndex += 1
			if userEntryIndex == len(keyCode):
				userEntryIndex = 0 # reset

				print_entry(user_entry)
				qwiic_i2c.delay_ms(300)
				clear_entry(user_entry)	
				print_entry(user_entry)			
			timeOutCounter = 0 #reset with any new presses.

		qwiic_i2c.delay_ms(200)
		timeOutCounter += 1

	# this means the user is actively inputing
	if timeOutCounter == TIMEOUT  and userIsActive == True: 
		print("\n\nTimed out... try again.")
		timeOutCounter = 0
		userEntryIndex = 0
		clear_entry(user_entry)
		userIsActive = False # so we don't continuously timeout while inactive.

#  check user entry against keyCode array.
#  if they all match up, then respond with true.
def check_entry(user_entry):

	for i in range(len(keyCode)):
		if user_entry[i] != keyCode[i]:
			return False

	return True 

#  "clear" entry with all spaces
def clear_entry(user_entry):

	user_entry[:] = [' ']*len(user_entry)

def print_entry(user_entry):

	print("\rUserEntry:%s" % (''.join(user_entry)), end="")
	# Some platforms won't print until newline character, so a flush is
	# needed to update. However some platforms (eg. MicroPython) don't
	# include sys.stdout.flush(), so wrap in a try block
	try:
		sys.stdout.flush()
	except AttributeError:
		pass


if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


