#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_env_keypad_ex3.py
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
import time
import sys


# the correct keyCode - change to your own unique set of keys if you like.
keyCode = ['1', '2', '3', '4'] 

def runExample():
	# used to store the presses coming in from user. init with blanks
	userEntry = [' ']*len(keyCode)
	# used to know when a user is active and therefore we want to engage timeout stuff
	userIsActive = False

	TIMEOUT=30  # in 100s of millisecs

	timeOutCounter = 0  # variable this is incremented to keep track of timeouts.
	userEntryIndex = 0 # used to keep track of where we are in the userEnt

	print("\nSparkFun qwiic Keypad   Example 3\n")
	myKeypad = qwiic_keypad.QwiicKeypad()

	if myKeypad.connected == False:
		print("The Qwiic Keypad device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myKeypad.begin()

	print("Initialized. Firmware Version: %s" % myKeypad.version)
	print("Please type in the correct 4 digit KeyCode:")


	button = 0
	while True:

		# necessary for keypad to pull button from stack to readable register
		myKeypad.update_fifo()  
		button = myKeypad.get_button()

		if button == -1:
			print("No keypad detected")
			time.sleep(1)

		elif button > 100:
			# At startup a series 127's come accoss -- way out of range
			# just noise
			# Skip
			pass
		elif button != 0:
			# store button into next spot in array, note, index is incremented later
			userEntry[userEntryIndex] = chr(button)

			printEntry(userEntry)
			userIsActive = True  # used to only timeout when user is active

			if checkEntry(userEntry):
				print("\n\nKeycode correct. Wahooooooooooo!")
				userIsActive = False # don't display timeout stuff.
				time.sleep(1)
		
			userEntryIndex += 1
			if userEntryIndex == len(keyCode):
				userEntryIndex = 0 # reset

				printEntry(userEntry)
				time.sleep(.3)
				clearEntry(userEntry)	
				printEntry(userEntry)			
			timeOutCounter = 0 #reset with any new presses.

		time.sleep(.2)
		timeOutCounter += 1

	# this means the user is actively inputing		
	if timeOutCounter == TIMEOUT  and userIsActive == True: 
		print("\n\nTimed out... try again.")
		timeOutCounter = 0
		userEntryIndex = 0
		clearEntry(userEntry)
		userIsActive = False # so we don't continuously timeout while inactive.

#  check user entry against keyCode array.
#  if they all match up, then respond with true.
def checkEntry(userEntry):

	for i in range(len(keyCode)):
		if userEntry[i] != keyCode[i]:
			return False

	return True 

#  "clear" entry with all spaces
def clearEntry(userEntry):

	userEntry[:] = [' ']*len(userEntry)

def printEntry(userEntry):

	print("\rUserEntry:%s" % (''.join(userEntry)), end="")
	# Some platforms won't print until newline character, so a flush is
	# needed to update. However some platforms (eg. MicroPython) don't
	# include sys.stdout.flush(), so wrap in a try block
	try:
		sys.stdout.flush()
	except:
		pass


if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


