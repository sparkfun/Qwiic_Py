#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex6_standard_deviation.py
#
# This example demonstrates how to read the standard deviation of the
# measurements of the SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

# The OTOS uses Kalman filters to estimate the position, velocity, and
# acceleration of the x, y, and heading. The square root of the diagonal
# elements of the covariance matrices are provided for the standard deviation
# of each measurement. THEY DO NOT REPRESENT THE ACTUAL TRACKING ERROR! These
# are statistical quantities that assume a correct model of the system, but
# there could be unmodelled error sources that cause the physical error to
# become larger than these statistical error (eg. improper calibration, or
# tilting the OTOS to not be flat against the tracking surface). These are
# provided primarily for anyone wanting to perform sensor fusion with
# additional sensors.
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
    print("\nQwiic OTOS Example 6 - Standard Deviation\n")

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

    # Reset the tracking algorithm - this resets the position to the origin,
    # but can also be used to recover from some rare tracking errors
    myOtos.resetTracking()

    # Main loop
    while True:
        # Read the position like normal. This example can be extended to include
        # velocity and acceleration, which have been omitted for simplicity, but
        # can be added by uncommenting the code below
        pos = myOtos.getPosition()
        # vel = myOtos.getVelocity()
        # acc = myOtos.getAcceleration()

        # Read the standard deviation of the tracking. Note that these values are
        # just the square root of the diagonal elements of the covariance matrices
        # of the Kalman filters used in the firmware of the OTOS, and THEY DO NOT
        # REPRESENT THE ACTUAL TRACKING ERROR! These are statistical quantities
        # that assume a correct model of the system, but there could be unmodelled
        # error sources that cause the physical error to become larger than these
        # statistical error (eg. improper calibration, or tilting the OTOS to not
        # be flat against the tracking surface). These are provided primarily for
        # anyone wanting to perform sensor fusion with additional sensors.
        posStdDev = myOtos.getPositionStdDev()
        # velStdDev = myOtos.getVelocityStdDev()
        # accStdDev = myOtos.getAccelerationStdDev()

        # These values can instead be burst read out in chunks:
        # (pos, vel, acc) = myOtos.getPosVelAcc()
        # (posStdDev, velStdDev, accStdDev) = myOtos.getPosVelAccStdDev()
        
        # Or burst read them all at once:
        # (pos, vel, acc, posStdDev, velStdDev, accStdDev) = myOtos.getPosVelAccAndStdDev()

        # Print position and standard deviation
        print()
        print("Position:")
        print("X (Inches): {} +/- {}".format(pos.x, posStdDev.x))
        print("Y (Inches): {} +/- {}".format(pos.y, posStdDev.y))
        print("Heading (Degrees): {} +/- {}".format(pos.h, posStdDev.h))

        # Print velocity and standard deviation
        # print()
        # print("Velocity:")
        # print("X (Inches/sec): {} +/- {}".format(vel.x, velStdDev.x))
        # print("Y (Inches/sec): {} +/- {}".format(vel.y, velStdDev.y))
        # print("Heading (Degrees/sec): {} +/- {}".format(vel.h, velStdDev.h))

        # Print acceleration and standard deviation
        # print()
        # print("Acceleration:")
        # print("X (Inches/sec^2): {} +/- {}".format(acc.x, accStdDev.x))
        # print("Y (Inches/sec^2): {} +/- {}".format(acc.y, accStdDev.y))
        # print("Heading (Degrees/sec^2): {} +/- {}".format(acc.h, accStdDev.h))

        # Wait a bit so we don't spam the port
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)