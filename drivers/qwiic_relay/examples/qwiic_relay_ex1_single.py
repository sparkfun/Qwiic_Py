#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_relay_ex1_single.py
#
# Example that shows the basics of using the single relay.
#-------------------------------------------------------------------------------
#
# Written by SparkFun Electronics, November 2023
# 
# This python library supports the SparkFun Electronics Qwiic sensor/board
# ecosystem on Python compatible devices, such as the Raspberry Pi, MicroPython
# and CircuitPython enabled microcontrollers, etc.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
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
#===============================================================================
# Example 1 - Single

import qwiic_relay
import qwiic_i2c
import sys

# Be sure to initialize your relay with the proper address.
my_relay = qwiic_relay.QwiicRelay(qwiic_relay.SINGLE_RELAY_DEFAULT_ADDR)
# my_relay = qwiic_relay.QwiicRelay(qwiic_relay.SINGLE_RELAY_JUMPER_CLOSE_ADDR)


print("\nSparkFun Qwiic Relay Example 1 - Single\n")

if not my_relay.begin():
    print("The Qwiic Relay isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    sys.exit(1)

# Repeat a couple times
for i in range(2):
    # Turn relay on
    my_relay.set_relay_on()

    # Print state of relay
    print("Relay state: " + str(my_relay.get_relay_state()))

    # Wait a moment
    qwiic_i2c.delay_ms(1000)

    # Turn relay off
    my_relay.set_relay_off()

    # Print state of relay
    print("Relay state: " + str(my_relay.get_relay_state()))

    # Wait a moment
    qwiic_i2c.delay_ms(1000)
