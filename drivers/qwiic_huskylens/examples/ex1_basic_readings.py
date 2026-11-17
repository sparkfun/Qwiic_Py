#-------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
# 
# Copyright (c) 2025 SparkFun Electronics
#-------------------------------------------------------------------------------
# ex1_basic_readings.py
#
# This example shows how to get data from the HuskyLens. Set the HuskyLens to
# any algorithm, point it at something it can recognize, and this example will
# print the details of what it sees.
#-------------------------------------------------------------------------------

import qwiic_huskylens 
import sys
import time

def runExample():
    print("\nQwiic HuskyLens Example 1 - Basic Readings\n")

    # Create instance of device
    myHuskyLens = qwiic_huskylens.QwiicHuskyLens()

    # Check if it's connected
    if myHuskyLens.is_connected() == False:
        print("Device not connected, please check your connection",
            file=sys.stderr)
        return

    # Initialize the device
    if myHuskyLens.begin() == False:
        print("Failed to initialize the device, please check your connection",
            file=sys.stderr)
        return

    # Main loop
    nScans = 0
    while True:
        # Wait a second between scans
        time.sleep(1)

        # Get all objects and lines found by the HuskyLens
        objects = myHuskyLens.get_objects_of_interest()
        lines = myHuskyLens.get_lines_of_interest()
        
        # If nothing is found, print a message
        if len(objects) == 0 and len(lines) == 0:
            print("Nothing found, point HuskyLens at something it recognizes")
            continue

        # Objects and/or lines were found, list them under a new scan header
        nScans += 1
        print("--------------------Scan #{}--------------------".format(nScans))

        # Print details of each object found
        for object in objects:
            # Every object has an ID. 0 indicates it's an unknown object
            print("Object ID: " + str(object.id))

            # Every object has a bounding box, defined by its center point, and
            # its width and height
            print("Object X: " + str(object.xCenter))
            print("Object Y: " + str(object.yCenter))
            print("Object Width: " + str(object.width))
            print("Object Height: " + str(object.height))
            print()

        # Print details of each line found
        for line in lines:
            # Every line has an ID. 0 indicates it's an unknown line
            print("Line ID: " + str(line.id))

            # Every line has a starting point and an ending point
            print("Line X1: " + str(line.xOrigin))
            print("Line Y1: " + str(line.yOrigin))
            print("Line X2: " + str(line.xTarget))
            print("Line Y2: " + str(line.yTarget))
            print()

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
