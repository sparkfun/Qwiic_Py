# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_eeprom_ex3_advanced_i2c.py
#
# This example demonstrates how to pass a custom EEPROM address.
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
# Example 3

from __future__ import print_function
import qwiic_eeprom
import time
import sys

def run_example():
    
    EEPROM_ADDRESS = 0b1010001 # 0b1010(A2 A1 A0): A standard I2C EEPROM with the ADR0 bit set to VCC

    print("\nSparkFun Qwiic EEPROM, Example 3\n")
    my_eeprom = qwiic_eeprom.QwiicEEPROM(0x51)

    if my_eeprom.begin() != True:
        print("\nThe Qwiic EEPROM isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    print("\nEEPROM ready!")

    my_value = -7.35
    my_eeprom.write_float(20, my_value)   # (location, data)
    my_read = my_eeprom.read_float(20) # (location to read)
    # Round to 2-decimal point precision
    my_read = round(my_read, 2)
    print("\nI read: " + str(my_read))

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
