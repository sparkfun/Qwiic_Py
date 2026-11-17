# !/usr/bin/env python
# ----------------------------------------------------------------
# qwiic_rfid_ex3.py
#
# Example that takes user input to change the I2C address of Qwiic RFID
# ----------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, January 2021
#
# This python library supports the SparkFun Electronics qwiic 
# sensor/board ecosystem on a Raspberry Pi (and compatible) single
# board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SParkFun. Buy a board!
# https://www.sparkfun.com/products/15191
# 
# ================================================================
# Copyright (c) 2021 SparkFun Electronics
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
# Example 3
#
# This example code demonstrates how to change the address of the Qwiic RFID Tag
# Reader to one of your choosing. There is a set range of available addresses from
# 0x07 to 0x78, so make sure your chosen address falls within this range.

import qwiic_rfid
import time
import sys

# If you've already changed the I2C address, change this to the current address!
currentAddress = qwiic_rfid._AVAILABLE_I2C_ADDRESS[0]

def run_example():

    print("\nSparkFun Qwiic RFID Reader Example 3")
    my_RFID = qwiic_rfid.QwiicRFID(currentAddress)

    if my_RFID.begin() == False:
        print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    print("\nReady!")

    print("Enter a new I2C address for the Qwiic RFID Reader to use.")
    print("Any address from 0x08 to 0x77 works.")
    print("Don't use the 0x prefix. For instance if you wanted to")
    print("change the address to 0x5B, you would type 5B and hit enter.")

    new_address = input("New Address: ")
    new_address = int(new_address, 16)

    # Check if the user entered a valid address
    if new_address >= 0x08 and new_address <= 0x77:
        print("Characters received and new address valid!")
        print("Attempting to set RFID reader address...")
        
        my_RFID.change_address(new_address)
        print("Address successfully changed!")
        # Check that the RFID Reader acknowledges on new address
        time.sleep(0.02)
        if my_RFID.begin() == False:
            print("The Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)

        else:
            print("RFID Reader acknowledged on new address!")
    
    else: 
        print("Address entered not a valid I2C address")

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 3")
        sys.exit(0)
