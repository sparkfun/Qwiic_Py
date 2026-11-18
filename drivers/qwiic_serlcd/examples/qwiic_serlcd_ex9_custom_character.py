#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_serlcd_ex9_custom_character.py
#
# This example prints "I <heart> SerLCD!" and a little dancing man
# to the LCD.
#
# Custom characters are recorded to SerLCD and are remembered even after power is lost.
# There is a maximum of 8 custom characters that can be recorded.
#
#------------------------------------------------------------------------
#
# Written by SparkFun Electronics, August 2020
#
# Ported from Arduino Library code with many contributions from
# Gaston Williams - August 29, 2018
# 
# Based on Adafruit's example at
#  
# https://github.com/adafruit/SPI_VFD/blob/master/examples/createChar/createChar.pde
#
# This example code is in the public domain.
# http://www.arduino.cc/en/Tutorial/LiquidCrystalCustomCharacter
#
# Also useful:
# http://icontexto.com/charactercreator/
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
# Example 9
#

import qwiic_serlcd
import qwiic_i2c
import sys

def run_example():

	print("\nSparkFun Qwiic SerLCD   Example 9\n")
	myLCD = qwiic_serlcd.QwiicSerLCD()

	if not myLCD.is_connected():
		print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myLCD.set_backlight(255, 255, 255) # Set backlight to bright white
	myLCD.set_contrast(5) # set contrast. Lower to 0 for higher contrast.
	myLCD.begin() # call this for default settings (no
	myLCD.left_to_right()
	qwiic_i2c.delay_ms(1000) # give a sec for system messages to complete
	
	# make some custom characters:
	heart = [ 
	0b00000, 
	0b01010, 
	0b11111, 
	0b11111, 
	0b11111, 
	0b01110, 
	0b00100, 
	0b00000]

	smiley = [
	0b00000,
	0b00000,
	0b01010,
	0b00000,
	0b00000,
	0b10001,
	0b01110,
	0b00000]

	frownie = [
	0b00000,
	0b00000,
	0b01010,
	0b00000,
	0b00000,
	0b00000,
	0b01110,
	0b10001]

	armsDown = [
	0b00100,
	0b01010,
	0b00100,
	0b00100,
	0b01110,
	0b10101,
	0b00100,
	0b01010]

	armsUp = [
	0b00100,
	0b01010,
	0b00100,
	0b10101,
	0b01110,
	0b00100,
	0b00100,
	0b01010]

	myLCD.create_char(0, heart)
	myLCD.create_char(1, smiley)
	myLCD.create_char(2, frownie)
	myLCD.create_char(3, armsDown)
	myLCD.create_char(4, armsUp)

	myLCD.set_cursor(0,0) # set cursor to the top left

	# Print a message to the LCD.
	myLCD.print("I ")
	myLCD.write_char(0) # Print the heart character, stored in location 0
	myLCD.print(" SerLCD! ")
	myLCD.write_char(1) # Print smiley

	while True:

		myLCD.set_cursor(4,1) # column, row
		myLCD.write_char(3) # print little man, arms down
		qwiic_i2c.delay_ms(200)

		myLCD.set_cursor(4,1) # column, row
		myLCD.write_char(4) # print little man, arms up
		qwiic_i2c.delay_ms(200)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 9")
		sys.exit(0)


