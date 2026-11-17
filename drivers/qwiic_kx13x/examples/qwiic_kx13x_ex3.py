#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_kx13x_ex3.py
#
#  This example shows both how to setup the buffer but also how to route the buffer's
#  interrupt to a physical interrupt pin.
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
import time
import sys

def runExample():

    print("\nSparkFun KX13X Accelerometer Example 3\n")
    # myKx = qwiic_kx13x.QwiicKX134() # If using the KX134 un-comment this line and replace other instances of "kx132" with "kx134"
    myKx = qwiic_kx13x.QwiicKX132()

    if myKx.connected == False:
            print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection", \
                    file=sys.stderr)
            return

    if myKx.begin():
        print("Ready.")
    else:
        print("Make sure you're using the KX132 and not the KX134")

    if (myKx.software_reset()):
        print("Reset")

    # Many settings for KX13X can only be
    # applied when the accelerometer is powered down.
    # However there are many that can be changed "on-the-fly"
    # check datasheet for more info
    myKx.enable_accel(False)
    
    myKx.enable_buffer_and_interrupt()
    myKx.enable_phys_interrupt()
    myKx.route_hardware_interrupt(0x40)

    myKx.set_buffer_operation_and_resolution(0x00)
    
    # myKx.set_range(myKx.KX134_RANGE8G)  # If using the KX134 un-comment this line and comment out below line
    myKx.set_range(myKx.KX132_RANGE2G)
    myKx.enable_accel()

    while True:
        if myKx.get_sample_level() > 0:

            # We can read the data more quickly by calling getRawAccelBufferData because we know
            # the buffer is being used and what the data resolution is.
            # The default buffer resolution is 8-bit. It will be 16-bit because we called setBufferResolution above.
            # If you comment setBufferResolution, change the '1' to a '0' for 8-bit data.

            if myKx.get_raw_accel_buffer_data(1): # Change the '1' to a '0' for 8-bit data.
                myKx.conv_accel_data()
                # If using the KX134 un-comment the print below and comment out the print below that
                # print("\nX: {0} Y: {1} Z: {2}".format(myKx.kx134_accel.x,
                #                         myKx.kx134_accel.y,
                #                         myKx.kx134_accel.z))
                print("\nX: {0} Y: {1} Z: {2}".format(myKx.kx132_accel.x,
                                                    myKx.kx132_accel.y,
                                                    myKx.kx132_accel.z))
        else:
            print(".",end="")
            time.sleep(.001) # wait 1 ms between checks

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)
