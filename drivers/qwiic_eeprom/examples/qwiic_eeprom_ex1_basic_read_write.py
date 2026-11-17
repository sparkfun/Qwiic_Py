# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_eeprom_ex1_basic_read_write.py
#
# This example demonstrates how to read and write various variables to memory.
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
# Example 1

from __future__ import print_function
import qwiic_eeprom
import time
import sys

def run_example():

    print("\nSparkFun Qwiic EEPROM, Example 1\n")
    my_eeprom = qwiic_eeprom.QwiicEEPROM()

    if my_eeprom.begin() != True:
        print("\nThe Qwiic EEPROM isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nEEPROM ready!")

    print("\nMem size in bytes: " + str(my_eeprom.length()))

    my_value1 = 200 # 0xC8
    my_eeprom.write_byte(300, my_value1)  # (location = 0x12C, data byte)
    my_read1 = my_eeprom.read_byte(300) # (location = 0x12C)
    print("\nI read: " + str(my_read1)) # Should be 0xC8 = 200
    
    my_value2 = -366
    my_eeprom.write_int(10, my_value2)
    my_read2 = my_eeprom.read_int(10)    # (location)
    print("\nI read: " + str(my_read2))

    my_value3 = -7.35
    my_eeprom.write_float(9, my_value3)
    my_read3 = my_eeprom.read_float(9)    # (location)
    # Round to 2-decimal point precision
    my_read3 = round(my_read3, 2)
    print("\nI read: " + str(my_read3))

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
    
