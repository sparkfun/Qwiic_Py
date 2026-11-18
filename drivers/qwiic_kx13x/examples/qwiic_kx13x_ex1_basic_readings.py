#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_kx13x_ex1_basic_readings.py
#
# Simple example for the Qwiic KX132/4 Accelerometer
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
# Example 1
# A simple example for the kx132 showing the basic settings and functions for retrieving accelerometer
# data

import qwiic_kx13x
import qwiic_i2c
import sys


print("\nSparkFun KX13X Accelerometer Example 1\n")
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
my_kx.enable_data_engine()
my_kx.enable_accel()

while True:
    if my_kx.data_ready():    
        my_kx.get_accel_data()
        # If using the KX134 un-comment the print below and comment out the print below that
        # print("X: {0}g Y: {1}g Z: {2}g".format(my_kx.kx134_accel.x,
        #                         my_kx.kx134_accel.y,
        #                         my_kx.kx134_accel.z))
        print("X: {0} Y: {1} Z: {2}".format(my_kx.kx132_accel.x,
                                            my_kx.kx132_accel.y,
                                            my_kx.kx132_accel.z))
        qwiic_i2c.delay_ms(20) #Set delay to 1/Output Data Rate which is by default 50Hz 1/50 = .02
