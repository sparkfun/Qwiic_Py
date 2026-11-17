#-------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
# 
# Copyright (c) 2025 SparkFun Electronics
#-------------------------------------------------------------------------------
# ex3_write_to_screen.py
#
# This example shows how to write text to the screen of the HuskyLens.
#-------------------------------------------------------------------------------

import qwiic_huskylens 
import sys
import time

def runExample():
    print("\nQwiic HuskyLens Example 3 - Write to Screen\n")

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
    while True:
        # We can write up to 20 characters at a time. The last 2 parameters are
        # optional x and y coordinates to position the text on the screen, which
        # default to 0, 0 (top left corner)
        print("Writing to screen")
        myHuskyLens.write_to_screen("Hello, World!", 0, 0) 
        time.sleep(2)
        
        print("Writing to screen elsewhere")
        myHuskyLens.write_to_screen("Goodbye, World!", 50, 50)
        time.sleep(2)
        
        # The text will stay on the screen until we clear it
        print("Clearing the screen")
        myHuskyLens.clear_screen()
        time.sleep(2)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example")
        sys.exit(0)
