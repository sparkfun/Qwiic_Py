#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_tca9548a_ex1.py
#
# Simple example for the Qwiic 8 Channel Mux
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
# Copyright (c) 2024 SparkFun Electronics
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
# Description: 
#   Some I2C devices respond to only one I2C address. This can be a problem
#   when you want to hook multiple of a device to the I2C bus. An I2C Mux
#   solves this issue by allowing you to change the 'channel' or port that
#   the master is talking to.

#   This example shows how to connect to different ports.
#   First, any devices connected to port 0 and 1 will have their i2c addresses printed, then any devices connected to ports 2 and 3
#   Make sure you do not have multiple devices with the same i2c address connected to BOTH ports 0 and 1, or 2 and 3
#==================================================================================
# Hardware Connections: 
#   Attach the Qwiic Mux Board to your control board with a Qwiic cable to the "Main" port on the Mux Board
#   Plug device(s) into ports 0, 1, 2 and/or 3
#==================================================================================

import qwiic_tca9548a
import qwiic_i2c
import time
import sys

def runExample():

    print("\nSparkFun TCA9548A 8-Channel Mux Example 1\n")
    
    myTca = qwiic_tca9548a.QwiicTCA9548A()

    if myTca.connected == False:
            print("The Qwiic TCA9548A 8-Channel Mux device isn't connected to the system. Please check your connection", \
                    file=sys.stderr)
            return

    # We will use this object to see what devices are connected to the master after configuring the MUX
    i2c = qwiic_i2c.getI2CDriver()

    while True:
        # By enabling channels 0 and 1, our Master device can speak to a device connected to port 0 or 1of the MUX
        print("Enabling channels 0 and 1")
        myTca.disable_all()
        myTca.enable_channels([0,1])
        myTca.list_channels()

        # Find any i2c devices connected to the master, we should see the addresses of any devices we have connected to port 0 or 1 here, 
		# but not any devices connected to other ports.
        print("Checking for i2c devices on ports 0 and 1")
        devices = i2c.scan()
        print("Devices found: ", devices)
        time.sleep(2)
        
        # Enable channels 2 and 3, our Master device can now speak to a device connected to port 2 or 3 of the MUX
        print("Enabling channels 2 and 3")
        myTca.disable_all()
        myTca.enable_channels([2,3])
        myTca.list_channels()

        # Find any i2c devices connected to the master, we should see the addresses of any devices we have connected to port 2 or 3 here,
		# but not any devices connected to other ports.
        print("Checking for i2c devices on ports 2 and 3")
        devices = i2c.scan()
        print("Devices found: ", devices)
        time.sleep(2)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
