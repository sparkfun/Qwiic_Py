# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_eeprom_ex2_settings.py
#
# This example demonstrates how to set the various settings for a given EEPROM.
# Read the datasheet! Each EEPROM will have specific values for: 
# Overall EEPROM size in bytes (512kbit = 64000, 256kbit = 32000)
# Bytes per page write (64 and 128 are common)
# Whether write polling is supported
# ----------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, July 2021
#
# This python library supports the SparkFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatable) single board 
# computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
# ======================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================
# Example 2

from __future__ import print_function
import qwiic_eeprom
import time
import sys

def run_example():

    print("\nSparkFun Qwiic EEPROM, Example 2\n")
    my_eeprom = qwiic_eeprom.QwiicEEPROM()

    if my_eeprom.begin() != True:
        print("\nThe Qwiic EEPROM isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nEEPROM ready!")

    # Set settings for this EEPROM
    my_eeprom.set_memory_size(512000/8) # In bytes. 512kbit = 64kbyte
    my_eeprom.set_page_size(128)    # in bytes. Has 128 byte page size.
    my_eeprom.disable_poll_for_write_complete()  # Supports I2C polling of write completion
    my_eeprom.set_page_write_time(3)    # 3 ms max write time

    print("\nMem size in bytes: " + str(my_eeprom.get_memory_size()))
    print("\nPage size in bytes: " + str(my_eeprom.get_page_size()))
    
    my_value = -7.35
    my_eeprom.write_float(20, my_value) # (location, data)
    my_read = my_eeprom.read_float(20)  # (location)
    # Round to 2-decimal point precision
    my_read = round(my_read, 2)
    print("\nI read: " + str(my_read))

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
