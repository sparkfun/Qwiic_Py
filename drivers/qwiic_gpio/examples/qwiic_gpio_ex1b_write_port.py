#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_gpio_ex1b.py
#
# This script flips all 8 outputs on and off every second.
#------------------------------------------------------------------------
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

import qwiic_gpio
import time
import sys

# This function is used to toggle the GPIO pin settings in a list of GPIO_HI or GPIO_LO
def flipGPIO( gpioConfig ):
    for i in range(len(gpioConfig)):
        if gpioConfig[i] == qwiic_gpio.QwiicGPIO.GPIO_HI:
            gpioConfig[i] = qwiic_gpio.QwiicGPIO.GPIO_LO
        else:
            gpioConfig[i] = qwiic_gpio.QwiicGPIO.GPIO_HI

def runExample():

    print("\nSparkFun Qwiic GPIO Example 1\n")
    myGPIO = qwiic_gpio.QwiicGPIO()

    if myGPIO.isConnected() == False:
        print("The Qwiic GPIO isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    myGPIO.begin()
    myGPIO.pinModePort( [ myGPIO.GPIO_OUT] * myGPIO.NUM_GPIO ) # Set all 8 pins to output

    gpioConfig = [ myGPIO.GPIO_HI, myGPIO.GPIO_LO, myGPIO.GPIO_HI, myGPIO.GPIO_LO, myGPIO.GPIO_HI, myGPIO.GPIO_LO, myGPIO.GPIO_HI, myGPIO.GPIO_LO ]

    while True:
        print("Writing new GPIO port outputs!")
        myGPIO.digitalWritePort( gpioConfig )
        flipGPIO( gpioConfig )
        time.sleep(1)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)