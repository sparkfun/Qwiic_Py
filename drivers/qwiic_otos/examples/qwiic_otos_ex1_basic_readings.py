#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex1_basic_readings.py
#
# This example demonstrates how to read the position and heading from the
# SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).
#
# This example should be used to verify that the OTOS is connected and
# functioning correctly. It will just print the position and heading tracked
# by the OTOS to the serial monitor. It is recommended that you check out the
# other examples before using the OTOS in your own project.
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
import qwiic_i2c

def run_example():
    print("\nQwiic OTOS Example 1 - Basic Readings\n")

    # Create instance of device
    my_otos = qwiic_otos.QwiicOTOS()

    # Check if it's connected
    if not my_otos.is_connected():
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    # Initialize the device
    my_otos.begin()

    print("Ensure the OTOS is flat and stationary during calibration!")
    for i in range(5, 0, -1):
        print("Calibrating in %d seconds..." % i)
        qwiic_i2c.delay_ms(1000)

    print("Calibrating IMU...")

    # Calibrate the IMU, which removes the accelerometer and gyroscope offsets
    my_otos.calibrate_imu()

    # Reset the tracking algorithm - this resets the position to the origin,
    # but can also be used to recover from some rare tracking errors
    my_otos.reset_tracking()

    # Main loop
    while True:
        # Get the latest position, which includes the x and y coordinates, plus
        # the heading angle
        my_position = my_otos.get_position()

        # Print measurement
        print()
        print("Position:")
        print("X (Inches): {}".format(my_position.x))
        print("Y (Inches): {}".format(my_position.y))
        print("Heading (Degrees): {}".format(my_position.h))

        # Wait a bit so we don't spam the serial port
        qwiic_i2c.delay_ms(500)

        # Alternatively, you can comment out the print and delay code above, and
        # instead use the following code to rapidly refresh the data
        # print("{}\t{}\t{}".format(my_position.x, my_position.y, my_position.h))
        # time.sleep(0.01)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example")
        sys.exit(0)