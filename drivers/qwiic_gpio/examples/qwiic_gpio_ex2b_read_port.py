#!/usr/bin/env python
# -----------------------------------------------------------------------------
# qwiic_gpio_ex2b.py
#

# This script allows the user to read the status of all 8 GPIO simultaneously
# ------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
#
# This python library supports the SparkFun Electroncis qwiic
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
# ==================================================================================
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
# ==================================================================================

import qwiic_gpio
import time
import sys


def runExample():

    print("\nSparkFun Qwiic GPIO Example 2b\n")
    myGPIO = qwiic_gpio.QwiicGPIO()

    if myGPIO.isConnected() == False:
        print("The Qwiic GPIO isn't connected to the system. Please check your connection",
              file=sys.stderr)
        return

    myGPIO.begin()
    myGPIO.pinModePort( [myGPIO.GPIO_IN] * myGPIO.NUM_GPIO ) # pass in a list of 8 GPIO_IN values

    while True:
        portValues = myGPIO.digitalReadPort()

        for i in range(myGPIO.NUM_GPIO):
            print("GPIO " + str(i) + ": " + ("HIGH" if portValues[i] == myGPIO.GPIO_HI else "LOW") )

        time.sleep(.25)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 2b")
        sys.exit(0)
