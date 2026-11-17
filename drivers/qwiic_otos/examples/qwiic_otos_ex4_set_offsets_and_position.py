#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex4_set_offsets_and_position.py
#
# This example demonstrates how to set the offset and position of the SparkFun
# Qwiic Optical Tracking Odometry Sensor (OTOS).

# If your OTOS is mounted to a robot and is not centered, you can specify the
# offset for the sensor relative to the center of the robot; rather than
# returning the position of the sensor, the OTOS will calculate and return the
# position of the robot's center. If you know where your robot is located,
# such as the starting location or from another sensor, you can send that
# position to the OTOS and it will continue to track from there.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, May 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https:#www.sparkfun.com/qwiic
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
    print("\nQwiic OTOS Example 4 - Set Offsets and Position\n")

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

    # Assuming you've mounted your sensor to a robot and it's not centered,
    # you can specify the offset for the sensor relative to the center of the
    # robot. The units default to inches and degrees, but if you want to use
    # different units, specify them before setting the offset! Note that as of
    # firmware version 1.0, these values will be lost after a power cycle, so
    # you will need to set them each time you power up the sensor. For example,
    # if the sensor is mounted 5 inches to the left (negative X) and 10 inches
    # forward (positive Y) of the center of the robot, and mounted 90 degrees
    # clockwise (negative rotation) from the robot's orientation, the offset
    # would be {-5, 10, -90}. These can be any value, even the angle can be
    # tweaked slightly to compensate for imperfect mounting (eg. 1.3 degrees).
    offset = qwiic_otos.Pose2D(-5, 10, -90)
    myOtos.setOffset(offset)

    # Reset the tracking algorithm - this resets the position to the origin,
    # but can also be used to recover from some rare tracking errors
    myOtos.resetTracking()

    # After resetting the tracking, the OTOS will report that the robot is at
    # the origin. If your robot does not start at the origin, or you have
    # another source of location information (eg. vision odometry), you can set
    # the OTOS location to match and it will continue to track from there.
    currentPosition = qwiic_otos.Pose2D(0, 0, 0)
    myOtos.setPosition(currentPosition)

    # Main loop
    while True:
        # Get the latest position, which includes the x and y coordinates, plus
        # the heading angle
        myPosition = myOtos.getPosition()

        # Print measurement
        print()
        print("Position:")
        print("X (Inches): {}".format(myPosition.x))
        print("Y (Inches): {}".format(myPosition.y))
        print("Heading (Degrees): {}".format(myPosition.h))

        # Wait a bit so we don't spam the serial port
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)