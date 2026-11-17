#-------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
# 
# Copyright (c) 2025 SparkFun Electronics
#-------------------------------------------------------------------------------
# ex2_learn.py
#
# This example shows how to learn new objects with the HuskyLens over I2C rather
# than using the buttons on the device. This gives some more flexibility in how
# objects are learned, such as being able to set the names and ID values.
#-------------------------------------------------------------------------------

import qwiic_huskylens 
import sys
import time

def runExample():
    print("\nQwiic HuskyLens Example 2 - Learn\n")

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

    # Uncomment one of these lines to set the algorithm to use
    algorithm = myHuskyLens.kAlgorithmFaceRecognition
    # algorithm = myHuskyLens.kAlgorithmObjectTracking
    # algorithm = myHuskyLens.kAlgorithmObjectRecognition
    # algorithm = myHuskyLens.kAlgorithmLineTracking
    # algorithm = myHuskyLens.kAlgorithmColorRecognition
    # algorithm = myHuskyLens.kAlgorithmTagRecognition
    # algorithm = myHuskyLens.kAlgorithmObjectClassification

    # Set the algorithm to use
    myHuskyLens.set_algorithm(algorithm)

    # Ask user if they want to forget all learned data for this algorithm
    print()
    print("Would you like to forget all learned data for this algorithm?")
    if input("Enter 'y' to forget, or anything else to skip: ") == 'y':
        print("Forgetting all learned data...")
        myHuskyLens.forget()

    # Learn loop
    while True:
        # Prompt user to point the HuskyLens at something to learn
        print()
        print("Point the HuskyLens at something new to learn!")
        val = input("Enter 'q' to quit, or anything else to learn the new object: ")
        if val == 'q':
            break

        # Wait for the HuskyLens to see something
        if algorithm == myHuskyLens.kAlgorithmLineTracking:
            myHuskyLens.wait_for_lines_of_interest()
        else:
            myHuskyLens.wait_for_objects_of_interest()

        # When the device sees something, let's learn it!
        myHuskyLens.learn_new()
        print("Learned something new!")

        # Prompt user to name what was just learned
        print()
        print("Would you like to name what was just learned?")
        print("The HuskyLens will show this name when it recognizes the object.")
        name = input("Enter a name, or enter nothing to clear the name: ")
        myHuskyLens.name_last(name)
        if name == '':
            print("Name cleared")
        else:
            print("Name set to: " + name)

        # Ask user if they want to continue learning the same thing
        print()
        print("Would you like to continue learning the same thing?")
        print("This can improve the recognition accuracy!")
        if input("Enter 'y' to continue learning, or anything else to skip: ") != 'y':
            continue

        # Loop to continue learning the same thing
        while True:
            # Prompt user to learn the same thing again
            print()
            print("Point the HuskyLens at the same thing again.")
            val = input("Enter 'q' to quit, or anything else to continue learning: ")
            if val == 'q':
                break

            # Wait for the HuskyLens to see something
            if algorithm == myHuskyLens.kAlgorithmLineTracking:
                myHuskyLens.wait_for_lines_of_interest()
            else:
                myHuskyLens.wait_for_objects_of_interest()

            # When the device sees something, let's learn it again!
            myHuskyLens.learn_same()
            print("Learned the same thing again!")

    # Instead of `learn_new()` and `learn_same()`, you can also use
    # `request_learn(id)` to manually specify the ID value to use. This can be
    # useful if you want to manage the ID values yourself. If the provided ID
    # is already in use, the HuskyLens use what it sees to improve the existing
    # recognition for that ID.
    # myHuskyLens.request_learn(id)

    # Instead of `name_last(name)`, you can use `request_custom_names(id, name)`
    # to manually specify the ID value to name. This can be useful if you want
    # to set the names of objects after learning, or rename objects. Setting
    # `name=''` will clear the name for that ID.
    # myHuskyLens.request_custom_name(id, name)

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
