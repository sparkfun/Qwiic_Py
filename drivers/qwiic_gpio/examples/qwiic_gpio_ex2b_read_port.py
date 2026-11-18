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
import qwiic_i2c
import sys


print("\nSparkFun Qwiic GPIO Example 2b\n")
my_gpio = qwiic_gpio.QwiicGPIO()

if not my_gpio.is_connected():
    print("The Qwiic GPIO isn't connected to the system. Please check your connection",
          file=sys.stderr)
    sys.exit(1)

my_gpio.begin()
my_gpio.pin_mode_port( [my_gpio.GPIO_IN] * my_gpio.NUM_GPIO ) # pass in a list of 8 GPIO_IN values

while True:
    port_values = my_gpio.digital_read_port()

    for i in range(my_gpio.NUM_GPIO):
        print("GPIO " + str(i) + ": " + ("HIGH" if port_values[i] == my_gpio.GPIO_HI else "LOW") )

    qwiic_i2c.delay_ms(250)
