#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex2_set_units.py
#
# This example demonstrates how to change the units of the SparkFun Qwiic
# Optical Tracking Odometry Sensor (OTOS).

# The OTOS library defaults to inches and degrees, but you can change the
# units to suit the needs of your project.
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
    print("\nQwiic OTOS Example 2 - Set Units\n")

    # Create instance of device
    myOtos = qwiic_otos.QwiicOTOS()

    # Check if it's connected
    if myOtos.is_connected() == False:
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    # Initialize the device
    myOtos.begin()

    print("Ensure the OTOS is flat and stationary during calibration!")
    for i in range(5, 0, -1):
        print("Calibrating in %d seconds..." % i)
        time.sleep(1)

    print("Calibrating IMU...")

    # Calibrate the IMU, which removes the accelerometer and gyroscope offsets
    myOtos.calibrateImu()

    # Set the desired units for linear and angular measurements. Can be either
    # meters or inches for linear, and radians or degrees for angular. If not
    # set, the default is inches and degrees. Note that this setting is not
    # stored in the sensor, it's part of the library, so you need to set at the
    # start of all your programs.
    myOtos.setLinearUnit(myOtos.kLinearUnitMeters)
    # myOtos.setLinearUnit(myOtos.kLinearUnitInches)
    myOtos.setAngularUnit(myOtos.kAngularUnitRadians)
    # myOtos.setAngularUnit(myOtos.kAngularUnitDegrees)

    # Reset the tracking algorithm - this resets the position to the origin,
    # but can also be used to recover from some rare tracking errors
    myOtos.resetTracking()

    # Main loop
    while True:
        # Get the latest position, which includes the x and y coordinates, plus
        # the heading angle
        myPosition = myOtos.getPosition()

        # Print measurement
        print()
        print("Position:")
        print("X (Meters): {}".format(myPosition.x))
        print("Y (Meters): {}".format(myPosition.y))
        print("Heading (Radians): {}".format(myPosition.h))

        # Wait a bit so we don't spam the serial port
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)