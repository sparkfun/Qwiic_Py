#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex7_get_version.py
#
# This example demonstrates how to get the hardware and firmware version
# numbers from the SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

# There may be future hardware and/or firmware changes of the OTOS, so you can
# use this example to check which version you have. See the product page or
# hardware repository to see what the latest version is:
# https://www.sparkfun.com/products/24904
# https://github.com/sparkfun/SparkFun_Optical_Tracking_Odometry_Sensor
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, May 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
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
#===============================================================================

import qwiic_otos
import sys
import time

def runExample():
    print("\nQwiic OTOS Example 7 - Get Version\n")

    # Create instance of device
    myOtos = qwiic_otos.QwiicOTOS()

    # Check if it's connected
    if myOtos.is_connected() == False:
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    # Initialize the device
    myOtos.begin()

    # Get the hardware and firmware version
    (hwVersion, fwVersion) = myOtos.getVersionInfo()

    # Extract the major and minor version numbers
    hwMajor = (hwVersion >> 4) & 0x0F
    hwMinor = hwVersion & 0x0F
    fwMajor = (fwVersion >> 4) & 0x0F
    fwMinor = fwVersion & 0x0F

    # Print the hardware and firmware version
    print("OTOS Hardware Version: v{}.{}".format(hwMajor, hwMinor))
    print("OTOS Firmware Version: v{}.{}".format(fwMajor, fwMinor))

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)