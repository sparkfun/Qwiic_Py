#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_otos_ex5_velocity_and_acceleration.py
#
# This example demonstrates how to read the velocity and acceleration from the
# SparkFun Qwiic Optical Tracking Odometry Sensor (OTOS).

# The primary purpose of the OTOS is to track position, but it also provides
# velocity and acceleration measurements for more advanced applications. Note
# that these measurements can be noisy and inaccurate, especially if the
# sensor is not flat to the ground.
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
import qwiic_i2c

def run_example():
    print("\nQwiic OTOS Example 5 - Velocity and Acceleration\n")

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
        # These values can be read individually like so:
        pos = my_otos.get_position()
        vel = my_otos.get_velocity()
        acc = my_otos.get_acceleration()

        # Or burst read them all at once with the following:
        # (pos, vel, acc) = my_otos.get_pos_vel_acc()

        # Print position
        print()
        print("Position:")
        print("X (Inches): {}".format(pos.x))
        print("Y (Inches): {}".format(pos.y))
        print("Heading (Degrees): {}".format(pos.h))
        
        # Print velocity
        print()
        print("Velocity:")
        print("X (Inches/sec): {}".format(vel.x))
        print("Y (Inches/sec): {}".format(vel.y))
        print("Heading (Degrees/sec): {}".format(vel.h))
        
        # Print acceleration
        print()
        print("Acceleration:")
        print("X (Inches/sec^2): {}".format(acc.x))
        print("Y (Inches/sec^2): {}".format(acc.y))
        print("Heading (Degrees/sec^2): {}".format(acc.h))

        # Wait a bit so we don't spam the serial port
        qwiic_i2c.delay_ms(500)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Example")
        sys.exit(0)