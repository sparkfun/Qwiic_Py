#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_tca9548a_ex2.py
#
# Example for the Qwiic 8 Channel Mux interfacing with two Qwiic VL53L1X Distance Sensors
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
#   This example shows how to hook up two VL53L1X laser distance sensors with the same address.
#   You can read the VL53L1X hookup guide and get the library from https://learn.sparkfun.com/tutorials/qwiic-distance-sensor-vl53l1x-hookup-guide
#==================================================================================
# Hardware Connections: 
#   Attach the Qwiic Mux Board to your control board with a Qwiic cable to the "Main" port on the Mux Board
#   Plug a VL53L1X device into port 0 and another into port 1
#==================================================================================

import qwiic_tca9548a
import qwiic_vl53l1x # Get the library here: https://github.com/sparkfun/Qwiic_VL53L1X_Py/tree/master or with mip
import qwiic_i2c
import time
import sys

NUMBER_OF_SENSORS = 2 # Change this number if you have more than 2 VL53L1X sensors. Connect all sensors to lowest available ports on MUX

def runExample():
    print("\nSparkFun TCA9548A 8-Channel Mux Example 2\n")

    # Create an instance of our MUX object
    myTca = qwiic_tca9548a.QwiicTCA9548A()
    
    if myTca.connected == False:
        print("The Qwiic TCA9548A 8-Channel Mux device isn't connected to the system. Please check your connection", \
                file=sys.stderr)
        return
    
    # Create a list of distance sensor objects
    distance_sensors = [None] * NUMBER_OF_SENSORS

    for i in range(NUMBER_OF_SENSORS):
        distance_sensors[i] = qwiic_vl53l1x.QwiicVL53L1X()

    # We will use this object to see what devices are connected to the master after configuring the MUX
    i2c = qwiic_i2c.getI2CDriver()

    print("Disabling all MUX Ports")
    myTca.disable_all()
    myTca.list_channels()

    # Now configure each sensor one at a time
    for i in range(NUMBER_OF_SENSORS):
        print("Enabling sensor on channel", i)
        myTca.disable_all()
        myTca.enable_channels([i])

        # If a device is connected, initialize it
        while True:
            if distance_sensors[i].sensor_init() == None:
                print("Sensor", i, " connected!")
                break
            else:
                print("Sensor", i, " not connected! Retrying...")

    while True:
        # Loop through each sensor and enable its MUX channel then read the distance
        for i in range(NUMBER_OF_SENSORS):
            # Enable the MUX channel for the sensor we want to read
            myTca.disable_all()
            myTca.enable_channels([i])

            # Read distance from the sensor
            distance_sensors[i].start_ranging()
            time.sleep(0.005)
            distance = distance_sensors[i].get_distance()
            time.sleep(0.005)
            distance_sensors[i].stop_ranging()

            distanceInches = distance / 25.4
            distanceFeet = distanceInches / 12.0

            print("Distance", i, "(in): ", distanceInches, "    Distance", i, "(ft): ", distanceFeet)

        time.sleep(0.5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 2")
		sys.exit(0)
