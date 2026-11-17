#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_as7265x_ex7_get_version.py
#
# This example shows how to read the temperature of the ICs
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
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
#===============================================================================

import qwiic_as7265x
import sys

def runExample():
    print("\nQwiic Spectral Triad Example 7 - Get Version\n")

    # Create instance of device
    myAS7265x = qwiic_as7265x.QwiicAS7265x()

    # Check if it's connected
    if myAS7265x.is_connected() == False:
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    # Initialize the device
    if myAS7265x.begin() == False:
        print("Unable to initialize the AS7265x. Please check your connection", file = sys.stderr)
        return

    deviceType = myAS7265x.get_device_type()
    hardwareVersion = myAS7265x.get_hardware_version()
    majorFirmwareVersion = myAS7265x.get_major_firmware_version()
    patchFirmwareVersion = myAS7265x.get_patch_firmware_version()
    buildFirmwareVersion = myAS7265x.get_build_firmware_version()

    print("Device Type:", hex(deviceType))
    print("HardwareVersion:", hex(hardwareVersion))
    print("Major Firmware Version:", hex(majorFirmwareVersion))
    print("Patch Firmware Version:", hex(patchFirmwareVersion))
    print("Build Firmware Version:", hex(buildFirmwareVersion))

    return

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)