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
import qwiic_i2c
import sys

# This function is used to toggle the GPIO pin settings in a list of GPIO_HI or GPIO_LO
def flip_gpio( gpio_config ):
    for i in range(len(gpio_config)):
        if gpio_config[i] == qwiic_gpio.QwiicGPIO.GPIO_HI:
            gpio_config[i] = qwiic_gpio.QwiicGPIO.GPIO_LO
        else:
            gpio_config[i] = qwiic_gpio.QwiicGPIO.GPIO_HI

def run_example():

    print("\nSparkFun Qwiic GPIO Example 1\n")
    my_gpio = qwiic_gpio.QwiicGPIO()

    if not my_gpio.is_connected():
        print("The Qwiic GPIO isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    my_gpio.begin()
    my_gpio.pin_mode_port( [ my_gpio.GPIO_OUT] * my_gpio.NUM_GPIO ) # Set all 8 pins to output

    gpio_config = [ my_gpio.GPIO_HI, my_gpio.GPIO_LO, my_gpio.GPIO_HI, my_gpio.GPIO_LO, my_gpio.GPIO_HI, my_gpio.GPIO_LO, my_gpio.GPIO_HI, my_gpio.GPIO_LO ]

    while True:
        print("Writing new GPIO port outputs!")
        my_gpio.digital_write_port( gpio_config )
        flip_gpio( gpio_config )
        qwiic_i2c.delay_ms(1000)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)