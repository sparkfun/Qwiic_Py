# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_eeprom_ex4_user_options.py
#
# This example demonstrates how to record various user settings easily 
# to EEPROM.
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
# Example 4

from __future__ import print_function
import qwiic_eeprom
import time
import sys
# TODO: remove this?
from collections import namedtuple
from dataclasses import *

LOCATION_SETTINGS = 0
SETTINGS_SIZE = 10 # 2 ints + 2 bools = 10 bytes total

# Load the current settings from EEPROM into the settings struct
def load_user_settings(my_mem, settings):
    # Uncomment these lines to forcibly erase the EEPROM and see how the defaults are set
    # print("\nErasing EEPROM, be patient please")
    # my_mem.erase()    

    # Check to see if EEPROM is blank. If the first four spots are zeros then we can assume the EEPROM is blank.
    num_bytes = 4
    if (my_mem.read_int(LOCATION_SETTINGS) == 0):     # (EEPROM address to read, thing to read to)
        # At power on, settings are set to defaults within the tuple
        # So go record the tuple as it currently exists so that defaults are set
        record_user_settings(my_mem, settings)

        print("\nDefault settings applied")
    else:
        
        settings.baud_rate == my_mem.read_int(0)
        settings.log_date == my_mem.read_byte(4)
        settings.enable_IMU == my_mem.read_byte(5)
        cal_val_temp = my_mem.read_float(6)
        # Round to 2-decimal point precision
        settings.cal_value == round(cal_val_temp, 2)

# Record the current settings into EEPROM
def record_user_settings(my_mem, settings):
    # Use our individual write functions to make writing this class easier
    my_mem.write_int(0, settings.baud_rate)
    time.sleep(0.1)
    my_mem.write_byte(4, settings.log_date)
    time.sleep(0.1)
    my_mem.write_byte(5, settings.enable_IMU)
    time.sleep(0.1)
    my_mem.write_float(6, settings.cal_value)
    time.sleep(0.1)

def run_example():

    print("\nSparkFun Qwiic EEPROM, Example 4\n")
    my_eeprom = qwiic_eeprom.QwiicEEPROM()

    if my_eeprom.begin() != True:
        print("\nThe Qwiic EEPROM isn't connected to the syste. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nEEPROM ready!")
    
    @dataclass
    class Settings:
        baud_rate: int
        log_date: bool
        enable_IMU: bool
        cal_value: float
        
    default_settings = Settings(115200, False, True, -5.17)

    load_user_settings(my_eeprom, default_settings)
        
    print("\nBaud rate: " + str(default_settings.baud_rate))

    log_str = ""
    if default_settings.log_date == True:
        log_str = "True"
    else:
        log_str = "False"
    print("\nlog_date: " + log_str)

    print("\ncal_value: " + str(default_settings.cal_value))

    # Now we can change something
    print("\nEnter a new baud rate (1200 to 115200): ")
    new_baud = input()
    if int(new_baud) < 1200 or int(new_baud) > 115200:
        print("\nError: baud rate out of range!")
    else:
        default_settings = replace(default_settings, baud_rate = int(new_baud))
        
        print("\nThis is the new baud rate: ")
        print(default_settings.baud_rate)
        
        record_user_settings(my_eeprom, default_settings)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
    
