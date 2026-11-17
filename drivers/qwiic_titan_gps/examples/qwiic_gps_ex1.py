#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_gps_ex1.py
#
# Simple Example for SparkFun GPS Breakout - XA1110
# In this example NMEA data is requested from the GPS module and the recieved Latitude,
# Longitude, and Time data is printed to the screen.  
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, October 2019
#
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
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
# Example 1
#

from time import sleep
import sys
import qwiic_titan_gps

def run_example():

    print("SparkFun GPS Breakout - XA1110!")
    qwiicGPS = qwiic_titan_gps.QwiicTitanGps()

    if qwiicGPS.connected is False:
        print("Could not connect to to the SparkFun GPS Unit. Double check that\
              it's wired correctly.", file=sys.stderr)
        return

    qwiicGPS.begin()

    while True:
        try:
            if qwiicGPS.get_nmea_data() is True:
                print("Latitude: {}, Longitude: {}, Time: {}".format(
                    qwiicGPS.gnss_messages['Latitude'],
                    qwiicGPS.gnss_messages['Longitude'],
                    qwiicGPS.gnss_messages['Time'])) # Time will be UTC time as a list [hh, mm, ss]
        except:
            print("Error while retrieving GPS Values!")

        sleep(1)


if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Basic Example.")
        sys.exit(0)
