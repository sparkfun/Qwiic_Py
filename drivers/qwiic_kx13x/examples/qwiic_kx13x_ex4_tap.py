#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_kx13x_ex4_tap.py
#
# Example for the Qwiic KX132/4 Accelerometer that shows the how to enable the tap interrupts.
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, November 2024
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
# Copyright (c) 2021 SparkFun Electronics
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

import qwiic_kx13x
import qwiic_i2c
import sys


print("\nSparkFun KX13X Accelerometer Example 4: Tap\n")
# my_kx = qwiic_kx13x.QwiicKX134() # If using the KX134 un-comment this line and replace other instances of "kx132" with "kx134"
my_kx = qwiic_kx13x.QwiicKX132()

if my_kx.is_connected() == False:
        print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection", \
                file=sys.stderr)
        sys.exit(1)

if my_kx.begin():
    print("Ready.")
else:
    print("Make sure you're using the KX132 and not the KX134")

if (my_kx.software_reset()):
    print("Reset")

# Many settings for KX13X can only be
# applied when the accelerometer is powered down.
# However there are many that can be changed "on-the-fly"
# check datasheet for more info
my_kx.enable_accel(False)
# my_kx.set_range(my_kx.KX134_RANGE16G)  # If using the KX134 un-comment this line and comment out below line
my_kx.set_range(my_kx.KX132_RANGE16G)
my_kx.enable_tap_engine()
my_kx.enable_accel()

while True:
    if my_kx.tap_detected():    
        print("Tap Detected: ", hex(my_kx.get_direction()))
        my_kx.clear_interrupt()

    if my_kx.unknown_tap() or my_kx.double_tap_detected():
        my_kx.clear_interrupt()

    qwiic_i2c.delay_ms(25) # Delay should be 1/ODR (Output Data Rate), default tap ODR is 400Hz
