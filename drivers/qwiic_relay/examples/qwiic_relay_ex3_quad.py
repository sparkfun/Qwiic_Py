#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_relay_ex2_quad.py
#
# Example that shows the basics of using the quad relays.
#------------------------------------------------------------------------
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
#==================================================================================
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
#==================================================================================
# Example 3 - Quad

import qwiic_relay
import qwiic_i2c
import sys

# Be sure to initialize your relay with the proper address.
my_relays = qwiic_relay.QwiicRelay(qwiic_relay.QUAD_RELAY_DEFAULT_ADDR)
# my_relays = qwiic_relay.QwiicRelay(qwiic_relay.QUAD_RELAY_JUMPER_CLOSE_ADDR)
# my_relays = qwiic_relay.QwiicRelay(qwiic_relay.QUAD_SOLID_STATE_RELAY_DEFAULT_ADDR)
# my_relays = qwiic_relay.QwiicRelay(qwiic_relay.QUAD_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR)

def run_example():

    print("\nSparkFun Qwiic Relay Example 3 - Quad\n")

    if not my_relays.begin():
        print("The Qwiic Relay isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    # Turn on relays one and three
    my_relays.set_relay_on(1)
    my_relays.set_relay_on(3)
    
    # Print the status of all relays
    print("Relay 1 state: " + str(my_relays.get_relay_state(1)))
    print("Relay 2 state: " + str(my_relays.get_relay_state(2)))
    print("Relay 3 state: " + str(my_relays.get_relay_state(3)))
    print("Relay 4 state: " + str(my_relays.get_relay_state(4)))
    print()

    # Wait a moment
    qwiic_i2c.delay_ms(1000)
    
    # Turn off 1 and 3, turn on 2 and 4
    my_relays.set_relay_off(1)
    my_relays.set_relay_on(2)
    my_relays.set_relay_off(3)
    my_relays.set_relay_on(4)
    
    # Print the status of all relays
    print("Relay 1 state: " + str(my_relays.get_relay_state(1)))
    print("Relay 2 state: " + str(my_relays.get_relay_state(2)))
    print("Relay 3 state: " + str(my_relays.get_relay_state(3)))
    print("Relay 4 state: " + str(my_relays.get_relay_state(4)))
    print()

    # Wait a moment
    qwiic_i2c.delay_ms(1000)
    
    # Turn all relays on
    my_relays.set_all_relays_on()
    
    # Print the status of all relays
    print("Relay 1 state: " + str(my_relays.get_relay_state(1)))
    print("Relay 2 state: " + str(my_relays.get_relay_state(2)))
    print("Relay 3 state: " + str(my_relays.get_relay_state(3)))
    print("Relay 4 state: " + str(my_relays.get_relay_state(4)))
    print()

    # Wait a moment
    qwiic_i2c.delay_ms(1000)

    # Turn all relays off
    my_relays.set_all_relays_off()
    
    # Print the status of all relays
    print("Relay 1 state: " + str(my_relays.get_relay_state(1)))
    print("Relay 2 state: " + str(my_relays.get_relay_state(2)))
    print("Relay 3 state: " + str(my_relays.get_relay_state(3)))
    print("Relay 4 state: " + str(my_relays.get_relay_state(4)))
    print()
    
if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 3")
        sys.exit(0)