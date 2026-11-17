# !/usr/bin/env python
# ----------------------------------------------------------------
# qwiic_rfid_ex2.py
#
# Basic example that reads RFID tags and prints all the IDs and the 
# times requested in the buffer when prompted by user.
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
# Example 2
#
# This example code demonstrates how to get every RFID card off of the Qwiic RFID
# reader. The Qwiic RFID reader can hold up to 20 cards and their scan times at a
# time. If more than 20 are read then the first card is overwritten. If you
# expect this to be the case then getting the scan time will help to see when the 
# RFID card was scanned. A brief note about time. This time is not the time when the
# RFID card was scanned but the time between when the RFID card was scanned and it 
# was requested by you, the user. There are two time functions available for large 
# reads: getAllTimes() and getAllPrecTimes(), both return time in seconds but the
# second option gives you a time with two decimal point precision (0.00)

import qwiic_rfid
import time
import sys

def run_example():
    
    print("\nSparkFun Qwiic RFID Example 2\n")
    my_RFID = qwiic_rfid.QwiicRFID()

    if my_RFID.begin() == False:
        print("The Qwiic RFID Reader isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nReady to scan some tags!")

    all_tags = [None] * my_RFID.MAX_TAG_STORAGE
    all_times = [None] * my_RFID.MAX_TAG_STORAGE

    while True:
        print("\nScan some tags, they will all be printed in 10 seconds!")

        time.sleep(10)
            
        my_RFID.get_all_tags(all_tags)
        my_RFID.get_all_prec_times(all_times)

        for i in range(0, my_RFID.MAX_TAG_STORAGE):
            if all_tags[i] == "000000":
                break
            
            print("\nScan " + str(i) + ":")
            print("Tag ID: " + all_tags[i])
            print("Scanned " + str(all_times[i]) + " seconds ago")

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 2")
        sys.exit(0)
