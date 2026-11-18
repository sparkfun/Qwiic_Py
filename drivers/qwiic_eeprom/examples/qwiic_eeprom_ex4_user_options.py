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

import qwiic_eeprom
import qwiic_i2c
import sys

LOCATION_SETTINGS = 0
SETTINGS_SIZE = 10 # 1 int + 2 bytes + 1 float = 10 bytes total

# The settings we keep in EEPROM, with their defaults
class Settings(object):
    def __init__(self, baud_rate=115200, log_date=False, enable_imu=True, cal_value=-5.17):
        self.baud_rate = baud_rate
        self.log_date = log_date
        self.enable_imu = enable_imu
        self.cal_value = cal_value

# Load the current settings from EEPROM into the settings object
def load_user_settings(my_mem, settings):
    # Uncomment these lines to forcibly erase the EEPROM and see how the defaults are set
    # print("\nErasing EEPROM, be patient please")
    # my_mem.erase()

    # Check to see if EEPROM is blank. If the first four spots are zeros then we can assume the EEPROM is blank.
    if my_mem.read_int(LOCATION_SETTINGS) == 0:
        # At power on, settings are set to defaults within the object
        # So go record the object as it currently exists so that defaults are set
        record_user_settings(my_mem, settings)

        print("\nDefault settings applied")
    else:
        settings.baud_rate = my_mem.read_int(LOCATION_SETTINGS)
        settings.log_date = bool(my_mem.read_byte(LOCATION_SETTINGS + 4))
        settings.enable_imu = bool(my_mem.read_byte(LOCATION_SETTINGS + 5))
        # Round to 2-decimal point precision
        settings.cal_value = round(my_mem.read_float(LOCATION_SETTINGS + 6), 2)

# Record the current settings into EEPROM
def record_user_settings(my_mem, settings):
    # Use our individual write functions to make writing this object easier
    my_mem.write_int(LOCATION_SETTINGS, settings.baud_rate)
    qwiic_i2c.delay_ms(100)
    my_mem.write_byte(LOCATION_SETTINGS + 4, int(settings.log_date))
    qwiic_i2c.delay_ms(100)
    my_mem.write_byte(LOCATION_SETTINGS + 5, int(settings.enable_imu))
    qwiic_i2c.delay_ms(100)
    my_mem.write_float(LOCATION_SETTINGS + 6, settings.cal_value)
    qwiic_i2c.delay_ms(100)


print("\nSparkFun Qwiic EEPROM, Example 4\n")
my_eeprom = qwiic_eeprom.QwiicEEPROM()

if not my_eeprom.begin():
    print("\nThe Qwiic EEPROM isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    sys.exit(1)

print("\nEEPROM ready!")

settings = Settings()

load_user_settings(my_eeprom, settings)

print("\nBaud rate: " + str(settings.baud_rate))
print("\nlog_date: " + str(settings.log_date))
print("\ncal_value: " + str(settings.cal_value))

# Now we can change something
print("\nEnter a new baud rate (1200 to 115200): ")
new_baud = int(input())
if new_baud < 1200 or new_baud > 115200:
    print("\nError: baud rate out of range!")
else:
    settings.baud_rate = new_baud

    print("\nThis is the new baud rate: ")
    print(settings.baud_rate)

    record_user_settings(my_eeprom, settings)
