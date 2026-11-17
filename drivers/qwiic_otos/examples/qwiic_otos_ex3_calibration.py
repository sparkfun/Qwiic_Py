#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex3_calibration.py
#
# This example demonstrates how to calibrate the SparkFun Qwiic Optical
# Tracking Odometry Sensor (OTOS).

# This example should be used to calibrate the linear and angular scalars of
# the OTOS to get the most accurate tracking performance. The linear scalar
# can be used to compensate for scaling issues with the x and y measurements,
# while the angular scalar can be used to compensate for scaling issues with
# the heading measurement. Note that if the heading measurement is off, that
# can also cause the x and y measurements to be off, so it's recommended to
# calibrate the angular scalar first.
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
    print("\nQwiic OTOS Example 3 - Calibration\n")

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

    # The IMU on the OTOS includes a gyroscope and accelerometer, which could
    # have an offset. Note that as of firmware version 1.0, the calibration
    # will be lost after a power cycle; the OTOS performs a quick calibration
    # when it powers up, but it is recommended to perform a more thorough
    # calibration at the start of all your programs. Note that the sensor must
    # be completely stationary and flat during calibration! When calling
    # calibrateImu(), you can specify the number of samples to take and whether
    # to wait until the calibration is complete. If no parameters are provided,
    # it will take 255 samples and wait until done; each sample takes about
    # 2.4ms, so about 612ms total
    myOtos.calibrateImu()

    # Alternatively, you can specify the number of samples and whether to wait
    # until it's done. If you don't want to wait, you can asynchronously check
    # how many samples remain with the code below. Once zero samples remain,
    # the calibration is done!
    # myOtos.calibrateImu(255, False)
    # done = False
    # while(done == False):
    #     # Check how many samples remain
    #     samplesRemaining = myOtos.getImuCalibrationProgress()

    #     # If 0 samples remain, the calibration is done
    #     if(samplesRemaining == 0):
    #         done = True

    # Here we can set the linear and angular scalars, which can compensate for
    # scaling issues with the sensor measurements. Note that as of firmware
    # version 1.0, these values will be lost after a power cycle, so you will
    # need to set them each time you power up the sensor. They can be any value
    # from 0.872 to 1.127 in increments of 0.001 (0.1%). It is recommended to
    # first set both scalars to 1.0, then calibrate the angular scalar, then
    # the linear scalar. To calibrate the angular scalar, spin the robot by
    # multiple rotations (eg. 10) to get a precise error, then set the scalar
    # to the inverse of the error. Remember that the angle wraps from -180 to
    # 180 degrees, so for example, if after 10 rotations counterclockwise
    # (positive rotation), the sensor reports -15 degrees, the required scalar
    # would be 3600/3585 = 1.004. To calibrate the linear scalar, move the
    # robot a known distance and measure the error; do this multiple times at
    # multiple speeds to get an average, then set the linear scalar to the
    # inverse of the error. For example, if you move the robot 100 inches and
    # the sensor reports 103 inches, set the linear scalar to 100/103 = 0.971
    myOtos.setLinearScalar(1.0)
    myOtos.setAngularScalar(1.0)

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