#!/usr/bin/env python
#-----------------------------------------------------------------------------
# ex1_splash_screen.py
#
# Simple Example for an OLED Display that displays the SparkFun splash screen
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2021
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers.
#
# More information on qwiic is at https:# www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
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

import qwiic_oled
import time
import sys

# --------- SET YOUR OLED DISPLAY TYPE HERE ----------------
# The library supports three different types of SparkFun boards. The demo uses the following
# variables to determine which device is being used. Uncomment the device being used for this demo.

userOLED = qwiic_oled.QwiicMicroOled()   # Micro OLED             https://www.sparkfun.com/products/14532
# userOLED = qwiic_oled.QwiicOledDisplay() # "Narrow" OLED          https://www.sparkfun.com/products/24606
# userOLED = qwiic_oled.QwiicLargeOled()  # Qwiic OLED 1.3in        https://www.sparkfun.com/products/23453

def runExample():
    #  Before you can start using the OLED, call begin() to init
    #  all of the pins and configure the OLED.

    print("\nOLED Display - Splash screen example\n")
    myOLED = userOLED

    if not myOLED.connected:
        print("The OLED Display isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    myOLED.begin()

    #  clear(ALL) will clear out the OLED's graphic memory.
    myOLED.clear(myOLED.ALL) #  Clear the display's memory (gets rid of artifacts)
  
    #  To actually draw anything on the display, you must call the display() function.
    myOLED.display()  #  Display buffer contents
    time.sleep(3)

    #  clear(PAGE) will clear the Arduino's display buffer.
    myOLED.clear(myOLED.PAGE)  #  Clear the display's buffer

    #  Display buffer contents
    myOLED.display()
    time.sleep(3)

    qwiic_oled.oled_logos.add_logo(myOLED._screenbuffer)

    myOLED.display()

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding OLED bitmap Example")
        sys.exit(0)
